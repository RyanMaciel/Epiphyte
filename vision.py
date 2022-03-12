"""
Lots of the boilerplate code here is from: https://towardsdatascience.com/implementing-real-time-object-detection-system-using-pytorch-and-opencv-70bac41148f7
Most of the difference is the way I am grabbing the bottom position of the output bounding boxes. 
"""
import cv2
import torch
import numpy as np
from torch import hub # Hub contains other models like FasterRCNN
model = torch.hub.load( \
                      'ultralytics/yolov5', \
                      'yolov5s', \
                      pretrained=True)

"""
The function below identifies the device which is availabe to make the prediction and uses it to load and infer the frame. Once it has results it will extract the labels and cordinates(Along with scores) for each object detected in the frame.
"""
def score_frame(frame, model):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device)
    frame = [frame]
    results = model(frame)
    labels = results.xyxyn[0][:, -1].numpy()
    cord = results.xyxyn[0][:, :-1].numpy()
    return labels, cord


# Get the position of the bottom middle of the bounding box (normalized to be 0...100)
def get_footer_coords(results, frame):
    labels, cord = results
    labels = labels.astype(int)
    n = len(labels)
    x_shape, y_shape = frame.shape[1], frame.shape[0]
    for i in range(n):
        row = cord[i]
        # If score is less than 0.2 we avoid making a prediction.
        if row[4] < 0.2: 
            continue
        x1 = int(row[0]*x_shape)
        x2 = int(row[2]*x_shape)
        y2 = int(row[3]*y_shape)

        bottom_x = ((x2+x1)/2) * (100/x_shape)
        bottom_y = y2 * (100/y_shape)
        classes = model.names # Get the name of label index
        class_name = classes[labels[i]]
        
        return (bottom_x, bottom_y)
"""
The function below takes the results and the frame as input and plots boxes over all the objects which have a score higer than our threshold.
"""
def plot_boxes(results, frame):
    labels, cord = results
    labels = labels.astype(int)
    n = len(labels)
    x_shape, y_shape = frame.shape[1], frame.shape[0]
    for i in range(n):
        row = cord[i]
        # If score is less than 0.2 we avoid making a prediction.
        if row[4] < 0.2: 
            continue
        x1 = int(row[0]*x_shape)
        y1 = int(row[1]*y_shape)
        x2 = int(row[2]*x_shape)
        y2 = int(row[3]*y_shape)

        bottom_x = (x2-x1)/2
        bottom_y = y2
        bgr = (0, 255, 0) # color of the box
        classes = model.names # Get the name of label index
        label_font = cv2.FONT_HERSHEY_SIMPLEX #Font for the label.
        cv2.rectangle(frame, \
                      (x1, y1), (x2, y2), \
                       bgr, 2) #Plot the boxes
        cv2.putText(frame,\
                    classes[labels[i]], \
                    (x1, y1), \
                    label_font, 0.9, bgr, 2) #Put a label over box.
        return frame

from time import time
"""
The Function below oracestrates the entire operation and performs the real-time parsing for video stream.
"""
out_file = "test.mp4"
player = cv2.VideoCapture(0) #Get your video stream.
def capture():
    assert player.isOpened() # Make sure that their is a stream. 
    #Below code creates a new video writer object to write our
    #output stream.
    _, frame = player.read() # Read the first frame.
    results = score_frame(frame, model) # Score the Frame
    return get_footer_coords(results, frame)
  
        
if __name__ == "__main__":
  capture()
