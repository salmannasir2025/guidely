import { askAI, uploadFile, getUserHistory, clearUserHistory } from './api.js';
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

    // --- Helper Functions ---
    const getUserId = () => {
        let userId = localStorage.getItem('regional-ai-user-id');
        if (!userId) {
            userId = `web-user-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
            localStorage.setItem('regional-ai-user-id', userId);
        }
        return userId;
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