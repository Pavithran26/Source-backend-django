import os
import firebase_admin
from firebase_admin import credentials, firestore, auth
from django.conf import settings

def get_firebase_app():
    try:
        return firebase_admin.get_app()
    except ValueError:
        # 1. Attempt to load from the environment variable (ideal for Vercel production)
        firebase_creds_json = os.getenv("FIREBASE_CREDENTIALS")
        if firebase_creds_json:
            import json
            try:
                creds_dict = json.loads(firebase_creds_json)
                cred = credentials.Certificate(creds_dict)
                return firebase_admin.initialize_app(cred)
            except Exception as e:
                print("Failed to initialize Firebase from environment variable:", str(e))

        # 2. Fall back to local serviceAccountKey.json file (ideal for local dev)
        cert_path = os.path.join(settings.BASE_DIR, 'serviceAccountKey.json')
        if not os.path.exists(cert_path):
            raise FileNotFoundError(
                f"Firebase service account key not found at {cert_path} "
                f"and the FIREBASE_CREDENTIALS environment variable is not configured."
            )
        
        cred = credentials.Certificate(cert_path)
        return firebase_admin.initialize_app(cred)

def get_firestore_client():
    get_firebase_app()
    return firestore.client()

def get_auth_client():
    get_firebase_app()
    return auth
