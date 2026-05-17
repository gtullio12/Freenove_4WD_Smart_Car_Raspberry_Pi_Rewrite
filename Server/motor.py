from pca9685 import PCA9685
import time

def move_forward():
    pca = PCA9685()
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

    time.sleep(3)
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

