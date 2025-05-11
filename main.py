import os
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse

from utils.frames import get_frame, computer_vector, computer_vector_from_path
from utils.vector import setup_collection, insert_points, search_points
from qdrant_client import QdrantClient


from pydantic import BaseModel
from typing import List


app = FastAPI()
FRAME_PATH = 'files'

if not os.path.exists(FRAME_PATH):
    os.makedirs(FRAME_PATH)

@app.post("/upload_video/")
async def upload_video(file: UploadFile = File(...), collection_name: str = "test", host: str = Form("http://localhost:6333")):
    print(f"Received file: {file.filename}")
    print(f"Collection name: {collection_name}")
    print(f"Host: {host}")
    try:
        file_location = os.path.join(FRAME_PATH, file.filename)
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        print(f"File saved at {file_location}")
        
        count_extracted_frames = get_frame(file_location)
        if count_extracted_frames == 0:
            raise HTTPException(status_code=400, detail="No frames extracted from the video.")
        print(f"Extracted {count_extracted_frames} frames from the video.")
        setup_collection(collection_name, dimensions=512)
        print(f"Collection {collection_name} is set up.")
        insert_points(FRAME_PATH, collection_name)
        print(f"Inserted {count_extracted_frames} points into the collection {collection_name}.")
        return {"message": f"Video uploaded and processed successfully. {count_extracted_frames} frames extracted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search/")
async def search(image: UploadFile = File(...), collection_name: str = "test", limit: int =Form(5), host: str = Form("http://localhost:6333")):
    print(f"Received image: {image.filename}")
    print(f"Collection name: {collection_name}")
    print(f"Limit: {limit}")
    print(f"Host: {host}")
    try:
        image_location = os.path.join(FRAME_PATH, image.filename)
        with open(image_location, "wb+") as file_object:
            file_object.write(image.file.read())
        print(f"Image saved at {image_location}")
        results = search_points(collection_name, image_location, limit, host)
        if os.path.exists(image_location):
            os.remove(image_location)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))