import cv2, time
from numpy import fromfile, uint8

from PySide2.QtCore import QThread, Signal

from Models.Detection import Detection
from Models.ProcessedImage import ProcessedImage
from Models.Parameters import Parameters
from Services.NeuralNetwork.NeuralNetwork import NeuralNetwork

class AnalysisThread(QThread):
    initialized = Signal()
    imageProcessed = Signal(ProcessedImage)
    completed = Signal()

    def __init__(self):
        super().__init__()
        self._abort = False
        self._network = None

    def start(self, parameters: Parameters, images: list):
        self._abort = True

        if self.isRunning():
            self.wait()

        self._morphotypes = parameters.selectedMorphotypes().keys()
        self._threshold = parameters.threshold()
        self._device_id = parameters.deviceId()
        self._srcPath = parameters.srcFolder()
        self._destPath = parameters.destFolder()
        self._images = images
        self._abort = False

        super().start()

    def stop(self):
        self._abort = True

    def run(self):
        # Give the configuration and weight files for the model and load the network using them.
        modelConfiguration = "Resources/config/yolov4_config.cfg"
        modelWeights = "Resources/config/yolov4_weights.weights"

        self._network = NeuralNetwork(modelConfiguration, modelWeights, self._threshold, self._device_id)
        
        self.initialized.emit()

        t0 = time.time()
        for image_name in self._images:
            if self._abort:
                self._network = None
                return

            detections = []

            filepath = self._srcPath + "/" + image_name

            #img = cv2.imread(filepath)
            img = cv2.imdecode(fromfile(filepath, dtype=uint8), cv2.IMREAD_UNCHANGED)
            network_output = self._network.process(img)

            for det in network_output:
                if det[1] in self._morphotypes:
                    detections.append(Detection(det[0], det[1], det[2]))

            if self._abort:
                self._network = None
                return

            processed_image = ProcessedImage(self._srcPath, image_name, (img.shape[1], img.shape[0]), detections)
            processed_image.setLoadedImage(img)
            self.imageProcessed.emit(processed_image)

        print("Predictions completed on %d images in %.2fs" % (len(self._images), time.time() - t0))

        self._network = None
        self.completed.emit()