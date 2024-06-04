import cv2
import pickle
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        color = (0, 0, 255) if shape.get('count', 0) > 3000 else (0, 255, 0)
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
        text_color = (0, 0, 255) if count > 3000 else (0, 255, 0)
        cv2.putText(img, str(count), text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)
    logging.debug("Count display completed")

def count_free_spaces(shapes, threshold=3000):
    logging.debug("Counting free spaces")
    free_spaces = sum(1 for shape in shapes if shape.get('count', 0) < threshold)
    return free_spaces

def display_free_spaces_count(img, free_spaces):
    logging.debug("Displaying free spaces count on image")
    text = f"Free Parks: {free_spaces}"
    position = (10, 30)  # Top-left corner of the screen
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    logging.debug("Free spaces count display completed")

def main():
    logging.info("Starting main function")
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    if not cap.isOpened():
        logging.error("Error: Could not open video capture")
        return

    # Set the capture size to 1280x720
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    shapes = load_shapes('shapesParkBCD.pkl')

    while True:
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

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
        display_free_spaces_count(img_with_all_shapes, free_spaces)

        # Resize the display window to 1280x720
        cv2.namedWindow("Image with all shapes", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Image with all shapes", 1280, 720)

        cv2.namedWindow("ImageBlur", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("ImageBlur", 1280, 720)

        cv2.namedWindow("ImageThresh", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("ImageThresh", 1280, 720)

        cv2.namedWindow("ImageMedian", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("ImageMedian", 1280, 720)

        cv2.imshow("Image with all shapes", img_with_all_shapes)
        cv2.imshow("ImageBlur", img_blur)
        cv2.imshow("ImageThresh", img_threshold)
        cv2.imshow("ImageMedian", img_median)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            logging.info("Quitting program")
            break

    cap.release()
    cv2.destroyAllWindows()
    logging.info("Program terminated")

if __name__ == "__main__":
    main()
