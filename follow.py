from robot import robot
import io
import socket
import struct
import time
import picamera


# Ip address of external machine
ip = "10.42.0.228"

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect((ip, 787))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    robot.enable()
    robot.setSpeed(0, 0)
    with picamera.PiCamera() as camera:
        camera.resolution = (400, 400)
        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview()
        time.sleep(2)
        
        # Note the start time and construct a stream to hold image data
        # temporarily (we could write it directly to connection but in this
        # case we want to find out the size of each capture first to keep
        # our protocol simple)
        start = time.time()
        stream = io.BytesIO()
        for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            # Write the length of the capture to the stream and flush to
            # ensure it actually gets sent
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
    
            # Rewind the stream and send the image data over the wire
            stream.seek(0)
            connection.write(stream.read())

            # Reset the stream for the next capture
            stream.seek(0)
            stream.truncate()

            data = client_socket.recv(1024).decode()

            test = data.split(" ")
            x = (float(test[1]))
            
            distance = robot.distance()

            turnSpeed = (x - 200)/2
            if(turnSpeed < 0):
                turnSpeed = -turnSpeed
            robot.setTurnSpeed(turnSpeed)
            robot.setDefaultSpeed(200)
            
            if(x == 0):
                robot.stop_driving()
                robot.stop_turning()

            elif(distance > 100):
                if(0 < x < 190 ):
                    robot.left()
                    robot.forward()
                elif(210 < x ):
                    robot.right()
                    robot.forward()
                else:
                    robot.stop_turning()
                    robot.forward()
            else:
                if(0 < x < 170):
                    robot.left()
                    robot.stop_driving()
                elif(230 < x):
                    robot.right()
                    robot.stop_driving()
                else:
                    robot.stop_turning()
                    robot.stop_driving()

                
        # Write a length of zero to the stream to signal we're done
        connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
    robot.setSpeed(0, 0)
    robot.disable()
    robot.shutdown_robot()



