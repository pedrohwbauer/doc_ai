
import os

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from rag.services import index_pdf
from .models import Document

@receiver(post_save, sender=Document)
def handle_document(sender, instance, created, **kwargs):
    file_path = settings.BASE_DIR / instance.file.path    

    # Ensure the text file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"The file {file_path} does not exist. Please check the path."
        )
    
    index_pdf(str(instance.id), str(instance.file.path))