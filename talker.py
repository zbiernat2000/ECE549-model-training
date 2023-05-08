import rospy
from std_msgs.msg import String
import cv2
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
from keras.models import load_model
import numpy as np




def talker():
    model = load_model('/home/ece5489/catkin_ws/src/beginner_tutorials/scripts/finetuned2.hdf5') #Load pretrained model
    vidcap = cv2.VideoCapture(0) #turn on camera
    label_list = ['backward','forward','left','right','stop'] #list of labels
    #define publisher
    pub = rospy.Publisher('chatter', String, queue_size=1)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    #check if video open
    if vidcap.isOpened():
        while not rospy.is_shutdown():
	    #read crop and show frame
            ret, frame = vidcap.read()
            frame = frame[:255,:255]
            cv2.imshow('frame', frame)
            #model prediction
            frame = preprocess_input(frame) #preprocess frame
            frame = tf.expand_dims(frame, axis=0) #expand dim to mimic batch size
            results = model.predict(frame) #predict image
            string = label_list[np.argmax(results)] #get label of result
            rospy.loginfo(string) #print
            pub.publish(string) #publish
            rate.sleep()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
