"""
Lots of the boilerplate code here is from: https://towardsdatascience.com/implementing-real-time-object-detection-system-using-pytorch-and-opencv-70bac41148f7
Most of the difference is the way I am grabbing the bottom position of the output bounding boxes. 
"""
import cv2
import torch
import numpy as np
from torch import hub # Hub contains other models like FasterRCNN


four_cc = cv2.VideoWriter_fourcc(*"H264") #Using MJPEG codex

from queue import Queue
from threading import Thread

def find_camera(vid_cap):
    for i in range(0, 200):
        try:   
            vid_cap.open(i)
            if vid_cap.isOpened():
                print(i)
                print("worked")
        except:
            continue

class Vision:
    def __init__(self):

        self.num_frames=0
        self.model = torch.hub.load( \
                        'ultralytics/yolov5', \
                        'yolov5s', \
                        pretrained=True)
        self.player = cv2.VideoCapture(3) # camera is 3
        #Below code creates a new video writer object to write our
        #output stream.
        self.x_shape = 1024
        self.y_shape = 576
        # self.x_shape = int(self.player.get(cv2.CAP_PROP_FRAME_WIDTH))
        # self.y_shape = int(self.player.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.out_file = "clip0.mp4"
        self.out_file_num = 0
        self.vid_writer = cv2.VideoWriter("a.mp4", four_cc, 20, \
                            (self.x_shape, self.y_shape))

        assert self.player.isOpened() # Make sure that there is a stream. 
        for i in range(0, 100):
            print(i)
            _, frame = self.player.read()
            if i>20:
                self.vid_writer.write(frame)
        self.vid_writer.release()
        # self.vid_writer = cv2.VideoWriter("a.mp4", four_cc, 20, \
        #                     (self.x_shape, self.y_shape))

    """
    The function below identifies the device which is availabe to make the prediction and uses it to load and infer the frame. Once it has results it will extract the labels and cordinates(Along with scores) for each object detected in the frame.
    """
    def score_frame(self, frame, model):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model.to(device)
        frame = [frame]
        results = model(frame)
        labels = results.xyxyn[0][:, -1].numpy()
        cord = results.xyxyn[0][:, :-1].numpy()
        return labels, cord


    # Get the position of the bottom middle of the bounding box (normalized to be 0...100)
    def get_footer_coords(self, results, frame):
        if frame is None:
            return (0, 0)
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
            classes = self.model.names # Get the name of label index
            class_name = classes[labels[i]]
            
            return (bottom_x, bottom_y)
    """
    The function below takes the results and the frame as input and plots boxes over all the objects which have a score higer than our threshold.
    """
    def plot_boxes(self, results, frame):
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
            classes = self.model.names # Get the name of label index
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
    Gets called once per frame by the server.
    """
    def capture(self):
        self.num_frames += 1
        if not self.player.isOpened():
            self.vid_writer = cv2.VideoWriter("a.mp4", four_cc, 20, \
                    (self.x_shape, self.y_shape)) 
        _, frame = self.player.read() # Read the first frame.
        if frame is None:
            return (0, 0)
        results = self.score_frame(frame, self.model) # Score the Frame
        frame = self.plot_boxes(results, frame) # Plot the boxes.
        
        if self.vid_writer.isOpened():
            self.vid_writer.write(frame) # Write the frame onto the output.
        
        if self.num_frames % 40 == 10:
            self.vid_writer.release()
            self.out_file_num += 1
            self.out_file = "clip" + str(self.out_file_num) + ".mp4"

        if self.num_frames % 40 == 39:
            self.vid_writer = cv2.VideoWriter(self.out_file, four_cc, 20, \
                            (self.x_shape, self.y_shape))

        return self.get_footer_coords(results, frame)

    if __name__ == "__main__":
     capture()
   
