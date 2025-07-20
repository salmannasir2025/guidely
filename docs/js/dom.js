export const DOMElements = {
    chatContainer: document.querySelector('.chat-container'),
    chatForm: document.getElementById('chat-form'),
    userInput: document.getElementById('user-input'),
    chatBox: document.getElementById('chat-box'),
    imageUploadBtn: document.getElementById('image-upload-btn'),
    imageInput: document.getElementById('image-input'),
    voiceUploadBtn: document.getElementById('voice-upload-btn'),
    voiceInput: document.getElementById('voice-input'),
    languageSelector: document.getElementById('language-selector'),
    themeToggleBtn: document.getElementById('theme-toggle-btn'),
    clearHistoryBtn: document.getElementById('clear-history-btn'),
    sendBtn: document.getElementById('send-btn'),
    stopGeneratingBtn: document.getElementById('stop-generating-btn'),
};

export function clearChatBox() {
    DOMElements.chatBox.innerHTML = '';
}

export function scrollChatBoxToBottom() {
    DOMElements.chatBox.scrollTop = DOMElements.chatBox.scrollHeight;
}

function createButton(options) {
    const button = document.createElement('button');
    button.className = options.className;
    button.title = options.title;

    const textSpan = document.createElement('span');
    textSpan.className = 'button-text';
    textSpan.innerHTML = options.initialHtml;
    button.appendChild(textSpan);

    button.appendChild(document.createElement('div')).className = 'spinner';

    button.onclick = (e) => {
        e.stopPropagation();
        options.onClick(button);
    };
    return button;
}

export function addMessage(text, className, handlers = {}) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', className);

    const contentWrapper = document.createElement('div');
    contentWrapper.className = 'message-content-wrapper';

    const p = document.createElement('p');
    p.textContent = text;
    contentWrapper.appendChild(p);

    const isRealAiMessage = className === 'ai-message' && !text.startsWith('Thinking') && !text.startsWith('Processing') && !text.startsWith('Sorry');
    if (isRealAiMessage) {
        if (handlers.onPlayAudio) {
            const playButton = createButton({
                className: 'play-audio-btn icon-btn', initialHtml: '🔊', title: 'Read aloud', onClick: (btn) => handlers.onPlayAudio(text, btn),
            });
            contentWrapper.appendChild(playButton);
        }
        if (handlers.onCopy) {
            const copyButton = createButton({
                className: 'copy-btn icon-btn', initialHtml: '📋', title: 'Copy text', onClick: (btn) => handlers.onCopy(text, btn),
            });
            contentWrapper.appendChild(copyButton);
        }

        if (handlers.onFeedback) {
            const feedbackContainer = document.createElement('div');
            feedbackContainer.className = 'feedback-container';
            const thumbUp = createButton({
                className: 'feedback-btn icon-btn', initialHtml: '👍', title: 'Good response', onClick: (btn) => handlers.onFeedback(btn, 'up'),
            });
            const thumbDown = createButton({
                className: 'feedback-btn icon-btn', initialHtml: '👎', title: 'Bad response', onClick: (btn) => handlers.onFeedback(btn, 'down'),
            });
            feedbackContainer.appendChild(thumbUp);
            feedbackContainer.appendChild(thumbDown);
            contentWrapper.appendChild(feedbackContainer);
        }
    }

    messageDiv.appendChild(contentWrapper);
    DOMElements.chatBox.appendChild(messageDiv);
    scrollChatBoxToBottom();
    return messageDiv;
}

export function addRegenerateButton(messageDiv, onRegenerate) {
    const contentWrapper = messageDiv.querySelector('.message-content-wrapper');
    if (!contentWrapper) return;

    // Avoid adding if one already exists
    if (contentWrapper.querySelector('.regenerate-btn')) return;

    const regenerateButton = createButton({
        className: 'regenerate-btn icon-btn',
        initialHtml: '🔄',
        title: 'Regenerate response',
        onClick: (btn) => onRegenerate(messageDiv, btn),
    });
    contentWrapper.appendChild(regenerateButton);
}

export function removeRegenerateButton(messageDiv) {
    const button = messageDiv?.querySelector('.regenerate-btn');
    if (button) button.remove();
}