import os
import firebase_admin
from firebase_admin import credentials, firestore, auth
from django.conf import settings

def get_firebase_app():
    try:
        return firebase_admin.get_app()
    except ValueError:
        cert_path = os.path.join(settings.BASE_DIR, 'serviceAccountKey.json')
        if not os.path.exists(cert_path):
            raise FileNotFoundError(f"Firebase service account key not found at {cert_path}")
        
        cred = credentials.Certificate(cert_path)
        return firebase_admin.initialize_app(cred)

def get_firestore_client():
    get_firebase_app()
    return firestore.client()

def get_auth_client():
    get_firebase_app()
    return auth
