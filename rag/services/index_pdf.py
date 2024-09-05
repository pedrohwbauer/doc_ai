import os
from .db import Database
from langchain_community.document_loaders import PyPDFLoader

def index_pdf(id, path):
    db = Database.get_instance()
    loader = PyPDFLoader(path)
    pages = loader.load_and_split()
    for page in pages:
        page.metadata['doc_id'] = id
        page.metadata['url'] = '/media/documents/' + os.path.basename(path)

    print('paaaaaaaaage')
    print(page)
    db.add_documents(pages)
