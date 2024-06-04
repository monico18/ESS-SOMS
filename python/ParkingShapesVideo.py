import cv2
import pickle
import math

# Initialize global variables
drawing = False  # True if mouse is pressed
prev_point = None  # Previous mouse click point
click_counter = 0  # Counter for left mouse button clicks
drawn_points = []  # List to store drawn points
shapes = []  # List to store drawn shapes
shape_counter = 0  # Counter to auto-assign shape numbers

# Load previously drawn shapes, if any
def load_shapes(file_path):
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []

shapes = load_shapes('shapes_Video4.pkl')

# Function to calculate the distance between two points
def distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

# Function to draw the shape number at the center of the shape
def draw_shape_number(image, number, points):
    center_x = sum(pt[0] for pt in points) // len(points)
    center_y = sum(pt[1] for pt in points) // len(points)
    cv2.putText(image, str(number), (center_x, center_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

# Mouse callback function for drawing
def connect_points(event, x, y, flags, param):
    global drawing, prev_point, drawn_points, click_counter, shape_counter

    if event == cv2.EVENT_LBUTTONDOWN:
        if click_counter < 4:
            drawing = True
            prev_point = (x, y)
            drawn_points.append(prev_point)
            click_counter += 1
        elif click_counter == 4:
            drawn_points.append((x, y))
            drawn_points.append(drawn_points[0])  # Close the polygon
            cv2.line(param, drawn_points[-2], drawn_points[-1], (0, 255, 0), 2)

            width = distance(drawn_points[0], drawn_points[1])
            height = distance(drawn_points[1], drawn_points[2])
            shape_name = str(shape_counter)
            shape_counter += 1
            
            shapes.append({'name': shape_name, 'points': drawn_points[:-1], 'width': width, 'height': height})
            
            drawn_points = []
            click_counter = 0
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

# Main function
def main():
    global img

    # Open video file
    cap = cv2.VideoCapture('img/Video4.mp4') 
    if not cap.isOpened():
        print("Error: Could not open video")
        return
    
    cv2.namedWindow("Video")
    cv2.setMouseCallback("Video", connect_points)

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        frame = cv2.resize(frame, (1280, 720))
        
        display_img = frame.copy()

        for shape in shapes:
            points = shape['points']
            for i in range(1, len(points)):
                cv2.line(display_img, points[i - 1], points[i], (0, 255, 0), 2)

        for shape_number, shape in enumerate(shapes):
            draw_shape_number(display_img, shape_number, shape['points'])
                    
        cv2.imshow("Video", display_img)

        key = cv2.waitKey(100) & 0xFF  # Adjust delay to control the frame rate
        if key == ord('q'):
            break
        elif key == ord('s'):
            with open('shapes_Video4.pkl', 'wb') as f:
                pickle.dump(shapes, f)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
