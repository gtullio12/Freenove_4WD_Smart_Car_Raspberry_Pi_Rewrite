import socket
import time
import pygame

pygame.init()
screen = pygame.display.set_mode((400,300))
pygame.display.set_caption("RC Car Controller")


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
            if not keys[pygame.K_w] and not keys[pygame.K_s] and not keys[pygame.K_a] and not keys[pygame.K_d]:
                print('Sending stop to server')
                client_socket.send('stop'.encode())
            elif keys[pygame.K_w]:
                print('Sending w to server')
                client_socket.send('w'.encode())

            time.sleep(0.03) # Delay for 30ms to not overwhelm server
    except KeyboardInterrupt:
        print('Exiting Program')
        client_socket.send("quit".encode())
        client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()