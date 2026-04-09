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
        const isGuest = !localStorage.getItem('guidely_jwt_token');
        const endpoint = isGuest ? `${BACKEND_URL}/ask/guest` : `${BACKEND_URL}/ask`;
        
        console.log('Making request to:', endpoint);
        console.log('Payload:', payload);
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/x-ndjson',
                ...getAuthHeader()
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
 * Key Management Methods
 */
export async function saveProviderKey(provider, key) {
    const response = await fetch(`${BACKEND_URL}/users/me/keys/`, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            ...getAuthHeader()
        },
        body: JSON.stringify({ provider, key })
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to save API key');
    }
    return await response.json();
}

export async function listProviderKeys() {
    const response = await fetch(`${BACKEND_URL}/users/me/keys/`, {
        method: 'GET',
        headers: getAuthHeader()
    });
    if (!response.ok) throw new Error('Failed to list API keys');
    const data = await response.json();
    return data.providers || [];
}

export async function deleteProviderKey(provider) {
    const response = await fetch(`${BACKEND_URL}/users/me/keys/${provider}`, {
        method: 'DELETE',
        headers: getAuthHeader()
    });
    if (!response.ok) throw new Error('Failed to delete API key');
    return await response.json();
}

/**
 * Utils
 */
function getAuthHeader() {
    const token = localStorage.getItem('guidely_jwt_token');
    return token ? { 'Authorization': `Bearer ${token}` } : {};
}

/**
 * Auth Methods
 */
export async function register(userData) {
    const response = await fetch(`${BACKEND_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
    });
    if (!response.ok) throw new Error('Registration failed');
    return await response.json();
}

export async function login(email, password) {
    const formData = new URLSearchParams();
    formData.append('username', email); // OAuth2PasswordRequestForm expects 'username'
    formData.append('password', password);

    const response = await fetch(`${BACKEND_URL}/auth/token`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData
    });
    if (!response.ok) throw new Error('Login failed');
    const data = await response.json();
    localStorage.setItem('guidely_jwt_token', data.access_token);
    return data;
}

export async function verifyGoogleToken(idToken) {
    const response = await fetch(`${BACKEND_URL}/auth/google`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: idToken })
    });
    if (!response.ok) throw new Error('Google authentication failed');
    const data = await response.json();
    localStorage.setItem('guidely_jwt_token', data.access_token);
    return data;
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