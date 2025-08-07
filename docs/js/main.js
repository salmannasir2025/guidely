import { askAI } from './api.js';
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

    // --- DOM Elements ---
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const imageInput = document.getElementById('image-input');
    const voiceInput = document.getElementById('voice-input');
    const languageSelector = document.getElementById('language-selector');
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    const stopGeneratingBtn = document.getElementById('stop-generating-btn');

    // --- Helper Functions ---


    const getUserId = () => {
        let userId = localStorage.getItem('regional-ai-user-id');
        if (!userId) {
            userId = `web-user-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
            localStorage.setItem('regional-ai-user-id', userId);
        }
        return userId;
    };

    const uploadFile = async (file, uploadType) => {
        if (!file) return null;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${BACKEND_URL}/api/data/upload-${uploadType}`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `Upload failed for ${uploadType}.`);
            }

            const data = await response.json();
            return data.text; // Return the extracted text or the transcription

        } catch (error) {
            console.error(`Error uploading ${uploadType}:`, error);
            appendMessage(`Error uploading ${uploadType}: ${error.message}`, 'ai-message');
            return null;
        }
    };

    // --- Event Listeners ---

    imageInput.addEventListener('change', async (event) => {
        const file = imageInput.files[0];
        if (file) {
            appendMessage(`Processing image...`, 'ai-message');
            const extractedText = await uploadFile(file, 'image');
            if (extractedText) {
                appendMessage(`Extracted Text: ${extractedText}`, 'ai-message');
            }
        }
        // Reset the input to allow re-uploading the same file.
        imageInput.value = '';
    });

    voiceInput.addEventListener('change', async (event) => {
        const file = voiceInput.files[0];
        if (file) {
            appendMessage(`Transcribing audio...`, 'ai-message');
            const transcribedText = await uploadFile(file, 'voice');
            if (transcribedText) {
                userInput.value = transcribedText; // Put in the user input
                appendMessage(`Transcribed Text: ${transcribedText}`, 'ai-message');
            }
        }
        // Reset the input to allow re-uploading the same file.
        voiceInput.value = '';
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
            user_id: getUserId(),
            mode: 'tutor',
            language_code: languageSelector.value,
        };

        await askAI(
            payload,
            abortController.signal,
            (chunk) => {
                // Process incoming stream chunks
                const lines = chunk.split('\n').filter(line => line.trim() !== '');
                for (const line of lines) {
                    try {
                        const parsed = JSON.parse(line);
                        if (parsed.type === 'content') {
                            fullResponse += parsed.chunk;
                            updateStreamedMessage(contentP, fullResponse);
                        } else if (parsed.type === 'result') {
                            fullResponse = parsed.chunk;
                            updateStreamedMessage(contentP, fullResponse);
                        }
                    } catch (e) {
                        console.error('Error parsing stream line:', e);
                    }
                }
            },
            () => {
                // On stream completion
                finalizeStreamedMessage(contentP, fullResponse);
                toggleLoadingState(false);
                abortController = null;
            },
            (error) => {
                // On error
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
    stopGeneratingBtn.addEventListener('click', () => abortController?.abort());
});