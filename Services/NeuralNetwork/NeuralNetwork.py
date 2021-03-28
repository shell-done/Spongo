import torch

from Services.NeuralNetwork.Utilities.configs import parse_config
from Services.NeuralNetwork.Utilities.weights import load_weights

from Services.NeuralNetwork.Utilities.devices import gpu_device_name, get_device, use_cuda
from Services.NeuralNetwork.Utilities.images import load_image
from Services.NeuralNetwork.Utilities.inferencing import inference_on_image

class NeuralNetwork:
    def __init__(self, cfg_file: str, weights_file: str, threshold: float) -> None:
        with torch.no_grad():
            self._model = parse_config(cfg_file)
            
            if(self._model is None):
                return

            self._model = self._model.to(get_device())
            self._model.eval()

            if(self._model.net_block.width != self._model.net_block.height):
                print("Error: Width and height must match in [net]")
                return

            self._network_dim = self._model.net_block.width

            print("Loading weights...")
            load_weights(self._model, weights_file)

            print("DARKNET")
            print("GPU:", gpu_device_name())
            print("Config:", cfg_file)
            print("Weights:", weights_file)
            print("Version:", self._model.version)
            print("Images seen:", self._model.imgs_seen)
            print("")
            print("Network Dim:", self._network_dim)

            self._obj_thresh = threshold

    def process(self, image_file: str):
        with torch.no_grad():
            image = load_image(image_file)
            if(image is None):
                return

            detections = inference_on_image(self._model, image, self._network_dim, self._obj_thresh)

            return detections
