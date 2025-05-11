import cv2
import os
import numpy as np


def simple_color_histogram(image, bins=(8, 8, 8)):
    hist = cv2.calcHist([image], [0, 1, 2], None, bins, [0, 256, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    return hist

def get_frame(video_path):
    if not video_path.endswith('.mp4'):
        raise ValueError("The file is not a valid mp4 video.")
    
    cap = cv2.VideoCapture(video_path)

    frames_dir = os.path.join(os.path.dirname(video_path), "Frames")
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)
        
    archive_dir = os.path.join(os.path.dirname(video_path), "frame_archive")
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

def computer_vector(base_dir, bins=(8,8,8)):
    img_path = os.path.join(base_dir, "Frames")
    if not os.path.exists(img_path):
        raise ValueError(f"The image directory does not exist. Please check the path at {img_path}.")
    
    img_files = sorted([f for f in os.listdir(img_path) if f.endswith('.jpg')])
    if not img_files:
        raise ValueError("No jpg files found in the image directory.")
    
    embeddings = []
    for fname in img_files:
        full_path = os.path.join(img_path, fname)
        image = cv2.imread(full_path)
        if image is None:
            continue
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        hist = simple_color_histogram(image, bins)
        embeddings.append(hist)
        # os.remove(full_path)
    embeddings = np.array(embeddings)
    
    return embeddings

def computer_vector_from_path(image_path, bins=(8,8,8)):
    if not os.path.exists(image_path):
        raise ValueError(f"The image path does not exist. Please check the path at {image_path}.")
    
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Unable to read image at {image_path}.")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hist = simple_color_histogram(image, bins)
    os.remove(image_path)
    return hist

# get_frame("Destiny_2_1322238855973175296.mp4")
# print(computer_vector("files").shape)