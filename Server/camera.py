from picamera2 import Picamera2
import time
from numpy import ndarray

camera = Picamera2()

camera.configure(camera.create_preview_configuration(
    main={"format": "RGB888"}
))

camera.start()

def get_current_frame() -> ndarray:
    return camera.capture_array("main")


