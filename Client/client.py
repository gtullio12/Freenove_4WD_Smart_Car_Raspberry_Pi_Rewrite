import socket
from curses import wrapper
import time


def client_program(stdscr):
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    stdscr.nodelay(True) # Sets getch to non-blocking
    try:
        while True:
            c = stdscr.getch() 
            if c == -1:
                client_socket.send('stop'.encode())
            elif c == ord('w') or c == ord('s'):
                print('client is sending: ', chr(c))
                client_socket.send(chr(c).encode())  # send message
            time.sleep(0.03) # Delay for 30ms to not overwhelm server
    except KeyboardInterrupt:
        print('Exiting Program')
        client_socket.send("quit".encode())
        client_socket.close()  # close the connection

wrapper(client_program)