import cv2
import os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array

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
        raise ValueError(f"The image file does not exist. Please check the path at {img_path}.")
    
    img = os.listdir(img_path)
    if not img:
        raise ValueError("The image directory is empty.")
    img = [f for f in img if f.endswith('.jpg')]
    if not img:
        raise ValueError("No jpg files found in the image directory.")
    res = []
    for i in img:
        image = load_img(os.path.join(img_path, i), target_size=(224, 224))
        image = img_to_array(image) / 255.0
        image = np.expand_dims(image, axis=0)
        res.append(image)
    res = np.array(res)
    
    return res

# get_frame("Destiny_2_1322238855973175296.mp4")
# print(computer_vector("files").shape)