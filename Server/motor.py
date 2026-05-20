from pca9685 import PCA9685
import time

pca = PCA9685()

def move_forward():
    # Move left upper wheel first
    pca.set_motor_pwm(0,0)
    pca.set_motor_pwm(1,2000)

    # Move right upper wheel
    pca.set_motor_pwm(6,0)
    pca.set_motor_pwm(7,2000)

    # Move left rear wheel
    pca.set_motor_pwm(3,0)
    pca.set_motor_pwm(2,2000)

    # Move right rear wheel
    pca.set_motor_pwm(4,0)
    pca.set_motor_pwm(5,2000)

def move_backward():
    pca.set_motor_pwm(0,2000)
    pca.set_motor_pwm(1,0)

    # Move right upper wheel
    pca.set_motor_pwm(6,2000)
    pca.set_motor_pwm(7,0)

    # Move left rear wheel
    pca.set_motor_pwm(3,2000)
    pca.set_motor_pwm(2,0)

    # Move right rear wheel
    pca.set_motor_pwm(4,2000)
    pca.set_motor_pwm(5,0)

def rotate_right():
    # Left upper wheel
    pca.set_motor_pwm(0,2000)
    pca.set_motor_pwm(1,-2000)

    # Left rear
    pca.set_motor_pwm(3,2000)
    pca.set_motor_pwm(2,-2000)

    # Right upper
    pca.set_motor_pwm(6,2000)
    pca.set_motor_pwm(7,2000)

    # Right lower
    pca.set_motor_pwm(4,2000)
    pca.set_motor_pwm(5,2000)

def rotate_left():
    pca.set_motor_pwm(0,2000)
    pca.set_motor_pwm(1,2000)

    # Left rear
    pca.set_motor_pwm(3,2000)
    pca.set_motor_pwm(2,2000)

    # Right upper
    pca.set_motor_pwm(6,2000)
    pca.set_motor_pwm(7,-2000)

    # Right lower
    pca.set_motor_pwm(4,2000)
    pca.set_motor_pwm(5,-2000)

def move_forward_right():
    # Left upper wheel
    pca.set_motor_pwm(0,0)
    pca.set_motor_pwm(1,1000)

    # Left rear
    pca.set_motor_pwm(3,0)
    pca.set_motor_pwm(2,1000)

    # Right upper
    pca.set_motor_pwm(6,0)
    pca.set_motor_pwm(7,3000)

    # Right lower
    pca.set_motor_pwm(4,0)
    pca.set_motor_pwm(5,3000)

def move_forward_left():
    # Left upper wheel
    pca.set_motor_pwm(0,0)
    pca.set_motor_pwm(1,3000)

    # Left rear
    pca.set_motor_pwm(3,0)
    pca.set_motor_pwm(2,3000)

    # Right upper
    pca.set_motor_pwm(6,0)
    pca.set_motor_pwm(7,1000)

    # Right lower
    pca.set_motor_pwm(4,0)
    pca.set_motor_pwm(5,1000)

def move_reverse_right():
    # Left upper wheel
    pca.set_motor_pwm(0,1000)
    pca.set_motor_pwm(1,0)

    # Left rear
    pca.set_motor_pwm(3,1000)
    pca.set_motor_pwm(2,0)

    # Right upper
    pca.set_motor_pwm(6,3000)
    pca.set_motor_pwm(7,0)

    # Right lower
    pca.set_motor_pwm(4,3000)
    pca.set_motor_pwm(5,0)

def move_reverse_left():
    # Left upper wheel
    pca.set_motor_pwm(0,3000)
    pca.set_motor_pwm(1,0)

    # Left rear
    pca.set_motor_pwm(3,3000)
    pca.set_motor_pwm(2,0)

    # Right upper
    pca.set_motor_pwm(6,1000)
    pca.set_motor_pwm(7,0)

    # Right lower
    pca.set_motor_pwm(4,1000)
    pca.set_motor_pwm(5,0)


def stop_motors():
    pca.set_motor_pwm(0,4095)
    pca.set_motor_pwm(1,4095)

    # Move right upper wheel
    pca.set_motor_pwm(6,4095)
    pca.set_motor_pwm(7,4095)

    # Move left rear wheel
    pca.set_motor_pwm(3,4095)
    pca.set_motor_pwm(2,4095)

    # Move right rear wheel
    pca.set_motor_pwm(4,4095)
    pca.set_motor_pwm(5,4095)
    

