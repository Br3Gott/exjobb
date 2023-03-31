
import cv2 as cv
import time
from picamera2 import Picamera2 as PiCamera

from opencv.pre_processing.filter import filter_image
from opencv.pixel_observer.pixel import make_pixel

from tensorflow.tensorflow_identify import Indentify

camera = PiCamera()
camera.start()
time.sleep(1)

pixel = make_pixel(0.4, 50)

def user_prompt():
    text = ""
    while (text != 'y' and text != 'n'):
        text = input("Failed! Continue monitor? (y/n): ")
    if (text == 'n'):
        print("Exiting...")
        exit()
    else:
        print("Continuing...")

while True:
    image = camera.capture_array("main")

    binary_image = filter_image(image)

    print("====== TensorFlow Status ", time.asctime(), " =====")
    # classify with tflite model
    if (not Indentify.run(binary_image, verbose=False)):
        print("FAILED")
        user_prompt()
    else:
        print("Tensorflow passed!")

    print("====== OpenCV Status ", time.asctime(), " =========")
    if (not pixel.add(binary_image)):
        print("FAILED")
        user_prompt()
        
    pixel.print_history_fitting()
    print("=========================================================")

    time.sleep(2)
