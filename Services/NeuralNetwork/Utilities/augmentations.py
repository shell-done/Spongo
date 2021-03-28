import cv2

from .constants import *

# KEEP
def image_resize(image, target_dim, image_info=None):
    """
    ----------
    Author: Damon Gwinn (gwinndr)
    ----------
    - Resizes a cv2 image to the desired dimensions
    - target_dim should be of the form (width, height)
    - Annotations should be already normalized so image resizing does not have an effect
    - Interpolation given by CV2_INTERPOLATION in constants.py
    ----------
    """

    new_img = cv2.resize(image, target_dim, interpolation=CV2_INTERPOLATION)
    nw = new_img.shape[CV2_W_DIM]
    nh = new_img.shape[CV2_H_DIM]

    # Setting dimension information for new image
    if(image_info is not None):
        image_info.set_augmentation(new_img)
        image_info.set_embedding_dimensions(nw, nh)


    return new_img