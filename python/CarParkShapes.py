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
video_index = 0  # Current video index
videos = ['Video1.mp4', 'Video2.mp4', 'Video3.mp4', 'Video4.mp4', 'Video5.mp4']

# Load previously drawn shapes, if any
def load_shapes(file_path):
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []

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
            cv2.line(img, drawn_points[-2], drawn_points[-1], (0, 255, 0), 2)

            width = distance(drawn_points[0], drawn_points[1])
            height = distance(drawn_points[1], drawn_points[2])
            shape_name = str(shape_counter)
            shape_counter += 1
            
            shapes.append({'name': shape_name, 'points': drawn_points[:-1], 'width': width, 'height': height})
            
            drawn_points = []
            click_counter = 0
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

def switch_video(cap):
    global video_index, shapes, shape_counter
    with open(f'shapes_{videos[video_index].split(".")[0]}.pkl', 'wb') as f:
        pickle.dump(shapes, f)
    
    video_index = (video_index + 1) % len(videos)
    cap.release()
    cap.open(f"./img/{videos[video_index]}")
    
    shapes = load_shapes(f'shapes_{videos[video_index].split(".")[0]}.pkl')
    shape_counter = len(shapes)
    
    cv2.waitKey(100)
    
# Main function
def main():
    global img

    cap = cv2.VideoCapture(f"./img/{videos[video_index]}")
    shapes.extend(load_shapes(f'shapes_{videos[video_index].split(".")[0]}.pkl'))
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Image", connect_points)

    while True:
        ret, frame = cap.read()
        if not ret:
            switch_video(cap)
            continue

        img = frame.copy()
        
        height, width = frame.shape[:2]
        cv2.resizeWindow("Image", width, height)

        for shape in shapes:
            points = shape['points']
            for i in range(1, len(points)):
                cv2.line(img, points[i - 1], points[i], (0, 255, 0), 2)

        for shape_number, shape in enumerate(shapes):
            draw_shape_number(img, shape_number, shape['points'])

        cv2.imshow("Image", img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            with open(f'shapes_{videos[video_index].split(".")[0]}.pkl', 'wb') as f:
                pickle.dump(shapes, f)
            break
        elif key == ord('s'):
            with open(f'shapes_{videos[video_index].split(".")[0]}.pkl', 'wb') as f:
                pickle.dump(shapes, f)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
