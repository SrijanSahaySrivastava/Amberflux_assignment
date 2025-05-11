import cv2
import os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input


model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

def get_frame(video_path):
    if not video_path.endswith('.mp4'):
        raise ValueError("The file is not a valid mp4 video.")
    
    cap = cv2.VideoCapture(video_path)

    frames_dir = os.path.join(os.path.dirname(video_path), "files/Frames")
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)
        
    archive_dir = os.path.join(os.path.dirname(video_path), "files/frame_archive")
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
        
    count = 0
    while True:
        success, image = cap.read()
        if not success:
            break
        frame_filename = f"frame{count}.jpg"
        frame_path = os.path.join(frames_dir, frame_filename)
        cv2.imwrite(frame_path, image)
        
        archive_path = os.path.join(archive_dir, frame_filename)
        cv2.imwrite(archive_path, image)
        
        count += 1

    cap.release()
    cv2.destroyAllWindows()
    
    os.remove(video_path)
    
    return count

def computer_vector(base_dir):
    img_path = os.path.join(base_dir, "Frames")
    if not os.path.exists(img_path):
        raise ValueError(f"The image directory does not exist. Please check the path at {img_path}.")
    
    img_files = sorted([f for f in os.listdir(img_path) if f.endswith('.jpg')])
    if not img_files:
        raise ValueError("No jpg files found in the image directory.")
    
    embeddings = []
    for fname in img_files:
        full_path = os.path.join(img_path, fname)
        image = load_img(full_path, target_size=(224, 224))
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = preprocess_input(image)
        embedding = model.predict(image)
        embeddings.append(embedding[0])  # embedding is already 1D now
    embeddings = np.array(embeddings)
    return embeddings

def computer_vector_from_path(image_path):
    if not os.path.exists(image_path):
        raise ValueError(f"The image path does not exist. Please check the path at {image_path}.")
    
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    embedding = model.predict(image)
    return embedding[0]  # Return the 1D array

# get_frame("Destiny_2_1322238855973175296.mp4")
# print(computer_vector("files").shape)