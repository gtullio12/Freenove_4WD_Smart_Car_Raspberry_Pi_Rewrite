import socket
from numpy import ndarray
import motor
import servo
import camera
import threading 

MOVE_FORWARD = 'move_forward'
MOVE_BACKWARD = 'move_backward'
TURN_RIGHT = 'turn_right'
TURN_LEFT = 'turn_left'
REVERSE = 'reverse'
TURN_FORWARD_RIGHT = 'turn_forward_right'
TURN_FORWARD_LEFT = 'turn_forward_left'
REVERSE_LEFT = 'reverse_left'
REVERSE_RIGHT = 'reverse_right'
STOP = 'stop'
TILT_UP = 'tilt_up'
TILT_DOWN = 'tilt_down'
PAN_LEFT = 'pan_LEFT'
PAN_RIGHT = 'pan_RIGHT'

servo_angle_adjust = 10

is_streaming = True 

key_press_socket = socket.socket()
key_press_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
key_press_socket.bind(('',5000))

streaming_socket = socket.socket()  # get instance
streaming_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
streaming_socket.bind(('', 5001))  # bind host address and port together

# configure how many client the server can listen simultaneously
streaming_socket.listen(1)
key_press_socket.listen(1)
key_press_conn, key_press_address = key_press_socket.accept()  # accept new connection
streaming_conn, streaming_address = streaming_socket.accept()  # accept new connection

def key_presses():
    print('starting key presses thread')

    # Set servo to default
    servo.reset_servos()

    try:
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = key_press_conn.recv(1024).decode()
            if not data:
                # if data is not received break
                break
            elif str(data) == PAN_LEFT:
                servo.set_pan_servo_pwm(servo_angle_adjust)
            elif str(data) == PAN_RIGHT:
                servo.set_pan_servo_pwm(-servo_angle_adjust)
            elif str(data) == TILT_UP:
                servo.set_tilt_servo_pwm(servo_angle_adjust)
            elif str(data) == TILT_DOWN:
                servo.set_tilt_servo_pwm(-servo_angle_adjust)
            elif str(data) == MOVE_FORWARD:
                motor.move_forward()
            elif str(data) == REVERSE: 
                motor.move_backward()
            elif str(data) == TURN_LEFT:
                motor.rotate_left()
            elif str(data) == TURN_RIGHT:
                motor.rotate_right()
            elif str(data) == TURN_FORWARD_RIGHT:
                motor.move_forward_right()
            elif str(data) == TURN_FORWARD_LEFT:
                motor.move_forward_left()
            elif str(data) == REVERSE_RIGHT:
                motor.move_reverse_right()
            elif str(data) == REVERSE_LEFT:
                motor.move_reverse_left()
            elif str(data) == STOP:
                motor.stop_motors()
            elif str(data) == 'quit':
                print('Shutting down motors')
                motor.stop_motors()
                break
    except socket.timeout:
        print('Timeout - stopping motors')
        motor.stop_motors()

    global is_streaming
    is_streaming = False
    key_press_socket.close()  # close the connection

    servo.reset_servos()

def streaming():
    while is_streaming:
        print('in server, getting current frame')
        frame = camera.get_current_frame()
        data = frame.tobytes()
        size = len(data)
        streaming_conn.sendall(size.to_bytes(4, 'big'))
        streaming_conn.sendall(data)
    print('is_streaming: ', is_streaming)

key_presses_thread = threading.Thread(target=key_presses)
key_presses_thread.start()

streaming_thread = threading.Thread(target=streaming)
streaming_thread.start()
