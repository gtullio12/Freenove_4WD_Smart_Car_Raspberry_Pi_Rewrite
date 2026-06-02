import socket
import pygame
import threading
import numpy

pygame.init()
screen = pygame.display.set_mode((640,480))
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

is_streaming = True
current_frame = None


host = '192.168.1.71'
key_press_port = 5000  # socket server port number
streaming_port = 5001  # socket server port number

key_press_socket = socket.socket()  # instantiate
key_press_socket.connect((host, key_press_port))  # connect to the server
key_press_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) # Disable Nagle's algorithm, that batches loads

streaming_socket = socket.socket()  # instantiate
streaming_socket.connect((host, streaming_port))  # connect to the server
streaming_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) # Disable Nagle's algorithm, that batches loads

def client_streaming():
    global current_frame, is_streaming
    print('starting client streaming thread')
    while is_streaming:
        print('recieved stream from server')
        size_data = streaming_socket.recv(4)
        size = int.from_bytes(size_data, 'big')
        print('size recieved: ', size)
        data = b''
        while len(data) < size:
            remaining = size - len(data)
            data += streaming_socket.recv(min(4096, remaining))

        print('actual recieved: ', len(data))
        nd_frame = numpy.frombuffer(data, dtype=numpy.uint8)
        pygame_frame = nd_frame.reshape(480, 640, 3)
        current_frame = pygame_frame.swapaxes(0, 1)

client_streaming_thread = threading.Thread(target=client_streaming)
client_streaming_thread.start()

# main thread - pygame loop
try:
    while True:
        pygame.event.pump()
        keys = pygame.key.get_pressed()

        if not keys[pygame.K_w] and not keys[pygame.K_s] and not keys[pygame.K_a] and not keys[pygame.K_d] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            key_press_socket.send(STOP.encode())
        elif keys[pygame.K_UP]:
            print('sending server tilt up')
            key_press_socket.send(TILT_UP.encode())
        elif keys[pygame.K_DOWN]:
            key_press_socket.send(TILT_DOWN.encode())
        elif keys[pygame.K_LEFT]:
            key_press_socket.send(PAN_LEFT.encode())
        elif keys[pygame.K_RIGHT]:
            key_press_socket.send(PAN_RIGHT.encode())
        elif keys[pygame.K_w] and keys[pygame.K_d]:
            key_press_socket.send(TURN_FORWARD_RIGHT.encode())
        elif keys[pygame.K_w] and keys[pygame.K_a]:
            key_press_socket.send(TURN_FORWARD_LEFT.encode())
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            key_press_socket.send(REVERSE_RIGHT.encode())
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            key_press_socket.send(REVERSE_LEFT.encode())
        elif keys[pygame.K_a]:
            key_press_socket.send(REVERSE.encode())
        elif keys[pygame.K_d]:
            key_press_socket.send(TURN_RIGHT.encode())
        elif keys[pygame.K_w]:
            key_press_socket.send(MOVE_FORWARD.encode())
        elif keys[pygame.K_s]:
            key_press_socket.send(REVERSE.encode())

        if current_frame is not None:
            pygame.surfarray.blit_array(screen, current_frame)
            pygame.display.flip()

        #time.sleep(0.03)

except KeyboardInterrupt:
    print('Exiting Program')
    is_streaming = False
    key_press_socket.send('quit'.encode())
    key_press_socket.close()
    streaming_socket.send('quit'.encode())
    streaming_socket.close()
    pygame.quit()
