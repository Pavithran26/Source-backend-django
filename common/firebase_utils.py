from core.firebase_admin import get_firestore_client
import logging

logger = logging.getLogger(__name__)

def sync_to_firestore(collection_name, document_id, data):
    """
    Syncs a single document to a Firestore collection.
    """
    try:
        db = get_firestore_client()
        doc_ref = db.collection(collection_name).document(str(document_id))
        doc_ref.set(data)
        logger.info(f"Successfully synced {collection_name}/{document_id} to Firestore")
    except Exception as e:
        logger.error(f"Error syncing to Firestore: {e}")

def delete_from_firestore(collection_name, document_id):
    """
    Deletes a document from a Firestore collection.
    """
    try:
        db = get_firestore_client()
        db.collection(collection_name).document(str(document_id)).delete()
        logger.info(f"Successfully deleted {collection_name}/{document_id} from Firestore")
    except Exception as e:
        logger.error(f"Error deleting from Firestore: {e}")
