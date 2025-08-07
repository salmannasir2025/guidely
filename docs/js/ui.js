const chatBox = document.getElementById('chat-box');
const chatForm = document.getElementById('chat-form');
const sendBtn = document.getElementById('send-btn');
const stopGeneratingBtn = document.getElementById('stop-generating-btn');

/**
 * Appends a new message to the chat box.
 * @param {string} text - The message content (can be plain text or HTML).
 * @param {string} className - The CSS class for the message div.
 * @param {boolean} isUser - True if the message is from the user.
 */
export function appendMessage(text, className, isUser = className === 'user-message') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${className}`;

    if (isUser) {
        const p = document.createElement('p');
        p.textContent = text;
        messageDiv.appendChild(p);
    } else {
        // For AI messages, we set innerHTML after sanitizing
        const p = document.createElement('p');
        p.textContent = text;
        messageDiv.appendChild(p);
    }

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

/**
 * Creates a placeholder for the AI's streaming response.
 * @returns {{aiMessageDiv: HTMLElement, contentP: HTMLElement}}
 */
export function createStreamedMessage() {
    const aiMessageDiv = document.createElement('div');
    aiMessageDiv.className = 'message ai-message';
    const contentP = document.createElement('p');
    contentP.textContent = 'Thinking...';
    aiMessageDiv.appendChild(contentP);
    chatBox.appendChild(aiMessageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    return { aiMessageDiv, contentP };
}

/**
 * Updates the content of a streaming AI message.
 * @param {HTMLElement} element - The <p> element holding the content.
 * @param {string} content - The new content to display.
 */
export function updateStreamedMessage(element, content) {
    element.textContent = content || 'Thinking...';
    chatBox.scrollTop = chatBox.scrollHeight;
}

/**
 * Finalizes a streamed message by rendering it as Markdown.
 * @param {HTMLElement} element - The <p> element holding the content.
 * @param {string} fullText - The complete text of the AI's response.
 */
export function finalizeStreamedMessage(element, fullText) {
    if (!fullText || fullText.trim() === '') {
        element.textContent = 'No response received.';
        return;
    }

    try {
        // Check if marked is available for markdown parsing
        if (typeof marked !== 'undefined' && typeof DOMPurify !== 'undefined') {
            const rawHtml = marked.parse(fullText);
            const sanitizedHtml = DOMPurify.sanitize(rawHtml);
            element.innerHTML = sanitizedHtml;
            
            // Apply syntax highlighting to any new code blocks if hljs is available
            if (typeof hljs !== 'undefined') {
                element.querySelectorAll('pre code').forEach((block) => {
                    hljs.highlightElement(block);
                });
            }
        } else {
            // Fallback to plain text if markdown libraries aren't available
            element.textContent = fullText;
        }
    } catch (error) {
        console.error('Error finalizing message:', error);
        element.textContent = fullText;
    }
}

/**
 * Toggles the loading state of the input form.
 * @param {boolean} isLoading - Whether to show the loading state.
 * @param {HTMLElement} specificButton - Optional specific button to toggle loading state.
 */
export function toggleLoadingState(isLoading, specificButton = null) {
    const inputField = chatForm.querySelector('input[type="text"]');
    
    if (inputField) {
        inputField.disabled = isLoading;
    }
    
    if (specificButton) {
        specificButton.disabled = isLoading;
        specificButton.classList.toggle('loading', isLoading);
    } else {
        sendBtn.disabled = isLoading;
        sendBtn.classList.toggle('loading', isLoading);
        stopGeneratingBtn.style.display = isLoading ? 'block' : 'none';
    }
}

/**
 * Toggles the dark/light theme for the application.
 */
export function toggleTheme() {
    const isDarkMode = document.body.classList.toggle('dark-mode');
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
    
    // Update theme toggle button text
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    if (themeToggleBtn) {
        const buttonText = themeToggleBtn.querySelector('.button-text');
        if (buttonText) {
            buttonText.textContent = isDarkMode ? '☀️' : '🌙';
        }
    }
}

/**
 * Applies the theme from localStorage when the page loads.
 */
export function applyInitialTheme() {
    const savedTheme = localStorage.getItem('theme');
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
        if (themeToggleBtn) {
            const buttonText = themeToggleBtn.querySelector('.button-text');
            if (buttonText) {
                buttonText.textContent = '☀️';
            }
        }
    } else {
        // Default to light mode if nothing is saved or it's set to light
        document.body.classList.remove('dark-mode');
        if (themeToggleBtn) {
            const buttonText = themeToggleBtn.querySelector('.button-text');
            if (buttonText) {
                buttonText.textContent = '🌙';
            }
        }
    }
}