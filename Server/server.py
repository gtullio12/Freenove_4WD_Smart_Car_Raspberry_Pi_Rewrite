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
START_STREAMING = 'start_streaming'
END_STREAMING = 'end_streaming'

servo_angle_adjust = 10

is_streaming = False

host = ''
port = 5000

server_socket = socket.socket()  # get instance

server_socket.bind((host, port))  # bind host address and port together

# configure how many client the server can listen simultaneously
server_socket.listen(1)
conn, address = server_socket.accept()  # accept new connection
print("Connection from: " + str(address))

def key_presses():
    print('starting key presses thread')

    # Set servo to default
    servo.reset_servos()

    try:
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(1024).decode()
            if not data:
                # if data is not received break
                break
            elif str(data) == START_STREAMING:
                global is_streaming
                is_streaming = True
                streaming_thread = threading.Thread(target=streaming)
                streaming_thread.start()
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

    is_streaming = False
    conn.close()  # close the connection

    servo.reset_servos()

def streaming():
    print('starting streaming thread')
    while is_streaming == True:
        frame = camera.get_current_frame()
        size = len(frame)
        conn.sendall(size.to_bytes(4, 'big'))  # send size first
        conn.sendall(frame.tobytes())   # then frame


key_presses_thread = threading.Thread(target=key_presses)
key_presses_thread.start()

