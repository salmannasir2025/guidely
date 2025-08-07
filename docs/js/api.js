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
        console.log('Making request to:', `${BACKEND_URL}/ask/guest`);
        console.log('Payload:', payload);
        
        const response = await fetch(`${BACKEND_URL}/ask/guest`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/x-ndjson'
            },
            body: JSON.stringify(payload),
            signal, // Pass the abort signal to fetch
        });

        console.log('Response status:', response.status);
        console.log('Response headers:', Object.fromEntries(response.headers.entries()));

        if (!response.ok) {
            let errorMessage;
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || `HTTP ${response.status}: ${response.statusText}`;
            } catch {
                errorMessage = `HTTP ${response.status}: ${response.statusText}`;
            }
            throw new Error(errorMessage);
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
        console.error('API Error:', error);
        if (error.name !== 'AbortError') {
            onError(error);
        }
    }
}

/**
 * Upload and process a file
 */
export async function uploadFile(file, uploadType) {
    if (!file) return null;

    const formData = new FormData();
    formData.append('file', file);

    try {
        console.log(`Uploading ${uploadType} to:`, `${BACKEND_URL}/files/upload`);
        
        const response = await fetch(`${BACKEND_URL}/files/upload`, {
            method: 'POST',
            body: formData,
        });

        console.log('Upload response status:', response.status);

        if (!response.ok) {
            let errorMessage;
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || `Upload failed: ${response.status}`;
            } catch {
                errorMessage = `Upload failed: ${response.status}`;
            }
            throw new Error(errorMessage);
        }

        const data = await response.json();
        return data.ocr_text || data.text || 'File processed successfully';

    } catch (error) {
        console.error(`Error uploading ${uploadType}:`, error);
        throw error;
    }
}

/**
 * Get user history
 */
export async function getUserHistory() {
    try {
        const response = await fetch(`${BACKEND_URL}/data/history`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch history: ${response.status}`);
        }

        const data = await response.json();
        return data.history || [];
    } catch (error) {
        console.error('Error fetching history:', error);
        return [];
    }
}

/**
 * Clear user history
 */
export async function clearUserHistory() {
    try {
        const response = await fetch(`${BACKEND_URL}/data/history`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            throw new Error(`Failed to clear history: ${response.status}`);
        }

        return true;
    } catch (error) {
        console.error('Error clearing history:', error);
        throw error;
    }
}