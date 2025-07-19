# Guidely: AI Tutor & Assistant

A multimodal AI assistant and subject tutor designed to provide comprehensive help for students and general users in Pakistan and beyond. The application leverages a suite of modern AI services and a robust backend architecture to deliver accurate, real-time answers across a variety of subjects.

---

## Key Features

- **Dual Modes:** Functions as both a general-purpose "AI Assistant" and a specialized "AI Tutor".
- **Multimodal Input:** Accepts queries via text, voice (Speech-to-Text), and images (OCR).
- **Intelligent Subject Routing:** Automatically classifies user queries (Math, Physics, Chemistry, Programming, AI, Digital Marketing, etc.) to use the best tool for the job.
- **Real-time Streaming:** LLM responses are streamed to the frontend for a responsive, real-time chat experience.
- **Accurate Math Solver:** Integrates `sympy` for precise mathematical calculations, with the LLM providing step-by-step explanations.
- **Live Web Search (RAG):** Uses Retrieval-Augmented Generation with live web search results to provide factual, up-to-date answers.
- **Full-Featured Frontend:** A clean, modern UI with features like dark mode, chat history, audio playback, file uploads, and response regeneration.
- **Production-Ready Backend:** Built with FastAPI and includes structured logging, rate limiting, health checks, and a distributed Redis cache.
- **CI/CD Automation:** Includes GitHub Actions workflows to automatically build, test, and deploy the application to Google Cloud Run.

## Tech Stack

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
- **Deployment:** Docker, Google Cloud Run, GitHub Actions



## Local Development Setup

Follow these instructions to set up and run the project on your local machine for development and testing.

### Prerequisites

- Git
- Python 3.11+
- Docker Desktop (recommended)
- Google Cloud SDK (`gcloud`)
- GitHub CLI (`gh`)
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
Deployment

This project is configured for automated CI/CD using GitHub Actions and Google Cloud.
Trigger: A deployment is automatically triggered on every git push to the main branch.
Process: The .github/workflows/deploy.yml workflow performs the following steps:
Authenticates securely with Google Cloud using Workload Identity Federation.
Builds a production-ready Docker image using the multi-stage Dockerfile.
Pushes the image to Google Artifact Registry.
Deploys the new image to Google Cloud Run.

### Secret Management: All production API keys are stored securely in Google Secret Manager and are injected into the Cloud Run service at runtime. They are never stored in the source code or the container image.
API Endpoints
A few key endpoints provided by the API:
GET /health: Performs a health check on all critical dependencies (Database, Cache, LLM, etc.) and returns a status report.
POST /ask: The main endpoint for submitting user queries. It handles classification, tool routing, and streams the final answer.
GET /history/{user_id}: Retrieves the last 10 interactions for a specific user.
DELETE /history/{user_id}: Deletes all chat history for a specific user.
POST /feedback: Allows users to submit feedback on the quality of an answer.

### License and Usage
Guidely: AI Tutor & Assistant is currently under development and is made publicly available for reference and educational purposes. The project is not open-source under traditional licenses.
you must obtain written consent from the copyright holder before engaging in any distribution or reproduction of the project's code or any of its parts. Unauthorized commercial use, distribution, and reproduction are strictly prohibited.
For inquiries regarding the use of this project, please contact the project maintainer directly.
Disclaimer: A proper license will be provided at a later date. Until then, please respect the terms mentioned above.
