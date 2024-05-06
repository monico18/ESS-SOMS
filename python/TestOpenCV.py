import cv2
import os

def open_camera():
    cap = cv2.VideoCapture(0)  # Use 0 for the default camera (usually the built-in webcam)

    if not cap.isOpened():
        print("Error: Failed to open camera.")
        return

    try:
        save_path = 'photos'
        os.makedirs(save_path, exist_ok=True)  # Create directory if it doesn't exist

        # Set the resolution to 1920x1080p
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture frame.")
            return

        # Stretch the image to fit the resolution
        stretched_frame = cv2.resize(frame, (1920, 1080))

        filename = os.path.join(save_path, 'photo.jpg')
        cv2.imwrite(filename, stretched_frame)
        print(f"Saved photo: {filename}")

    finally:
        cap.release()
        cv2.destroyAllWindows()

open_camera()
