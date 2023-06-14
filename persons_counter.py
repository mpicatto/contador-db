import argparse
import cv2
import numpy as np
import os
import time
from datetime import datetime
from psycopg2 import extras
from utils import config as cfg
from utils.db_client import DBConnectionAdapter


#create and verify imgs folder
try:
    if not os.path.exists("./imgs"):
        os.makedirs("./imgs")
except:
    print ("Unable to create folder, check folder permissions and try again")        

#global variables
start_time = time.time()
process_start_time = 0
video=cv2.VideoCapture(cfg.input_url)
yolo = cv2.dnn.readNet("./yolov3.weights","./yolov3.cfg")

classes = []
with open("./coco.names", 'r') as f:
    classes = f.read().splitlines()

#functions
def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbose", help="Prints process results",
                    action="store_true")
    parser.add_argument("-d","--video", help="Shows video feed and clasification results on screen",
                    action="store_true")
    parser.add_argument("-s","--save", help="Save clasification images on disk",
                    action="store_true")                
    args=parser.parse_args()
    return args

def frame_to_blob(frame):
    #turns image to RGB mode and splits color bands to input to the DNN
    global process_start_time
    process_start_time = time.time() 
    blob = cv2.dnn.blobFromImage(frame,1/255,(416,416),(0,0,0), swapRB=True, crop=False)
    yolo.setInput(blob)
    output_layers(frame)

def output_layers(frame):
    #execute the object detection
    height = frame.shape[0]
    width = frame.shape[1]
    boxes=[]
    confidences=[]
    class_ids=[]
    output_layers_name = yolo.getUnconnectedOutLayersNames()
    layeroutput=yolo.forward(output_layers_name)
    
    for output in layeroutput:
        
        for detection in output:
            score = detection[5:]
            class_id = np.argmax(score)
            confidence =score[class_id]
            
            if confidence > cfg.confidence_val:
                center_x = int(detection[0]*width)
                center_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)
                x=int(center_x-w/2)
                y=int(center_y-h/2)

                boxes.append([x,y,w,h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    bounding_boxes(frame,boxes,confidences,class_ids)

def bounding_boxes(frame,boxes,confidences,class_ids):
    #filter objets and plots bounding boxes around and counts detected humans
    count = 0 
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    
    if isinstance(indexes, tuple):
        data_handling(frame,count)
        return 
    
    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0,255, size = (len(boxes),3))
    
    for i in indexes.flatten():
        
        if class_ids[i]==0:
            x,y,w,h =boxes[i]
            label = str(classes[class_ids[i]])
            confi = str(round(confidences[i], 2))
            color = colors[i]
            cv2.rectangle(frame, (x,y), (x+w,y+h), color,2)
            cv2.putText(frame,label+" "+confi, (x,y+20),font, 2, (255,255,255),2)
            count +=1    
    
    if options.video:
        cv2.imshow("Clasification",frame)
    
    data_handling(count)

def date_format():
    #creates datetime 
    timestr = time.strftime("%Y-%m-%d %H:%M:%S")
    return timestr

def time_stamp():
    timestamp = datetime.now()
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')

def data_handling(count):
    #saves image 
    date= date_format()
    time_tag = time_stamp()
    process_time=round(time.time() - process_start_time, 3)
    
    if options.verbose:
        print("[+]People counted:%s Date:%s" %(count,date))
        print('[+]frame processing time: %s sec.' %(process_time))

    if count > 0:
            with DBConnectionAdapter() as connection:
                with connection.cursor (cursor_factory=extras.NamedTupleCursor) as cursor:
                    connection.rollback()
                    cursor.execute(
                        """
                        INSERT INTO traffic
                        (id_location, timestamp, count)
                        VALUES
                        (%s,%s,%s)
                        """,
                        (cfg.id_local, time_tag, count)
                    )
                    connection.commit()     

         
#arguments parser
options = args()

#video feed capture
while True:

    check, frame=video.read()
    if options.video:
        cv2.imshow("Feed",frame)
    
    if int(round(time.time() - start_time)) >=cfg.interval:
        start_time=time.time()
        if not options.save:
            dir = './imgs'
            for file in os.scandir(dir):
                os.remove(file.path)

        frame_to_blob(frame)
        
    key=cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
if options.video:
    cv2.destroyAllWindows()
