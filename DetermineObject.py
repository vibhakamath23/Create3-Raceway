from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
from picamera2 import Picamera2
from libcamera import controls
import time

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = Picamera2()
camera.set_controls({"AfMode": controls.AfModeEnum.Continuous}) # sets auto focus mode
camera.resolution = (224, 224)  # Set the resolution as needed
#camera.framerate = 10  # Set the framerate as needed
#raw_capture = PiRGBArray(camera, size=camera.resolution)

camera.start() # activates camera

time.sleep(1) # wait to give camera time to start up

def ObjectAndLevel():
    # Grab the webcamera's image.
    image = camera.capture_array("main")
    #camera.start_preview()
    #cv2.imshow('img',image)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Convert BGR to RGB
    # Assuming image has shape (height, width, channels)
    
    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Show the image in a window
    cv2.imshow("Webcam Image", image)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    #print("reshaped")

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    return(class_name[2:], str(np.round(confidence_score * 100))[:-2])
    
    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    camera.stop()
    cv2.destroyAllWindows()
