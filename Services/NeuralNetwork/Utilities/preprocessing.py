from .constants import *
from .devices import get_device, cpu_device

from .images import image_to_tensor
from .image_info import ImageInfo
from .augmentations import image_resize

# KEEP
def preprocess_image_eval(image, target_dim, force_cpu=False):
    """
    ----------
    Author: Damon Gwinn (gwinndr)
    ----------
    - Converts a cv2 image into Darknet input format with dimensions target_dim x target_dim
    - show_img will show the augmented input image
    - force_cpu will force the return type to be on the cpu, otherwise uses the default device
    - Returns preprocessed input tensor and image info object for mapping detections back
    ----------
    """

    # Tracking image information to map detections back
    image_info = ImageInfo(image)

    if(force_cpu):
        device = cpu_device()
    else:
        device = get_device()

    input_image = image_resize(image, (target_dim, target_dim), image_info=image_info)

    # Converting to tensor
    input_tensor = image_to_tensor(input_image, device=device)

    return input_tensor, image_info