from google.oauth2 import id_token
from google.auth.transport import requests
from ..config import settings
import logging

def verify_google_token(token: str) -> dict:
    """
    Verifies a Google ID token received from the frontend.
    Returns the user's Google profile information (email, name, picture).
    """
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        id_info = id_token.verify_oauth2_token(
            token, 
            requests.Request(), 
            settings.google_client_id
        )

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        return {
            "email": id_info["email"],
            "full_name": id_info.get("name"),
            "picture": id_info.get("picture"),
            "google_id": id_info["sub"],
            "email_verified": id_info.get("email_verified", False)
        }
    except ValueError as e:
        # Invalid token
        logging.error(f"Google token verification failed: {e}")
        return {}
    except Exception as e:
        logging.error(f"Unexpected error during Google token verification: {e}")
        return {}
