from picamera2 import Picamera2
import time
from numpy import ndarray

camera = Picamera2()


def get_current_frame() -> ndarray:
    print('taking picture now...')
    camera.start()
    time.sleep(1)
    arr = camera.capture_array("main")
    return arr


