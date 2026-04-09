# Guidely: AI Tutor & Assistant

Guidely is a sophisticated, multilingual AI-powered tutor and assistant designed to provide educational support tailored to the regions of Pakistan. It leverages a modern tech stack to deliver a responsive, secure, and feature-rich experience.

The backend for this application is designed for simple local execution, ensuring it can run on legacy hardware without the need for complex containerization like Docker.

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
- **Persistent Chat History**: Saves user interactions to a database for session continuity.
- **Robust & Simple Architecture**:
    - Built with **FastAPI** for high-performance, asynchronous request handling.
    - **Rate Limiting** to prevent abuse and ensure service stability.
    - **Smart Caching**: Uses Redis if available, or falls back to an efficient in-memory cache for speed on slower systems.

## 🛠️ Tech Stack

- **Backend:** FastAPI, Uvicorn
- **Database:** MongoDB (Local or Atlas)
- **Cache**: In-memory (Default) or Redis (Optional)
- **Core AI Services:**
  - **LLM:** Google Gemini
  - **Speech-to-Text:** Google Cloud Speech-to-Text
  - **Text-to-Speech:** Google Cloud Text-to-Speech
  - **OCR:** Google Cloud Vision
  - **Web Search:** SerpAPI
- **Frontend:** Vanilla HTML, CSS, and JavaScript (ESM)

## 🚀 Local Development Setup

### Prerequisites

- Git
- Python 3.11+
- Access to a MongoDB instance and the required Google Cloud APIs.

### 1. Clone the Repository

```bash
git clone https://github.com/salmannasir2025/guidely.git
cd guidely
```

### 2. Backend Setup

The backend is a FastAPI application.

**Step A: Create and Activate Virtual Environment**

```bash
python -m venv .venv
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

**Step B: Install Dependencies**

```bash
pip install -r requirements.txt
```

**Step C: Configure Environment Variables**

Create a file named `.env` inside the `api/` directory (or use environment variables) with the following:

```env
GEMINI_API_KEY="your_key"
SERPAPI_API_KEY="your_key"
MONGO_CONNECTION_STRING="mongodb://localhost:27017"
MONGO_DB_NAME="guidely"
JWT_SECRET_KEY="your_secret"
FRONTEND_URL="http://localhost:5500"
```

**Step D: Run the Backend Server**

```bash
python main.py
```

The API will be available at `http://127.0.0.1:8000`. You can view the interactive documentation at `http://127.0.0.1:8000/docs`.

### 3. Frontend Setup

The frontend is located in the `docs/` directory (static site). You can run it by opening `docs/index.html` in a browser or by using a simple static file server.

```bash
# Example using Python to serve the frontend
cd docs
python -m http.server 5500
```


### License and Usage
Guidely: AI Tutor & Assistant is currently under development and is made publicly available for reference and educational purposes. The project is not open-source under traditional licenses.
you must obtain written consent from the copyright holder before engaging in any distribution or reproduction of the project's code or any of its parts. Unauthorized commercial use, distribution, and reproduction are strictly prohibited.
For inquiries regarding the use of this project, please contact the project maintainer directly.
Disclaimer: A proper license will be provided at a later date. Until then, please respect the terms mentioned.
