# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 20:29:32 2020
https://medium.com/@luanaebio/detecting-people-with-yolo-and-opencv-5c1f9bc6a810
@author: Pragadeesh
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
image = plt.imread('C:/Users/Pragadeesh/Desktop/Human Detect/DSC_0013.JPG')

classes = None
with open('C:/Users/Pragadeesh/Desktop/Human Detect/yolo/coco.names', 'r') as f:
 classes = [line.strip() for line in f.readlines()]
 
 
 
net = cv2.dnn.readNet('C:/Users/Pragadeesh/Desktop/Human Detect/yolo/yolov3-spp.weights', 'C:/Users/Pragadeesh/Desktop/Human Detect/yolo/yolov3-spp.cfg')
net.setInput(cv2.dnn.blobFromImage(image, 0.00392, (416,416), (0,0,0), True, crop=False))
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
outs = net.forward(output_layers)


class_ids = []
confidences = []
boxes = []
Width = image.shape[1]
Height = image.shape[0]
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.1:
            center_x = int(detection[0] * Width)
            center_y = int(detection[1] * Height)
            w = int(detection[2] * Width)
            h = int(detection[3] * Height)
            x = center_x - w / 2
            y = center_y - h / 2
            class_ids.append(class_id)
            confidences.append(float(confidence))
            boxes.append([x, y, w, h])
            
indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.1, 0.1)
#check if is people detection
for i in indices:
    i = i[0]
    box = boxes[i]
    if class_ids[i]==0:
        label = str(classes[class_id]) 
        cv2.rectangle(image, (round(box[0]),round(box[1])), (round(box[0]+box[2]),round(box[1]+box[3])), (255, 0, 0), 8)
        cv2.putText(image, label, (round(box[0])-10,round(box[1])-10), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 6)
        
plt.figure(figsize=(20,20))        
plt.imshow(image)

