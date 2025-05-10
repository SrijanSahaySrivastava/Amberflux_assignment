import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse

from utils.frames import get_frame


from pydantic import BaseModel
from typing import List


app = FastAPI()
FRAME_PATH = 'files'

if not os.path.exists(FRAME_PATH):
    os.makedirs(FRAME_PATH)

@app.post("/upload_video/")
async def upload_video(file: UploadFile = File(...)):
    try:
        # Save the uploaded video file
        file_location = os.path.join(FRAME_PATH, file.filename)
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        
        count_extracted_frames = get_frame(file_location)
        
        
        
        return {"file_path": file_location}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}