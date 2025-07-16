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
export function appendMessage(text, className, isUser = true) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${className}`;

    if (isUser) {
        const p = document.createElement('p');
        p.textContent = text;
        messageDiv.appendChild(p);
    } else {
        // For AI messages, we set innerHTML after sanitizing
        messageDiv.innerHTML = text;
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
    aiMessageDiv.appendChild(contentP);
    chatBox.appendChild(aiMessageDiv);
    return { aiMessageDiv, contentP };
}

/**
 * Updates the content of a streaming AI message.
 * @param {HTMLElement} element - The <p> element holding the content.
 * @param {string} content - The new content to display.
 */
export function updateStreamedMessage(element, content) {
    element.textContent = content;
    chatBox.scrollTop = chatBox.scrollHeight;
}

/**
 * Finalizes a streamed message by rendering it as Markdown.
 * @param {HTMLElement} element - The <p> element holding the content.
 * @param {string} fullText - The complete text of the AI's response.
 */
export function finalizeStreamedMessage(element, fullText) {
    const rawHtml = marked.parse(fullText);
    const sanitizedHtml = DOMPurify.sanitize(rawHtml);
    element.innerHTML = sanitizedHtml;
    // Apply syntax highlighting to any new code blocks
    element.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightElement(block);
    });
}

/**
 * Toggles the loading state of the input form.
 * @param {boolean} isLoading - Whether to show the loading state.
 */
export function toggleLoadingState(isLoading) {
    chatForm.querySelector('input[type="text"]').disabled = isLoading;
    sendBtn.disabled = isLoading;
    sendBtn.classList.toggle('loading', isLoading);
    stopGeneratingBtn.style.display = isLoading ? 'block' : 'none';
}

/**
 * Toggles the dark/light theme for the application.
 */
export function toggleTheme() {
    const isDarkMode = document.body.classList.toggle('dark-mode');
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
}

/**
 * Applies the theme from localStorage when the page loads.
 */
export function applyInitialTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
    } else {
        // Default to light mode if nothing is saved or it's set to light
        document.body.classList.remove('dark-mode');
    }
}