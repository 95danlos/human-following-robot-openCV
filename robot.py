import pigpio
import time


# Motor speed 0 - 255
_max_speed = 255
MAX_SPEED = _max_speed

pi = pigpio.pi()

def io_init():  

    if not pi.connected:
        exit()

    # Motors
    pi.set_mode(12, pigpio.OUTPUT) # motor1 pwm pin
    pi.set_mode(13, pigpio.OUTPUT) # motor2 pwm pin
    pi.set_mode(22, pigpio.OUTPUT) # motor1 enable pin
    pi.set_mode(23, pigpio.OUTPUT) # motor2 enable pin
    pi.set_mode(24, pigpio.OUTPUT) # motor1 direction pin
    pi.set_mode(25, pigpio.OUTPUT) # motor1 direction pin

    pi.set_PWM_frequency(12,8000) # motor1 pwm pin
    pi.set_PWM_frequency(13,8000) # motor2 pwm pin

    # Ultrasonic distance Sensor
    pi.set_mode(17, pigpio.OUTPUT) # Trig pin
    pi.set_mode(18, pigpio.INPUT)  # Echo pin
    


class Motor(object):
    MAX_SPEED = _max_speed

    def __init__(self, pwm_pin, dir_pin, en_pin):
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin
        self.en_pin = en_pin
        self.dir_value = 0

    def enable(self):
        pi.write(self.en_pin, 1)

    def disable(self):
        pi.write(self.en_pin, 0)

    def setSpeed(self, speed):
        if speed < 0:
            speed = -speed
            self.dir_value = 1
        else:
            self.dir_value = 0

        if speed > MAX_SPEED:
            speed = MAX_SPEED

        pi.write(self.dir_pin, self.dir_value)
        pi.set_PWM_dutycycle(self.pwm_pin, speed)


class Robot(object):
    MAX_SPEED = _max_speed

    def __init__(self):
        self.motor1 = Motor(12, 24, 22)
        self.motor2 = Motor(13, 25, 23)

        self.current_speed = 0
        self.speed = 150
        self.x = 50
        self.driving_forward = False
        self.driving_backward = False
        self.turning_right = False
        self.turning_left = False

        self.left_encoder_ticks = 0
        self.right_encoder_ticks = 0
        self.v_left = 0.0
        self.v_right = 0.0

        self.shutdown = False

        io_init()

    def enable(self):
        self.motor1.enable()
        self.motor2.enable()

    def disable(self):
        self.motor1.disable()
        self.motor2.disable()

    def setSpeed(self, m1_speed, m2_speed):
        self.motor1.setSpeed(m1_speed)
        self.motor2.setSpeed(m2_speed)

    def shutdown_robot(self):
        self.shutdown = True
    
    def setDefaultSpeed(self, x):
        self.speed = x

    def setTurnSpeed(self, x):
        self.x = x

    def forward(self):
        if(self.driving_backward == False):
            self.driving_forward = True
            if(self.turning_right == True):
                self.setSpeed(self.speed + self.x, self.speed - self.x)
            elif(self.turning_left == True):
                self.setSpeed(self.speed - self.x, self.speed + self.x)
            else:
                self.setSpeed(self.speed, self.speed)


    def backward(self):
        if(self.driving_forward == False):
            self.driving_backward = True
            if(self.turning_right == True):
                self.setSpeed(-self.speed - self.x, -self.speed + self.x)
            elif(self.turning_left == True):
                self.setSpeed(-self.speed + self.x, -self.speed - self.x)
            else:
                self.setSpeed(-self.speed, -self.speed)


    def right(self):
        self.turning_right = True
        self.turning_left = False
        if(self.driving_forward == True):
            self.setSpeed(self.speed + self.x, self.speed - self.x)
        elif(self.driving_backward == True):
            self.setSpeed(-self.speed - self.x, -self.speed + self.x)
        else:
            self.setSpeed(70 + self.x, -70 -self.x)

    
    def left(self):
        self.turning_left = True
        self.turning_right = False
        if(self.driving_forward == True):
            self.setSpeed(self.speed - self.x, self.speed + self.x)
        elif(self.driving_backward == True):
            self.setSpeed(-self.speed + self.x, -self.speed - self.x)
        else:
            self.setSpeed(-70 -self.x, 70 + self.x)


    def stop_driving(self):
        self.driving_forward = False
        self.driving_backward = False
        if(self.turning_right == True):
            self.setSpeed(70 + self.x, -70 -self.x)
        elif(self.turning_left == True):
            self.setSpeed(-70 -self.x, 70 + self.x)
        else:
            self.setSpeed(0, 0)


    def stop_turning(self):
        self.turning_right = False
        self.turning_left = False
        if(self.driving_forward == True):
            self.setSpeed(self.speed, self.speed)
        elif(self.driving_backward == True):
            self.setSpeed(-self.speed, -self.speed)
        else:
            self.setSpeed(0, 0)






    '''
    Sensor functions
    '''

    def distance(self):
        pi.write(17, 1)
        time.sleep(0.00001)
        pi.write(17, 0)

        StartTime = time.time()
        StopTime = time.time()
    
        while (pi.read(18) == 0):
            StartTime = time.time()
    
        while (pi.read(18) == 1):
            StopTime = time.time()
    
        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2

        return distance



robot = Robot()


