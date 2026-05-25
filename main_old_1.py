'''
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return {'message': 'Chatbot run successfully'}
'''

from fastapi import FastAPI, UploadFile, File
import shutil
import os

app = FastAPI()

UPLOAD_DIR = 'uploads'

os.makedirs(UPLOAD_DIR, exist_ok = True)

@app.get('/')
def home():
    return {'message': 'Chatbot run successfully'}

@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        'filename': file.filename,
        'status': 'uploaded successfully'
    }
