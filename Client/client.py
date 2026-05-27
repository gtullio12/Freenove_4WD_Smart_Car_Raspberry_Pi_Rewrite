import socket
import time
import pygame

pygame.init()
screen = pygame.display.set_mode((400,300))
pygame.display.set_caption("RC Car Controller")

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


def client_program():
    # Run locally on laptop
    host = '192.168.1.71'
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) # Disable Nagle's algorithm, that batches loads

    try:
        while True:
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if not keys[pygame.K_w] and not keys[pygame.K_s] and not keys[pygame.K_a] and not keys[pygame.K_d] and keys[pygame.K_UP] and keys[pygame.K_DOWN] and keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
                client_socket.send(STOP.encode())
            elif keys[pygame.K_UP]:
                print('sending server tilt up')
                client_socket.send(TILT_UP.encode())
            elif keys[pygame.K_DOWN]:
                client_socket.send(TILT_DOWN.encode())
            elif keys[pygame.K_LEFT]:
                client_socket.send(PAN_LEFT.encode())
            elif keys[pygame.K_RIGHT]:
                client_socket.send(PAN_RIGHT.encode())
            elif keys[pygame.K_w] and keys[pygame.K_d]:
                client_socket.send(TURN_FORWARD_RIGHT.encode())
            elif keys[pygame.K_w] and keys[pygame.K_a]:
                client_socket.send(TURN_FORWARD_LEFT.encode())
            elif keys[pygame.K_s] and keys[pygame.K_d]:
                client_socket.send(REVERSE_RIGHT.encode())
            elif keys[pygame.K_s] and keys[pygame.K_a]:
                client_socket.send(REVERSE_LEFT.encode())
            elif keys[pygame.K_a]:
                client_socket.send(REVERSE.encode())
            elif keys[pygame.K_d]:
                client_socket.send(TURN_RIGHT.encode())
            elif keys[pygame.K_w]:
                client_socket.send(MOVE_FORWARD.encode())
            elif keys[pygame.K_s]:
                client_socket.send(REVERSE.encode())

            time.sleep(0.03) # Delay for 30ms to not overwhelm server
    except KeyboardInterrupt:
        print('Exiting Program')
        client_socket.send("quit".encode())
        client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
