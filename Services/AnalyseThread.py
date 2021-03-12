# This Python file uses the following encoding: utf-8

import cv2
import numpy as np
from PyQt5.QtCore import (QThread, Qt, pyqtSignal, QMutex)
from PyQt5.QtGui import QPixmap

from Services.Loader import Loader
from Models.Detection import Detection
from Models.ProcessedImage import ProcessedImage

class AnalyseThread(QThread):
    imageProcessedSignal = pyqtSignal(int, ProcessedImage)

    def __init__(self):
        super(QThread, self).__init__()
        self.mutex = QMutex()
        self.__abort = False

    def start(self, path: str, images: list[str]):
        self.mutex.lock()
        self.__abort = True
        self.mutex.unlock()

        if self.isRunning:
            self.wait()

        self.__path = path
        self.__images = images
        self.__abort = False

        super().start()

    def stop(self):
        self.mutex.lock()
        self.__abort = True
        self.mutex.unlock()

    def run(self):
        # Give the configuration and weight files for the model and load the network using them.
        modelConfiguration = "data/parameters/yolov4_custom_test.cfg"
        modelWeights = "data/parameters/yolov4_custom_train_last.weights"

        # Load Yolo Network
        print("Loading Yolo...")
        net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        layer_names = net.getLayerNames()

        #Determine the output layer names from the YOLO model
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        print("Yolo loaded")
        
        for image_idx, image_name in enumerate(self.__images):
            if self.__abort:
                return

            filepath = self.__path + "/" + image_name

            # Load image
            img = cv2.imread(filepath)
            height, width, channels = img.shape

            # Preprocess image
            blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)

            # Detecting objects
            net.setInput(blob)
            outs = net.forward(output_layers)

            # Showing informations
            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
            
            detections = []

            # Use NMS function in opencv to perform Non-maximum Suppression
            # Give it score threshold and NMS threshold as arguments.
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.3)
            for i in range(len(boxes)):
                if i in indexes:
                    detections.append(Detection(boxes[i], class_ids[i], confidences[i]))

            if self.__abort:
                return

            processed_image = ProcessedImage(filepath, detections)
            self.imageProcessedSignal.emit(image_idx, processed_image)

        print("Predictions complete on %d images" % len(self.__images))
