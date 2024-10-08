import cv2
import pickle

width, height = 86, 170

try:
    with open('.\img\CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

#Mouse Draw Event
def mouseDraw(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

while True:
    # Import img
    img = cv2.imread('.\img\CarParkingTest.jpg')
    img = cv2.resize(img, (1280, 720))
    #Draw Rectangle
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 3)
    #Show img
    cv2.imshow("image", img)
    cv2.setMouseCallback("image", mouseDraw)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


