import cv2
import os

def get_frame(video_path):
    if not video_path.endswith('.mp4'):
        raise ValueError("The file is not a valid mp4 video.")
    
    cap = cv2.VideoCapture(video_path)

    frames_dir = os.path.join(os.path.dirname(video_path), "Frames")
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)
    count = 0
    while True:
        success, image = cap.read()
        if not success:
            break
        cv2.imwrite(os.path.join(frames_dir, f"frame{count}.jpg"), image)
        count += 1

    cap.release()
    cv2.destroyAllWindows()
    
    os.remove(video_path)
    
    return count

# get_frame("files\Destiny_2_1322238855973175296.mp4")