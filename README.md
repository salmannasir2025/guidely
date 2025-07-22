# Guidely: AI Tutor & Assistant

Guidely is a sophisticated, multilingual AI-powered tutor and assistant designed to provide educational support tailored to the regions of Pakistan. It leverages a modern tech stack to deliver a responsive, secure, and feature-rich experience.

The backend for this application is now deployed on **[Fly.io](https://fly.io/)** and is configured for continuous deployment using GitHub Actions.

## ✨ Features

- **Secure User Authentication**: JWT-based registration and login system with strong password hashing.
- **Conversational AI Core**: A powerful core that can function as both a "tutor" and a general "assistant".
- **Retrieval-Augmented Generation (RAG)**: Enhances LLM responses with real-time context from web searches for up-to-date and accurate answers.
- **Specialized Tools**:
    - **Math Solver**: Integrates Sympy for accurate mathematical problem-solving.
    - **Web Search**: Uses SerpApi to gather relevant information for a wide range of topics.
- **Multilingual Capabilities**:
    - **Text-to-Speech**: Converts text into natural-sounding speech for supported languages (English, Urdu).
    - **Speech-to-Text**: Transcribes user audio into text.
    - **Translation**: Translates text between English and regional languages like Urdu, Pashto, and Sindhi.
- **Image-to-Text (OCR)**: Extracts text from images using Google Cloud Vision.
- **Persistent Chat History**: Saves user interactions to a MongoDB database for session continuity.
- **Robust & Scalable Architecture**:
    - Built with **FastAPI** for high-performance, asynchronous request handling.
    - **Rate Limiting** to prevent abuse and ensure service stability.
    - **Redis Caching** for expensive operations like LLM calls and web searches to improve performance and reduce costs.

## 🛠️ Tech Stack

- **Backend:** FastAPI, Uvicorn
- **Database:** MongoDB Atlas
- **Cache:** Redis
- **Core AI Services:**
  - **LLM:** Google Gemini
  - **Speech-to-Text:** Google Cloud Speech-to-Text
  - **Text-to-Speech:** Google Cloud Text-to-Speech
  - **OCR:** Google Cloud Vision
  - **Web Search:** SerpAPI
- **Frontend:** Vanilla HTML, CSS, and JavaScript (ESM)
- **Deployment:** Fly.io, Docker, GitHub Actions



## Local Development Setup

Follow these instructions to set up and run the project on your local machine for development and testing.

### Prerequisites

- Git
- Python 3.11+
- Docker Desktop (recommended)
- Access to a MongoDB Atlas cluster, Redis instance, and the required Google Cloud APIs.

### 1. Clone the Repository

git clone https://github.com/salmannasir2025/guidely.git
cd guidely

### 2. Backend Setup
The backend is a FastAPI application located in the api/ directory.
Step A: Create and Activate Virtual Environment

### Navigate into the API directory
cd api

### Create a virtual environment
python -m venv .venv

### Activate the environment
### On Windows (PowerShell):
.\\.venv\\Scripts\\Activate.ps1

### On macOS/Linux:
source .venv/bin/activate
Step B: Install Dependencies

### Ensure your virtual environment is active
pip install -r requirements.txt

### Step C: Configure Environment Variables
The application requires API keys and connection strings to run. These are managed via a .env file for local development.
Create a file named .env inside the api/ directory.
Copy the contents of api/.env.example into your new api/.env file.
Fill in the actual values for each variable.

### Required Variables:

Variable	Description
GEMINI_API_KEY	Your API key for the Google Gemini LLM.
SERPAPI_API_KEY	Your API key for the SerpAPI web search.
MONGO_URI	The full connection string for your MongoDB.
REDIS_URL	The connection URL for your Redis instance.
FRONTEND_URL	The local URL of the frontend (e.g., http://127.0.0.1:5500) for CORS.
Note: The .env file is listed in .gitignore and will never be committed to the repository.

### Step D: Run the Backend Server
### From the 'api/' directory with the virtual environment active:
uvicorn index:app --reload
The API will be available at http://127.0.0.1:8000. You can view the interactive documentation at http://127.0.0.1:8000/docs.

### 3. Frontend Setup
With the backend running, you can now launch the vanilla JS frontend.
Open with a Live Server:
The easiest way to run the frontend is with a live server extension (like "Live Server" in VS Code).
Right-click the frontend/index.html file and choose "Open with Live Server". This handles CORS issues automatically.

### Open Directly:
Alternatively, navigate to the frontend directory in your file explorer.
Open the index.html file directly in a modern web browser.
The application should now be fully functional on your local machine.

## ☁️ Deployment

This application is configured for continuous deployment to **Fly.io**. Any push to the `main` branch will automatically trigger the deployment workflow defined in `.github/workflows/fly-deploy.yml`.

### License and Usage
Guidely: AI Tutor & Assistant is currently under development and is made publicly available for reference and educational purposes. The project is not open-source under traditional licenses.
you must obtain written consent from the copyright holder before engaging in any distribution or reproduction of the project's code or any of its parts. Unauthorized commercial use, distribution, and reproduction are strictly prohibited.
For inquiries regarding the use of this project, please contact the project maintainer directly.
Disclaimer: A proper license will be provided at a later date. Until then, please respect the terms mentioned.
