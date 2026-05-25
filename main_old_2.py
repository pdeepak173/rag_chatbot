from fastapi import FastAPI, UploadFile, File
import shutil
import os
import numpy as np
import pickle

from loaders import load_docs
from chunking import split_docs
from embeddings import create_embeddings
from retrieval import create_vectorstore, load_vectorstore, save_vectorstore 

app = FastAPI()

UPLOAD_DIR = 'uploads'
VECTOR_DIR = 'vectorstore'

os.makedirs(UPLOAD_DIR, exist_ok = True)
os.makedirs(VECTOR_DIR, exist_ok = True)


@app.get('/')
def home():
    return {'message': 'Chatbot run successfully'}

@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    
    # SAVE FILE
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    # LOAD DOCUMENT
    documents = load_docs(file_path)

    # CHUNKING
    chunks = split_docs(documents)

    # EXTRACT TEXTS
    chunk_texts = [i.page_content for i in chunks]

    # CREATE EMBEDDINGS
    embeddings = create_embeddings(chunk_texts)

    # CREATE VECTORSTORE
    index = create_vectorstore(np.array(embeddings))

    # SAVE VECTORSTORE
    faiss_path = os.path.join(VECTOR_DIR, 'faiss_index.index')
    save_vectorstore(index, faiss_path)

    # SAVE CHUNKS
    with open(os.path.join(VECTOR_DIR, 'chunks.pk1'), 'wb') as f:
        pickle.dump(chunk_texts, f)


    return {
        'filename': file.filename,
        'chunks': len(chunk_texts),
        'status': 'uploaded successfully'
    }
