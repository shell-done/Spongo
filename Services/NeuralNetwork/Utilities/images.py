import torch
import cv2
import numpy as np

from .constants import *
from .devices import get_device, cpu_device

from .detections import detections_best_class

# KEEP
def load_image(image_file):
    """
    ----------
    Author: Damon Gwinn (gwinndr)
    ----------
    - Loads in an image from file using cv2
    - Converts from grayscale to color if applicable
    - Returns None if invalid
    ----------
    """

    image = cv2.imread(image_file)
    if(image is None):
        print("load_image: Error: Could not read image file:", image_file)
        return None

    if(image.shape[CV2_C_DIM] == 1):
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif(image.shape[CV2_C_DIM] != 3):
        print("load_image: Error: With image file:", image_file)
        print("    Expected 1 or 3 color channels, got:", image.shape[CV2_C_DIM])
        return None

    return image

# KEEP
def draw_detections(detections, image, class_names, verbose_output=False):
    """
    ----------
    Author: Damon Gwinn (gwinndr)
    ----------
    - Creates a new image with the detections shown as bounding boxes
    - verbose_output will additionally print the detections to console
    - See BBOX DRAWING section in Services.NeuralNetwork.Utilities.constants to control how bounding boxes are drawn
    ----------
    """

    image = image.copy()

    # Grabbing bboxes and the classes with the best confidence
    bboxes = detections[..., DETECTION_X1:DETECTION_Y2+1]
    class_confs, classes = detections_best_class(detections)

    # Sort by confidence (better bbox color stability on videos)
    _, indices = torch.sort(class_confs, dim=0, descending=True)
    bboxes = bboxes[indices].cpu().numpy()
    classes = classes[indices].cpu().type(torch.int32).numpy()
    class_confs = class_confs[indices].cpu().numpy()

    n_colors = len(BBOX_COLORS)

    # Drawing each detection on the image
    for i in range(len(detections)):
        bbox = bboxes[i]
        class_name = class_names[classes[i]]
        class_conf = class_confs[i]
        color = BBOX_COLORS[i % n_colors]

        # Rounding bbox
        x1 = int(round(bbox[BBOX_X1]))
        y1 = int(round(bbox[BBOX_Y1]))
        x2 = int(round(bbox[BBOX_X2]))
        y2 = int(round(bbox[BBOX_Y2]))
        bbox = (x1, y1, x2, y2)

        if(BBOX_INCLUDE_CLASS_CONF):
            label = "%s %.2f" % (class_name, class_conf)
        else:
            label = class_name

        draw_bbox_inplace(image, bbox, label, color)

        # Extended output is similar to darknet's
        if(verbose_output):
            print("Class:", class_name)
            print("Conf: %.2f" % class_conf)
            print("Left_x:", x1)
            print("Left_y:", y1)
            print("Width:", x2-x1)
            print("Height:", y2-y1)
            print("")

    return image

# KEEP
def draw_bbox_inplace(image, bbox, label, color):
    """
    ----------
    Author: Damon Gwinn (gwinndr)
    ----------
    - Draws the given bbox on the image in_place (image is not copied first)
    - bbox should be an integer list-like in the format (x1 y1 x2 y2)
    - See BBOX DRAWING in constants.py for tweaking output formatting
    - This is a helper function, recommend you use draw_detections or draw_annotations
    ----------
    """

    x1 = bbox[BBOX_X1]
    y1 = bbox[BBOX_Y1]
    x2 = bbox[BBOX_X2]
    y2 = bbox[BBOX_Y2]

    # Bbox rectangle top-left and bottom-right
    p1 = (x1, y1)
    p2 = (x2, y2)

    cv2.rectangle(image, p1, p2, color, BBOX_RECT_THICKNESS)

    # Getting the label text size
    t_dims = cv2.getTextSize(label, BBOX_FONT, BBOX_FONT_SCALE, BBOX_FONT_THICKNESS)[0]

    # Drawing a label rectangle above the bbox at the top left to make the text pop out better
    label_rect_x1 = x1
    label_rect_y1 = y1 - t_dims[CV2_TEXT_SIZE_H] - (BBOX_TEXT_TOP_PAD + BBOX_TEXT_BOT_PAD)
    label_rect_x2 = x1 + t_dims[CV2_TEXT_SIZE_W] + (BBOX_TEXT_LEFT_PAD + BBOX_TEXT_RIGHT_PAD)
    label_rect_y2 = y1

    # Label to go into the rectangle
    label_x = x1 + BBOX_TEXT_LEFT_PAD
    label_y = y1 - BBOX_TEXT_BOT_PAD

    # Will put the label below the bbox at the top left if it clips outside the image
    if(label_rect_y1 < 0):
        move_y = (y1 - label_rect_y1)

        label_rect_y1 += move_y
        label_rect_y2 += move_y
        label_y += move_y

    label_rect_p1 = (label_rect_x1, label_rect_y1)
    label_rect_p2 = (label_rect_x2, label_rect_y2)
    label_text_p = (label_x, label_y)

    # Drawing the label rectangle with the text inside
    cv2.rectangle(image, label_rect_p1, label_rect_p2, color, CV2_RECT_FILL)
    cv2.putText(image, label, label_text_p, BBOX_FONT, BBOX_FONT_SCALE, COLOR_BLACK, BBOX_FONT_THICKNESS);

    return

# KEEP
def image_to_tensor(image, device=None):
    """
    ----------
    Author: Damon Gwinn (gwinndr)
    ----------
    - Converts cv2 image into a pytorch input tensor
    - Helper function, recommended you use one of preprocess_image_eval or preprocess_image_train
    - If device is None, uses the default device (get_device)
    ----------
    """

    if(device is None):
        device = get_device()

    # rgb
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # normalize
    if(image.dtype == np.uint8):
        image = image_uint8_to_float(image)

    # then convert to tensor
    tensor = torch.from_numpy(image).to(device)
    tensor = tensor.permute(CV2_C_DIM, CV2_H_DIM, CV2_W_DIM).contiguous()

    return tensor

# KEEP
def image_uint8_to_float(image):
    """
    ----------
    Author: Damon Gwinn (gwinndr)
    ----------
    - Converts cv2 image from uint8 (0-255) to float (0-1)
    - In other words, normalizes an image
    ----------
    """

    return image.astype(np.float32) / 255.0
