import cv2
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
from keras.models import load_model
import numpy as np

model = load_model('checkpoints/finetuned2.hdf5')
vidcap = cv2.VideoCapture(0)
label_list = ['backward','forward','stop','left','right']
if vidcap.isOpened():
    while(True):
        ret, frame = vidcap.read()
        frame = frame[:255,:255]
        cv2.imshow('frame', frame)
        #frame = np.expand_dims(frame,)
        #print(frame.shape)
        frame = preprocess_input(frame)
        frame = tf.expand_dims(frame, axis=0)
        results = model.predict(frame)
        print(results)
        print(label_list[np.argmax(results)])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
else:
    print("Cannot open camera")
