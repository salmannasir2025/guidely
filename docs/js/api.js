import { BACKEND_URL } from './config.js';

/**
 * Handles the streaming API call to the backend.
 * @param {object} payload - The data to send to the backend.
 * @param {AbortSignal} signal - The AbortSignal to allow canceling the request.
 * @param {function} onChunk - Callback function to handle each received data chunk.
 * @param {function} onDone - Callback function when the stream is finished.
 * @param {function} onError - Callback function to handle errors.
 */
export async function askAI(payload, signal, onChunk, onDone, onError) {
    try {
                const response = await fetch(`${BACKEND_URL}/ask/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
            signal, // Pass the abort signal to fetch
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'An unknown error occurred.');
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { done, value } = await reader.read();
            if (done) {
                onDone();
                break;
            }
            const chunk = decoder.decode(value, { stream: true });
            onChunk(chunk);
        }
    } catch (error) {
        if (error.name !== 'AbortError') {
            onError(error);
        }
    }
}