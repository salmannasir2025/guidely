# AI Tutor & Assistant

A multimodal AI assistant and subject tutor designed to provide comprehensive help for students and general users. The application leverages a suite of modern AI services and a robust backend architecture to deliver accurate, real-time answers across a variety of subjects.

## Key Features

- **Dual Modes:** Functions as both a general-purpose "AI Assistant" and a specialized "AI Tutor".
- **Multimodal Input:** Accepts queries via text, voice (Speech-to-Text), and images (OCR).
- **Intelligent Subject Routing:** Automatically classifies user queries (Math, Physics, Chemistry, Programming, AI, Digital Marketing, etc.) to use the best tool for the job.
- **Real-time Streaming:** LLM responses are streamed to the frontend for a responsive, real-time chat experience.
- **Accurate Math Solver:** Integrates `sympy` for precise mathematical calculations, with the LLM providing step-by-step explanations.
- **Live Web Search (RAG):** Uses Retrieval-Augmented Generation with live web search results to provide factual, up-to-date answers.
- **Full-Featured Frontend:** A clean, modern UI with features like dark mode, chat history, audio playback, file uploads, and response regeneration.
- **Production-Ready Backend:** Built with FastAPI and includes structured logging, rate limiting, health checks, and a distributed Redis cache.
- **CI/CD Automation:** Includes GitHub Actions workflows to automatically build, test, and deploy the application.

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

---

## Getting Started

Follow these instructions to set up and run the project on your local machine for development and testing.

### Prerequisites

- Git
- Python 3.11+
- Docker (for containerized setup)
- Access to a MongoDB Atlas cluster, Redis instance, and Google Cloud Platform for API keys.

### 1. Backend Setup

First, set up and run the backend server.

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/salmannasir2025/guidely.git
    cd guidely
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # Navigate to the backend directory
    cd backend

    # Create a virtual environment
    python -m venv .venv

    # Activate it
    # On Windows
    .venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    -   Copy the example `.env.example` file to a new `.env` file in the `backend` directory.
    -   Fill in the required API keys and connection strings. See `backend/.env.example` for the full list.

5.  **Run the backend server:**
    ```sh
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000` and the interactive documentation at `http://127.0.0.1:8000/docs`.

### 2. Frontend Setup

With the backend running, you can now launch the frontend.

1.  **Open the frontend file:**
    -   Navigate to the `frontend` directory in your file explorer.
    -   Open the `index.html` file directly in a modern web browser (like Chrome, Firefox, or Edge).

The application should now be fully functional on your local machine.