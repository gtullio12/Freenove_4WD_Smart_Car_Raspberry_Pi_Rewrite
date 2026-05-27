from pca9685 import PCA9685

pca = PCA9685()

def move_backward():
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

def move_forward():
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
    pca.set_motor_pwm(0,4000)
    pca.set_motor_pwm(1,0)

    # Left rear
    pca.set_motor_pwm(3,4000)
    pca.set_motor_pwm(2,0)

    # Right upper
    pca.set_motor_pwm(6,0)
    pca.set_motor_pwm(7,0)

    # Right lower
    pca.set_motor_pwm(4,0)
    pca.set_motor_pwm(5,0)

def move_forward_left():
    # Left upper wheel
    pca.set_motor_pwm(0,0)
    pca.set_motor_pwm(1,0)

    # Left rear
    pca.set_motor_pwm(3,0)
    pca.set_motor_pwm(2,0)

    # Right upper
    pca.set_motor_pwm(6,4000)
    pca.set_motor_pwm(7,0)

    # Right lower
    pca.set_motor_pwm(4,4000)
    pca.set_motor_pwm(5,0)

def move_reverse_right():
    # Left upper wheel
    pca.set_motor_pwm(0,0)
    pca.set_motor_pwm(1,4000)

    # Left rear
    pca.set_motor_pwm(3,0)
    pca.set_motor_pwm(2,4000)

    # Right upper
    pca.set_motor_pwm(6,0)
    pca.set_motor_pwm(7,0)

    # Right lower
    pca.set_motor_pwm(4,0)
    pca.set_motor_pwm(5,0)

def move_reverse_left():
    # Left upper wheel
    pca.set_motor_pwm(0,0)
    pca.set_motor_pwm(1,0)

    # Left rear
    pca.set_motor_pwm(3,0)
    pca.set_motor_pwm(2,0)

    # Right upper
    pca.set_motor_pwm(6,0)
    pca.set_motor_pwm(7,4000)

    # Right lower
    pca.set_motor_pwm(4,0)
    pca.set_motor_pwm(5,4000)

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
    

