# import the necessary packages
import numpy as np
import argparse
import imutils
import time
import cv2
import os
import math
# construct the argument parse and parse the arguments


#Get the average of confidences
def calculate_average(file_path):
    with open(file_path, 'r') as file:
        numbers = [float(line.strip()) for line in file]
    if len(numbers)==0:
        average="No aggressive behavior detected"
        return average
    else:
        total = sum(numbers)
        average = total / len(numbers)
        return average

def get_time():
    time=("{} minutes {} seconds ".format(int(tMinutes),tSeconds))
    return time

def is_not_number_or_float(value):
    return not isinstance(value, (float, int)) or math.isnan(value)

def write_analysis(file_path, average):
    with open(file_path, 'w') as file:
        if average==0:
            file.write('Video Analysis\n No aggressive behavior detected -.Total time : {:.2f} seconds '.format(totalTime))
        else:
            file.write('Video Analysis\n -. Average confidences :{}\n -.Total time : {} minutes {:.2f} seconds '.format(str(average),(tMinutes),(tSeconds)))


def detect_video(videoPath,session_id,filename):
   
    labelsPath=('services/backend_aggressive/yolo-config/obj.names')
    
    LABELS = open(labelsPath).read().strip().split("\n")
    # initialize a list of colors to represent each possible class label
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
                            dtype="uint8")
    # derive the paths to the YOLO weights and model configuration
    
    weightsPath=('services/backend_aggressive/yolo-config/416x416-64sdv-3-fold.weights')
    configPath=('services/backend_aggressive/yolo-config/yolov4-config.cfg')


    
    # load our YOLO object detector trained on COCO dataset (80 classes)
    # and determine only the *output* layer names that we need from YOLO
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

    # initialize the video stream, pointer to output video file, and
    # frame dimensions
    vs = cv2.VideoCapture(videoPath)
    writer = None
    (W, H) = (None, None)
    # try to determine the total number of frames in the video file
    try:
        prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
            else cv2.CAP_PROP_FRAME_COUNT
        total = int(vs.get(prop))
        print("[INFO] {} total frames in video".format(total))
    # an error occurred while trying to determine the total
    # number of frames in the video file
    except:
        print("[INFO] could not determine # of frames in video")
        print("[INFO] no approx. completion time can be provided")
        total = -1

    #Create file for analytics
    file = open('static/temp/{}_confidences.txt'.format(filename), 'w')

    # loop over frames from the video file stream 
    while True:
        # read the next frame from the file
        (grabbed, frame) = vs.read()
        # if the frame was not grabbed, then we have reached the end
        # of the stream
        if not grabbed:
            break
        # if the frame dimensions are empty, grab them
        if W is None or H is None:
            (H, W) = frame.shape[:2]

    # construct a blob from the input frame and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes
        # and associated probabilities
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                    swapRB=True, crop=False)
        net.setInput(blob)
        start = time.time()
        layerOutputs = net.forward(ln)
        end = time.time()
        # initialize our lists of detected bounding boxes, confidences,
        # and class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability)
                # of the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > 0.5: #args changed
                    # scale the bounding box coordinates back relative to
                    # the size of the image, keeping in mind that YOLO
                    # actually returns the center (x, y)-coordinates of
                    # the bounding box followed by the boxes' width and
                    # height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    # use the center (x, y)-coordinates to derive the top
                    # and and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    # update our list of bounding box coordinates,
                    # confidences, and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

                    
                    file.write('{}\n'.format(sum(confidences)/len(confidences)))
                    

    # apply non-maxima suppression to suppress weak, overlapping
        # bounding boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5,
                                0.3)
        
        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                # draw a bounding box rectangle and label on the frame
                color = [int(c) for c in COLORS[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(LABELS[classIDs[i]],
                                        confidences[i])
                sumF=+(confidences[i])
                
                cv2.putText(frame, text, (x, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
        

    # check if the video writer is None
        if writer is None:
            # initialize our video writer
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            writer = cv2.VideoWriter('static/temp/{}_yolo_output.avi'.format(session_id), fourcc, 30,
                                    (frame.shape[1], frame.shape[0]), True)
            # some information on processing single frame
            if total > 0:
                elap = (end - start)
                global totalTime;
                global tMinutes;
                global tSeconds;
                totalTime=elap*total
                tMinutes=int(totalTime)/60
                tSeconds=int(totalTime)%60
                
                print("[INFO] single frame took {:.4f} seconds".format(elap))
                print("[INFO] estimated total time to finish: {} minutes {} seconds ".format(int(tMinutes),tSeconds))
                
        # write the output frame to disk
        
        writer.write(frame)
        
    # release the file pointers
    
    print("[INFO] cleaning up...")
    file.close()
    writer.release()
    vs.release()


