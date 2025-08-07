// Centralized configuration for the frontend application.

const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

// Use the local backend for local development, and the deployed backend URL for production.
const PROD_BACKEND_URL = 'https://guidely-api.fly.dev';
const LOCAL_BACKEND_URL = 'http://127.0.0.1:8000';

export const BACKEND_URL = isLocal ? LOCAL_BACKEND_URL : PROD_BACKEND_URL;

// Debug logging
console.log('Frontend Environment:', {
    hostname: window.location.hostname,
    isLocal: isLocal,
    backendUrl: isLocal ? LOCAL_BACKEND_URL : PROD_BACKEND_URL
});