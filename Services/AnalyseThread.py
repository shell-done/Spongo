# This Python file uses the following encoding: utf-8

import cv2
import numpy as np
from PyQt5.QtCore import (QThread, Qt, pyqtSignal, QMutex)

class AnalyseThread(QThread):
    analyseThreadSignal = pyqtSignal(str, int, dict)

    def __init__(self):
        super(QThread, self).__init__()
        self.mutex = QMutex()
        self.__abort = False

    def start(self, path, images):
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
        # Load names of classes
        classesFile = "data/parameters/classes.names"
        #classes = ["a", "b", "c", "d", "e"]
        with open(classesFile, 'rt') as f:
            classes = f.read().rstrip('\n').split('\n')

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

        colors = [
            [76, 177, 34],
            [164, 73, 163],
            [155, 105, 0],
            [0, 0, 230],
            [0, 168, 217],
            [100, 0, 0]
        ]

        progress = 0
        
        for image in self.__images:
            if self.__abort:
                return

            sponges = {}
            for i in range(len(classes)):
                sponges[classes[i]] = 0

            # Load image
            img = cv2.imread(self.__path + "/" + image)
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
            
            # Use NMS function in opencv to perform Non-maximum Suppression
            # Give it score threshold and NMS threshold as arguments.
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.3)
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = "%s : %.2f" % (classes[class_ids[i]], confidences[i])

                    sponges[classes[class_ids[i]]] += 1

                    color = colors[class_ids[i]]
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)

                    cv2.rectangle(img, (x, y), (x + w, y + h), color, 6)
                    cv2.rectangle(img, (x - 3, y - labelSize[1] - 20), (x + labelSize[0], y), color, -1)
                    cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                

            progress += 1

            if self.__abort:
                return

            if(len(boxes) != 0):
                deb = cv2.imwrite("data/predictions/" + image, img)
                self.analyseThreadSignal.emit(image, progress, sponges)
            else:
                self.analyseThreadSignal.emit("", progress, [])
            

        print("Predictions complete on %d images, they are available in data/predictions/ folder" % len(self.__images))
