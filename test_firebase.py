import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bszone_backend.settings')
django.setup()

from core.firebase_admin import get_firestore_client

def test_connection():
    try:
        print("Attempting to connect to Firestore...")
        db = get_firestore_client()
        # Try to write a test document
        test_ref = db.collection('test_connection').document('ping')
        test_ref.set({'status': 'online', 'timestamp': firestore.SERVER_TIMESTAMP})
        print("Successfully wrote test document to 'test_connection/ping'")
        
        # Try to read it back
        doc = test_ref.get()
        if doc.exists:
            print(f"Read back test document: {doc.to_dict()}")
        
        # Cleanup
        test_ref.delete()
        print("Successfully deleted test document. Connection is FULLY functional!")
        
    except Exception as e:
        print(f"FAILED to connect to Firestore: {str(e)}")

if __name__ == "__main__":
    from firebase_admin import firestore
    test_connection()
