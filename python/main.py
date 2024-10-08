import cv2
import pickle
import numpy as np
import logging
from flask import Flask, Response
from flask_socketio import SocketIO, emit
import base64

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

videos = ['Video1.mp4', 'Video4.mp4']
video_index = 0

def load_shapes(file_path):
    logging.info(f"Loading shapes from {file_path}")
    with open(file_path, 'rb') as f:
        shapes = pickle.load(f)
    logging.info(f"Loaded {len(shapes)} shapes")
    return shapes

def preprocess_image(img):
    logging.debug("Preprocessing image")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    img_threshold = cv2.adaptiveThreshold(
        img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 25, 16
    )
    img_median = cv2.medianBlur(img_threshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_median, kernel, iterations=1)
    logging.debug("Image preprocessing completed")
    return img_dilate, img_blur, img_threshold, img_median

def draw_shapes(img, shapes):
    logging.debug("Drawing shapes on image")
    for shape in shapes:
        points = shape['points']
        color = (0, 0, 255) if shape.get('count', 0) > shape['threshold'] else (0, 255, 0)
        thickness = 2
        for i in range(1, len(points)):
            cv2.line(img, points[i - 1], points[i], color, thickness)
    logging.debug("Shapes drawing completed")

def count_nonzero_pixels(img, shapes):
    logging.debug("Counting nonzero pixels for each shape")
    for shape in shapes:
        x, y, w, h = cv2.boundingRect(np.array(shape['points']))
        img_crop = img[y:y + h, x:x + w]
        count = cv2.countNonZero(img_crop)
        shape['count'] = count
    logging.debug("Nonzero pixels counting completed")

def display_count_on_image(img, shapes):
    logging.debug("Displaying counts on image")
    for shape in shapes:
        x, y, w, h = cv2.boundingRect(np.array(shape['points']))
        count = shape['count']
        text_position = (x + (w - 50) // 2, y + h + 25)
        text_color = (0, 0, 255) if count > shape['threshold'] else (0, 255, 0)
        cv2.putText(img, str(count), text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)
    logging.debug("Count display completed")

def count_free_spaces(shapes, threshold=2000):
    logging.debug("Counting free spaces")
    free_spaces = sum(1 for shape in shapes if shape.get('count', 0) < shape['threshold'])
    return free_spaces

def display_free_spaces_count(img, free_spaces):
    logging.debug("Displaying free spaces count on image")
    text = f"Free Parks: {free_spaces}"
    position = (10, 30)  
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    logging.debug("Free spaces count display completed")

def generate_frames():
    logging.info("Starting video capture")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logging.error("Error: Could not open video capture")
        return
    
    shapes = load_shapes('shapesParkMaquete.pkl')
    for shape in shapes:
        shape['threshold'] = 3000 

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    previous_free_spaces = 0
    while True:
        success, img = cap.read()
        if not success:
            logging.error("Error: Could not read frame from video capture")
            break

        logging.debug("Processing frame")
        img_dilate, img_blur, img_threshold, img_median = preprocess_image(img)

        img_with_all_shapes = img.copy()
        count_nonzero_pixels(img_dilate, shapes)
        draw_shapes(img_with_all_shapes, shapes)
        display_count_on_image(img_with_all_shapes, shapes)

        free_spaces = count_free_spaces(shapes)
            
        if free_spaces != previous_free_spaces:
            ret, buffer = cv2.imencode('.jpg', img_with_all_shapes)
            image_base64 = base64.b64encode(buffer).decode('utf-8')
            socketio.emit('free_spaces', {'free_spaces': free_spaces, 'image': image_base64})
        display_free_spaces_count(img_with_all_shapes, free_spaces)
        previous_free_spaces = free_spaces
        ret, buffer = cv2.imencode('.jpg', img_with_all_shapes)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()
    logging.info("Video capture ended")

def generate_video_frames():
    global video_index
    logging.info(f"Starting video processing for {videos[video_index]}")
    cap = cv2.VideoCapture(f"./img/{videos[video_index]}")
    shapes = load_shapes(f'shapes_{videos[video_index].split(".")[0]}.pkl')
    
    # Set the thresholds for each video
    if videos[video_index] == 'Video1.mp4':
        threshold = 1200
    elif videos[video_index] == 'Video4.mp4':
        threshold = 500
    
    for shape in shapes:
        shape['threshold'] = threshold

    previous_free_spaces = 0
    frame_counter = 0
    frame_skip = 3 

    while True:
        ret, img = cap.read()
        if not ret:
            logging.info(f"Finished processing {videos[video_index]}")
            video_index = (video_index + 1) % len(videos)
            cap.release()
            cap = cv2.VideoCapture(f"./img/{videos[video_index]}")
            shapes = load_shapes(f'shapes_{videos[video_index].split(".")[0]}.pkl')
            
            if videos[video_index] == 'Video1.mp4':
                threshold = 1250
            elif videos[video_index] == 'Video4.mp4':
                threshold = 500
                
            for shape in shapes:
                shape['threshold'] = threshold
                
            continue

        frame_counter += 1
        if frame_counter % frame_skip != 0:
            continue
        
        img = cv2.resize(img, (1280, 720))

        logging.debug("Processing video frame")
        img_dilate, img_blur, img_threshold, img_median = preprocess_image(img)

        img_with_all_shapes = img.copy()
        count_nonzero_pixels(img_dilate, shapes)
        draw_shapes(img_with_all_shapes, shapes)
        display_count_on_image(img_with_all_shapes, shapes)

        free_spaces = count_free_spaces(shapes)
            
        if free_spaces != previous_free_spaces:
            ret, buffer = cv2.imencode('.jpg', img_with_all_shapes)
            image_base64 = base64.b64encode(buffer).decode('utf-8')
            socketio.emit('free_spaces_live', {'free_spaces': free_spaces, 'image': image_base64})
        display_free_spaces_count(img_with_all_shapes, free_spaces)
        previous_free_spaces = free_spaces
        ret, buffer = cv2.imencode('.jpg', img_with_all_shapes)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()
    logging.info("Video processing ended")
    
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_ipl')
def videos_ipl():
    return Response(generate_video_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5000)
    socketio.run(app, host='0.0.0.0', port=5000)
