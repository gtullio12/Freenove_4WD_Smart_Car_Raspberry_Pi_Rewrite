import socket
import motor

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
            elif str(data) == 'w':
                print('server recieved: ', str(data))
                motor.move_forward()
            elif str(data) == 's':
                print('server recieved: ', str(data))
                motor.move_backward()
            elif str(data) == 'a':
                motor.rotate_left()
            elif str(data) == 'd':
                print('moving forward right')
                motor.rotate_right()
            elif str(data) == 'wd':
                motor.move_forward_right()
            elif str(data) == 'wa':
                motor.move_forward_left()
            elif str(data) == 'sd':
                motor.move_reverse_right()
            elif str(data) == 'sa':
                motor.move_reverse_left()
            elif str(data) == 'stop':
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
