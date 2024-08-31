
import os

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Document

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)
persistent_directory = str(settings.BASE_DIR / "db" / "chroma_db")
chroma_db = Chroma(collection_name="documents", embedding_function=embeddings, persist_directory=persistent_directory)

@receiver(post_save, sender=Document)
def handle_document(sender, instance, created, **kwargs):
    file_path = settings.BASE_DIR / instance.file.path    

    # Ensure the text file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"The file {file_path} does not exist. Please check the path."
        )
    
    # Read the text content from the file
    loader = TextLoader(file_path)
    documents = loader.load()

    # Split the document into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # Add to chromadb
    chroma_db.add_documents(docs)