import os
import django
# from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

import random
import string
from rag.services.db import Database
from langchain_core.documents import Document

def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

db = Database.get_instance()

documents = []
for i in range(5000):
    text = generate_random_string(1000)
    document = Document(
        page_content=text,
        metadata={"meta": "data"}
    )
    documents.append(document)

db.add_documents(documents)