import socket
import motor

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

def server_program():
    host = ''
    port = 5000

    server_socket = socket.socket()  # get instance

    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(1)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    conn.settimeout(0.2)
    try:
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(1024).decode()
            if not data:
                # if data is not received break
                break
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
    conn.close()  # close the connection



if __name__ == '__main__':
    server_program()
