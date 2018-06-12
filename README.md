# human-following-robot-openCV

Code for developing a human following robot using openCV and Raspberry pi.


## Hardware

* Raspberry pi 3 with hd camera
* Differential wheeled robot
* Ultrasonic distance sensor


## Software

* Python 2.7
* OpenCV.............
* Numpy


## Instruction

1. Install Python 2.7
2. Install Numpy with `<pip install numpy>`
3. Install opvenCV 3.4 and move the file `C:\opencv\build\python\x86\2.7\cv2.pyd` into `C:\Python27\Lib\site-packages\`
4. Clone project with `git clone https://github.com/95danlos/human-following-robot-openCV.git`
5. Change pin numbers in robot.py to mach your raspberry pi pins
6. Change the ip address in follow.py to mach your pc ip
7. Deploy robot.py and follow.py on the robot and object_detect.py on your pc
8. Run object_detect.py and then follow.py

