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

- **Backend**: Python, FastAPI
- **Deployment**: Fly.io
- **CI/CD**: GitHub Actions
- **Database**: MongoDB
- **Cache**: Redis
- **LLM**: Google Gemini Pro
- **Web Search**: SerpApi
- **Cloud Services**:
    - Google Cloud Vision (OCR)
    - Google Cloud Speech-to-Text
    - Google Cloud Text-to-Speech

## 🚀 Local Setup

To run the application locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd guidely
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    Create a `.env` file inside the `api/` directory and populate it with the necessary credentials. See `api/config.py` for all required variables.

    ```env
    # api/.env
    GEMINI_API_KEY="your_gemini_api_key"
    SERPAPI_API_KEY="your_serpapi_key"
    MONGO_CONNECTION_STRING="your_mongodb_connection_string"
    REDIS_URL="your_redis_url"
    FRONTEND_URL="http://localhost:3000" # Or your frontend's local URL
    JWT_SECRET_KEY="a_very_secret_key_for_jwt"
    ```

4.  **Run the application:**
    From the root directory, run the following command:
    ```bash
    uvicorn api.index:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000` and the interactive documentation at `http://127.0.0.1:8000/docs`.

## ☁️ Deployment

This application is configured for continuous deployment to **Fly.io**. Any push to the `main` branch will automatically trigger the deployment workflow defined in `.github/workflows/fly-deploy.yml`.

---

## Disclaimer

THIS SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## License

This software and related documentation is the property of Mr. Muhammad Salman Nasir and is provided under the terms of this Custom License. By using this software, you accept the terms of this license agreement.

The above-mentioned individual grants you a non-exclusive, non-transferable license to use this software for personal and educational purposes only, subject to the following conditions:

1.  **No Distribution**: You may not distribute, sell, rent, lease, or sublicense this software to any third party without the prior written consent.
2.  **No Reverse Engineering**: You may not reverse engineer, decompile, or disassemble this software, except as permitted by law.
3.  **Attribution**: You must maintain all copyright notices and attributions on any copies of the software.
4.  **Limited Liability**: Mr. Muhammad Salman Nasir shall not be liable for any damages resulting from the use of this software.
5.  **Termination**: This license is effective until terminated. Mr. Muhammad Salman Nasir may terminate this license at any time if you fail to comply with the terms of this agreement.

You do not acquire any ownership rights to the software as a result of this license. The software is licensed, not sold. By using this software, you agree to comply with all applicable laws and regulations regarding the use of this software. For inquiries regarding the use of this software, please contact Mr. Muhammad Salman Nasir by email.

