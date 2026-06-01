from pca9685 import PCA9685

pca9685 = PCA9685(0x40, debug=True)
pca9685.set_pwm_freq(50)

# Servo 0 -> pan
pan_channel = 8 

# Servo 1 -> tilt
tilt_channel = 9

# Create pulses for servo's to keep track of
current_pulse = {
    'pan_pulse': 1500,
    'tilt_pulse': 1500
}


def set_pan_servo_pwm(angle: int) -> None:
    pulse = current_pulse['pan_pulse'] + angle
    pca9685.set_servo_pulse(pan_channel, pulse)
    current_pulse['pan_pulse'] = pulse

def set_tilt_servo_pwm(angle: int) -> None:
    pulse = current_pulse['tilt_pulse'] + angle
    pca9685.set_servo_pulse(tilt_channel, pulse)
    current_pulse['tilt_pulse'] = pulse

def reset_servos() -> None:
    pca9685.set_servo_pulse(pan_channel, 1500)
    pca9685.set_servo_pulse(tilt_channel, 1500)


