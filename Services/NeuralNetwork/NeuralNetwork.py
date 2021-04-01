import cv2
import torch

from Services.NeuralNetwork.tool.torch_utils import do_detect
from Services.NeuralNetwork.tool.darknet2pytorch import Darknet

class NeuralNetwork:
    @staticmethod
    def isCudaAvailable() -> bool:
        return torch.cuda.is_available()

    @staticmethod
    def getAvailableCalculationDevices() -> dict:
        devices = {}
        devices["cpu"] = "CPU"

        if torch.cuda.is_available():
            for device_idx in range(torch.cuda.device_count()):
                devices["cuda:%d" % device_idx] = "GPU (%s)" % torch.cuda.get_device_name(device_idx)

        return devices

    def __init__(self, cfg_file: str, weights_file: str, threshold: float, device_id: str) -> None:
        with torch.no_grad():
            self._obj_thresh = threshold
            self._device_id = device_id

            self._model = Darknet(cfg_file)
            
            if(self._model is None):
                return

            #self._model.print_network()
            self._model.load_weights(weights_file)

            self._model = self._model.to(device_id)
            self._model.eval()

    def process(self, image_file: str):
        with torch.no_grad():
            img = cv2.imread(image_file)
            sized = cv2.resize(img, (416, 416))
            sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)

            if(img is None):
                return

            boxes = do_detect(self._model, sized, self._obj_thresh, 0.4, self._device_id)

            detections = []
            img_height, img_width = img.shape[:2]
            for box in boxes[0]:
                x1 = int(box[0] * img_width)
                y1 = int(box[1] * img_height)
                x2 = int(box[2] * img_width)
                y2 = int(box[3] * img_height)

                xywh = (x1, y1, x2-x1, y2-y1)
                conf = float(box[5])
                id = int(box[6])

                detections.append([xywh, id, conf])

            return detections
