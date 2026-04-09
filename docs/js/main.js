import { askAI, uploadFile, getUserHistory, clearUserHistory, login, register, verifyGoogleToken, saveProviderKey, listProviderKeys, deleteProviderKey } from './api.js';
import { BACKEND_URL } from './config.js';
import {
    appendMessage,
    createStreamedMessage,
    updateStreamedMessage,
    finalizeStreamedMessage,
    toggleLoadingState,
    toggleTheme,
    applyInitialTheme,
} from './ui.js';

document.addEventListener('DOMContentLoaded', () => {
    console.log('Frontend initialized with backend URL:', BACKEND_URL);

    // --- DOM Elements ---
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const imageInput = document.getElementById('image-input');
    const voiceInput = document.getElementById('voice-input');
    const languageSelector = document.getElementById('language-selector');
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    const stopGeneratingBtn = document.getElementById('stop-generating-btn');
    const clearHistoryBtn = document.getElementById('clear-history-btn');

    // Auth Elements
    const authCtaBanner = document.getElementById('auth-cta-banner');
    const openAuthBtn = document.getElementById('open-auth-btn');
    const closeCtaBtn = document.getElementById('close-cta-btn');
    const authModal = document.getElementById('auth-modal');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    
    // Settings Elements
    const settingsBtn = document.getElementById('settings-btn');
    const settingsModal = document.getElementById('settings-modal');
    const closeSettingsBtn = document.getElementById('close-settings-btn');
    const providerItems = document.querySelectorAll('.provider-item');
    const keyInputForm = document.getElementById('key-input-form');
    const keyInputTitle = document.getElementById('key-input-title');
    const apiKeyInput = document.getElementById('api-key-input');
    const saveKeyBtn = document.getElementById('save-key-btn');
    const deleteKeyBtn = document.getElementById('delete-key-btn');
    const cancelKeyBtn = document.getElementById('cancel-key-btn');
    const activeProviderSelect = document.getElementById('active-provider-select');
    
    let currentEditingProvider = null;

    // --- Helper Functions ---
    const getUserId = () => {
        let userId = localStorage.getItem('regional-ai-user-id');
        if (!userId) {
            userId = `web-user-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
            localStorage.setItem('regional-ai-user-id', userId);
        }
        return userId;
    };

    const isUserLoggedIn = () => !!localStorage.getItem('guidely_jwt_token');

    const checkTrialStatus = () => {
        if (isUserLoggedIn()) return;

        let trialStart = localStorage.getItem('guidely_trial_start');
        if (!trialStart) {
            trialStart = Date.now().toString();
            localStorage.setItem('guidely_trial_start', trialStart);
        }

        const oneDayMs = 24 * 60 * 60 * 1000;
        const timeElapsed = Date.now() - parseInt(trialStart);

        if (timeElapsed > oneDayMs && !localStorage.getItem('guidely_cta_dismissed')) {
            authCtaBanner.style.display = 'flex';
        }
    };

    // --- Event Listeners ---
    imageInput.addEventListener('change', async (event) => {
        const file = imageInput.files[0];
        if (file) {
            appendMessage(`Processing image: ${file.name}...`, 'ai-message');
            try {
                const extractedText = await uploadFile(file, 'image');
                if (extractedText) {
                    appendMessage(`Extracted Text: ${extractedText}`, 'ai-message');
                    // Optionally auto-fill the input with extracted text
                    if (userInput.value.trim() === '') {
                        userInput.value = extractedText;
                    }
                }
            } catch (error) {
                appendMessage(`Error processing image: ${error.message}`, 'ai-message');
            }
        }
        // Reset the input to allow re-uploading the same file.
        imageInput.value = '';
    });

    voiceInput.addEventListener('change', async (event) => {
        const file = voiceInput.files[0];
        if (file) {
            appendMessage(`Transcribing audio: ${file.name}...`, 'ai-message');
            try {
                const transcribedText = await uploadFile(file, 'voice');
                if (transcribedText) {
                    userInput.value = transcribedText; // Put in the user input
                    appendMessage(`Transcribed Text: ${transcribedText}`, 'ai-message');
                }
            } catch (error) {
                appendMessage(`Error transcribing audio: ${error.message}`, 'ai-message');
            }
        }
        // Reset the input to allow re-uploading the same file.
        voiceInput.value = '';
    });

    // Clear history functionality
    clearHistoryBtn.addEventListener('click', async () => {
        if (confirm('Are you sure you want to clear your chat history? This action cannot be undone.')) {
            try {
                toggleLoadingState(true, clearHistoryBtn);
                await clearUserHistory();
                
                // Clear the chat box
                const chatBox = document.getElementById('chat-box');
                chatBox.innerHTML = `
                    <div class="message ai-message">
                        <p>Hello! How can I help you today? Ask me a question about Math, Physics, Chemistry, or anything else!</p>
                    </div>
                `;
                
                appendMessage('Chat history cleared successfully!', 'ai-message');
            } catch (error) {
                appendMessage(`Error clearing history: ${error.message}`, 'ai-message');
            } finally {
                toggleLoadingState(false, clearHistoryBtn);
            }
        }
    });

    let abortController = null;

    // Apply the saved theme as soon as the page loads
    applyInitialTheme();
    checkTrialStatus();

    // --- Auth Event Listeners ---
    openAuthBtn.addEventListener('click', () => {
        authModal.style.display = 'flex';
        initGoogleSignin();
    });

    closeCtaBtn.addEventListener('click', () => {
        authCtaBanner.style.display = 'none';
        localStorage.setItem('guidely_cta_dismissed', 'true');
    });

    closeModalBtn.addEventListener('click', () => authModal.style.display = 'none');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.getAttribute('data-tab');
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(`${tabId}-tab`).classList.add('active');
        });
    });

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('login-email').value;
        const pass = document.getElementById('login-password').value;
        try {
            await login(email, pass);
            location.reload(); // Refresh to update UI state
        } catch (err) {
            alert('Login failed: ' + err.message);
        }
    });

    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('signup-name').value;
        const email = document.getElementById('signup-email').value;
        const pass = document.getElementById('signup-password').value;
        try {
            await register({ full_name: name, email: email, password: pass });
            await login(email, pass);
            location.reload();
        } catch (err) {
            alert('Signup failed: ' + err.message);
        }
    });

    function initGoogleSignin() {
        if (typeof google === 'undefined') return;
        
        const handleCredentialResponse = async (response) => {
            try {
                await verifyGoogleToken(response.credential);
                location.reload();
            } catch (err) {
                alert('Google Sign-In failed: ' + err.message);
            }
        };

        google.accounts.id.initialize({
            client_id: "YOUR_GOOGLE_CLIENT_ID", // To be updated by user in config
            callback: handleCredentialResponse
        });

        google.accounts.id.renderButton(
            document.getElementById("google-login-btn"),
            { theme: "outline", size: "large", width: 340 }
        );
        google.accounts.id.renderButton(
            document.getElementById("google-signup-btn"),
            { theme: "outline", size: "large", width: 340 }
        );
    }

    // --- Settings / Key Management Logic ---
    const ALL_PROVIDERS = ['openai', 'gemini', 'minimax', 'grok', 'qwen'];
    const FREE_PROVIDERS = ['minimax', 'qwen'];

    const loadProviderStatuses = async () => {
        if (!isUserLoggedIn()) return;
        try {
            const configuredProviders = await listProviderKeys();

            // Reset ALL provider statuses to default
            ALL_PROVIDERS.forEach(p => {
                const el = document.getElementById(`${p}-status`);
                if (!el) return;
                if (p === 'gemini') {
                    el.textContent = 'Using System Key';
                } else if (FREE_PROVIDERS.includes(p)) {
                    el.textContent = 'Free — Key Required';
                } else {
                    el.textContent = 'Not Configured';
                }
                el.classList.remove('status-active');
            });

            configuredProviders.forEach(p => {
                const statusEl = document.getElementById(`${p}-status`);
                if (statusEl) {
                    statusEl.textContent = 'Active (Your Key)';
                    statusEl.classList.add('status-active');
                }
            });
        } catch (err) {
            console.error('Failed to load provider statuses:', err);
        }
    };

    settingsBtn.addEventListener('click', () => {
        if (!isUserLoggedIn()) {
            authModal.style.display = 'flex';
            return;
        }
        settingsModal.style.display = 'flex';
        loadProviderStatuses();
    });

    closeSettingsBtn.addEventListener('click', () => {
        settingsModal.style.display = 'none';
        keyInputForm.style.display = 'none';
    });

    providerItems.forEach(item => {
        const editBtn = item.querySelector('.edit-key-btn');
        editBtn.addEventListener('click', async () => {
            const provider = item.getAttribute('data-provider');
            currentEditingProvider = provider;
            keyInputTitle.textContent = `Manage ${provider.charAt(0).toUpperCase() + provider.slice(1)} Key`;
            keyInputForm.style.display = 'block';
            apiKeyInput.value = '';
            
            // Check if key exists to show delete button
            const configured = await listProviderKeys();
            deleteKeyBtn.style.display = configured.includes(provider) ? 'inline-block' : 'none';
        });
    });

    saveKeyBtn.addEventListener('click', async () => {
        const key = apiKeyInput.value.trim();
        if (!key) return;
        
        try {
            toggleLoadingState(true, saveKeyBtn);
            await saveProviderKey(currentEditingProvider, key);
            keyInputForm.style.display = 'none';
            loadProviderStatuses();
            alert(`Key for ${currentEditingProvider} saved securely.`);
        } catch (err) {
            alert('Failed to save key: ' + err.message);
        } finally {
            toggleLoadingState(false, saveKeyBtn);
        }
    });

    deleteKeyBtn.addEventListener('click', async () => {
        if (!confirm(`Delete key for ${currentEditingProvider}?`)) return;
        try {
            toggleLoadingState(true, deleteKeyBtn);
            await deleteProviderKey(currentEditingProvider);
            keyInputForm.style.display = 'none';
            loadProviderStatuses();
        } catch (err) {
            alert('Deletion failed: ' + err.message);
        } finally {
            toggleLoadingState(false, deleteKeyBtn);
        }
    });

    cancelKeyBtn.addEventListener('click', () => {
        keyInputForm.style.display = 'none';
    });

    // --- Event Handlers ---
    const handleFormSubmit = async (event) => {
        event.preventDefault();
        const query = userInput.value.trim();
        if (!query) return;

        toggleLoadingState(true);
        appendMessage(query, 'user-message');
        userInput.value = '';

        const { aiMessageDiv, contentP } = createStreamedMessage();
        let fullResponse = '';
        abortController = new AbortController();

        const payload = {
            query: query,
            mode: 'tutor',
            language_code: languageSelector.value,
            provider: activeProviderSelect.value,
        };

        console.log('Sending request with payload:', payload);

        await askAI(
            payload,
            abortController.signal,
            (chunk) => {
                // Process incoming stream chunks
                const lines = chunk.split('\n').filter(line => line.trim() !== '');
                for (const line of lines) {
                    try {
                        const parsed = JSON.parse(line);
                        console.log('Parsed chunk:', parsed);
                        
                        if (parsed.type === 'content' && parsed.chunk) {
                            fullResponse += parsed.chunk;
                            updateStreamedMessage(contentP, fullResponse);
                        } else if (parsed.type === 'result' && parsed.chunk) {
                            fullResponse = parsed.chunk;
                            updateStreamedMessage(contentP, fullResponse);
                        }
                    } catch (e) {
                        console.error('Error parsing stream line:', e, 'Line:', line);
                        // If it's not JSON, treat it as plain text
                        if (line.trim()) {
                            fullResponse += line;
                            updateStreamedMessage(contentP, fullResponse);
                        }
                    }
                }
            },
            () => {
                // On stream completion
                console.log('Stream completed. Full response:', fullResponse);
                finalizeStreamedMessage(contentP, fullResponse);
                toggleLoadingState(false);
                abortController = null;
            },
            (error) => {
                // On error
                console.error('Stream error:', error);
                contentP.textContent = `Error: ${error.message}`;
                contentP.style.color = 'red';
                toggleLoadingState(false);
                abortController = null;
            }
        );
    };

    // --- Event Listeners ---
    chatForm.addEventListener('submit', handleFormSubmit);
    themeToggleBtn.addEventListener('click', toggleTheme);
    stopGeneratingBtn.addEventListener('click', () => {
        if (abortController) {
            abortController.abort();
            appendMessage('Generation stopped by user.', 'ai-message');
        }
    });

    // Test backend connection on load
    fetch(`${BACKEND_URL}/health`)
        .then(response => {
            if (response.ok) {
                console.log('✅ Backend connection successful');
            } else {
                console.warn('⚠️ Backend health check failed:', response.status);
            }
        })
        .catch(error => {
            console.error('❌ Backend connection failed:', error);
            appendMessage('Warning: Unable to connect to backend server. Please check your internet connection.', 'ai-message');
        });
});