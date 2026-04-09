# Guidely: AI Tutor & Assistant

Guidely is a sophisticated, multilingual AI-powered tutor and assistant designed to provide educational support tailored to the regions of Pakistan. It connects users with multiple AI engines through a single, unified interface — letting each user bring their own preferred AI or use the built-in default, all with enterprise-grade security.

The backend is designed for simple local execution, ensuring it runs on legacy hardware without complex containerisation.

## ✨ Features

### 🤖 Multi-Provider AI Engine
Guidely is not locked to a single AI model. Users can connect and switch between multiple AI providers from within the app:

| Provider | Model | Free Tier |
|---|---|---|
| **Google Gemini** | gemini-pro | ✅ Built-in default |
| **OpenAI** | GPT-4 Turbo | — |
| **Minimax** | MiniMax-Text-01 | ✅ |
| **xAI Grok** | grok-beta | — |
| **Alibaba Qwen** | qwen-turbo | ✅ |

Each provider's credentials are stored using AES-128 encryption, bound to the user's identity. Switching models takes one click from the chat interface.

### 🔐 Secure Authentication
- **Google Sign-In**: One-click login/registration via Google OAuth2.
- **Email & Password**: Traditional JWT-based authentication with strong password hashing.
- **Guest Mode**: Users can chat freely without an account. A non-intrusive sign-up prompt appears after a trial period to encourage saving history.

### 🛡️ Cryptographic API Key Vault
Users who supply their own AI provider keys are protected by the built-in security vault:
- Keys are encrypted with **AES-128 (Fernet)** at rest.
- Each key is cryptographically bound to the user's unique identity — making cross-user decryption impossible even in the event of a database breach.
- Keys are never logged or stored in plain text.

### 📚 Intelligent Learning Tools
- **Retrieval-Augmented Generation (RAG)**: Real-time web search context is injected into AI responses for up-to-date accuracy.
- **Math Solver**: Integrates SymPy for accurate symbolic mathematics.
- **Query Classification**: Automatically routes questions to the most appropriate tool (math, search, or LLM).

### 🌍 Multilingual Capabilities
- **Text-to-Speech**: Natural-sounding audio in English and Urdu.
- **Speech-to-Text**: Transcribes voice notes into text queries.
- **Translation**: Supports English ↔ Urdu, Pashto, Punjabi, and Sindhi.
- **Image-to-Text (OCR)**: Extracts text from uploaded images via Google Cloud Vision.

### ⚡ Robust Architecture
- **Streaming Responses**: All AI responses stream in real time using Server-Sent Events (SSE).
- **Rate Limiting**: Protects all endpoints from abuse.
- **Smart Caching**: Redis if available, in-memory fallback for lightweight environments.
- **File Support**: Images and documents can be uploaded and processed alongside queries.
- **Persistent History**: All authenticated interactions are saved per user.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | FastAPI, Uvicorn, Python 3.9+ |
| **Database** | MongoDB (Local or Atlas) |
| **Cache** | Redis (optional) / In-Memory |
| **AI Providers** | Google Gemini, OpenAI, Minimax, xAI Grok, Alibaba Qwen |
| **Auth** | JWT + Google OAuth2 |
| **Speech** | Google Cloud Speech-to-Text / Text-to-Speech |
| **OCR** | Google Cloud Vision |
| **Web Search** | SerpAPI |
| **Frontend** | Vanilla HTML, CSS, JavaScript (ES Modules) |

---

## 🚀 Local Development Setup

### Prerequisites

- Git
- Python 3.9+
- A MongoDB instance (local `mongod` or MongoDB Atlas)
- A Google Gemini API key (required for the built-in default AI)

### 1. Clone the Repository

```bash
git clone https://github.com/salmannasir2025/guidely.git
cd guidely
```

### 2. Backend Setup

**Step A: Create and Activate a Virtual Environment**

```bash
python -m venv .venv
# macOS / Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

**Step B: Install Dependencies**

```bash
pip install -r requirements.txt
```

**Step C: Configure Environment Variables**

Create a file named `.env` inside the `api/` directory:

```env
GEMINI_API_KEY="your_gemini_key"
SERPAPI_API_KEY="your_serpapi_key"
MONGO_CONNECTION_STRING="mongodb://localhost:27017"
MONGO_DB_NAME="guidely"
JWT_SECRET_KEY="your_strong_secret"
SECRET_VAULT_KEY="your_32byte_fernet_key"   # Generate: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
GOOGLE_CLIENT_ID="your_google_oauth_client_id"
FRONTEND_URL="http://localhost:5500"
```

> **Note**: `GEMINI_API_KEY` is the only required AI key. All other provider keys (OpenAI, Minimax, Grok, Qwen) are supplied by users at runtime through the in-app Settings panel.

**Step D: Run the Backend**

```bash
python main.py
```

API available at `http://127.0.0.1:8000` · Interactive docs at `http://127.0.0.1:8000/docs`

### 3. Frontend Setup

The frontend is a static site in the `docs/` directory.

```bash
python -m http.server 5500 --directory docs
```

Open `http://localhost:5500` in your browser.

---

## 🔑 Using Your Own AI Provider Keys

1. Register or log in to Guidely.
2. Click the **⚙️ Settings** button in the chat header.
3. Select a provider (e.g., Minimax or Qwen), click **Manage**, and paste your API key.
4. Your key is encrypted instantly and stored securely. The raw key is never saved.
5. Use the **Active Model** selector to switch between providers at any time.

> **Free options**: Minimax (`minimax.io`) and Alibaba Qwen (`dashscope.aliyuncs.com`) both offer free-tier API keys with generous limits.

---

### License and Usage

Guidely is currently under active development and is made publicly available for reference and educational purposes. This project is **not** open-source under traditional licenses.

You must obtain written consent from the copyright holder before engaging in any distribution or reproduction of the project's code or any of its parts. Unauthorized commercial use, distribution, and reproduction are strictly prohibited.

For enquiries regarding the use of this project, please contact the project maintainer directly.

*A formal license will be provided at a later date. Until then, please respect the terms stated above.*
