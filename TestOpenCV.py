import cv2

def open_camera():
    cap = cv2.VideoCapture(0)  # Use 0 for the default camera (usually the built-in webcam)

    if not cap.isOpened():
        print("Error: Failed to open camera.")
        return

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("Error: Failed to capture frame.")
                break

            cv2.imshow('Camera', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

# Call the function to open the camera
open_camera()
