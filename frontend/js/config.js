// Centralized configuration for the frontend application.

const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

// Use the local backend for local development, and the deployed Cloud Run URL for production.
// Update this with the live URL of your backend after you deploy it to Google Cloud Run.
const PROD_BACKEND_URL = 'https://regional-aibot-backend-448688349387.us-central1.run.app'; // <-- IMPORTANT: Update this later
const LOCAL_BACKEND_URL = 'http://127.0.0.1:8000';

export const BACKEND_URL = isLocal ? LOCAL_BACKEND_URL : PROD_BACKEND_URL;