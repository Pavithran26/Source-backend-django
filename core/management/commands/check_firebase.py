from django.core.management.base import BaseCommand
from core.firebase_admin import get_firestore_client

class Command(BaseCommand):
    help = 'Check Firebase Admin connection'

    def handle(self, *args, **options):
        try:
            db = get_firestore_client()
            # Try to list collections as a basic check
            collections = db.collections()
            self.stdout.write(self.style.SUCCESS('Successfully connected to Firebase!'))
            self.stdout.write(f'Project ID: {db._project_id}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to connect to Firebase: {str(e)}'))
