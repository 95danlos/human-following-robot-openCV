import io
import socket
import struct
import cv2
import numpy as np
import time

listOfDetectedPersonFireBase = []
camFocusID = 0

# Load trained object detection model
net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 787))
server_socket.listen(0)
# Accept a single connection and make a file-like object out of it
conn = server_socket.accept()[0]
connection = conn.makefile('rb')
try:
    while True:
        listOfDetectedPersons = []
        objectID = None
        confidence = None

        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        image_stream.seek(0)
        
        data = np.fromstring(image_stream.getvalue(), dtype=np.uint8)
        frame = cv2.imdecode(data, 1)
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()
        for i in np.arange(0, detections.shape[2]):
            objectID = detections[0, 0, i, 1]
            confidence = detections[0, 0, i, 2]
            if (objectID == 15.0) & (confidence > 0.1):
                listOfDetectedPersons.append(np.asscalar(np.int16(i)))

        if (len(listOfDetectedPersons) != len(listOfDetectedPersonFireBase)):
            listOfDetectedPersonFireBase = listOfDetectedPersons

        if(len(listOfDetectedPersons) == 0):
            hei = "0.0 0.0"
            conn.send(hei.encode())

        for i in listOfDetectedPersons:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            label = "{}: {:.2f}%".format("person",confidence * 100)
            cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 255, 5), 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,5), 2)
            xMidBox = ((endX - startX) / 2)
            xPoint = startX + xMidBox
            xMove = xPoint - 50

            yMidBox = ((endY - startY) / 2)
            yPoint = startY + yMidBox
            yTest = yPoint - 50

            "x:", xPoint, "y:", yPoint, "pos:", xMove

            xx = str(xPoint)
            yy = str(yPoint)
            pos = str(xMove)

            sh = pos + " " + xx
            conn.send(sh.encode())
            break

        cv2.namedWindow('Frame',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Frame', 800,800)
        cv2.imshow("Frame",frame)
        cv2.waitKey(1)

finally:
    cv2.destroyAllWindows()
    connection.close()
    server_socket.close()


