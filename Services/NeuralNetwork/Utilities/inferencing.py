import torch

from .constants import *

from .preprocessing import preprocess_image_eval
from .detections import detections_best_class, extract_detections, correct_detections
from .nms import run_nms

# KEEP
def inference(model, input_tensor, obj_thresh):
    """
    ----------
    Author: Damon Gwinn (gwinndr)
    ----------
    - Runs yolo model and extracts detections
    - Input should be a tensor of the form: (BATCH, N_CHANNEL, H_DIM, W_DIM)
    - Returned detections are relative to the input tensor (see correct_detections in Services.NeuralNetwork.Utilities.detections)
    ----------
    """

    model.eval()
    with torch.no_grad():
        # Running the model
        predictions = model(input_tensor)

        # Extracting detections from predictions
        detections = extract_detections(predictions, obj_thresh)

    return detections


# KEEP
def inference_on_image(model, image, network_dim, obj_thresh):
    """
    ----------
    Author: Damon Gwinn (gwinndr)
    ----------
    - Similar to inference except takes in an image as input (simpler to use)
    - Performs all needed pre and post processing
    - Returned detections are relative to the input image
    - show_img will show the augmented input image
    ----------
    """

    # Preprocessing
    input_tensor, img_info = preprocess_image_eval(image, network_dim)
    input_tensor = input_tensor.unsqueeze(0) # batch dim

    detections = inference(model, input_tensor, obj_thresh)[0]

    # Postprocessing
    detections = run_nms(detections, model, obj_thresh)
    detections = correct_detections(detections, img_info)


    # Grabbing bboxes and the classes with the best confidence
    bboxes = detections[..., DETECTION_X1:DETECTION_Y2+1]
    class_confs, classes = detections_best_class(detections)

    # Sort by confidence (better bbox color stability on videos)
    _, indices = torch.sort(class_confs, dim=0, descending=True)
    bboxes = bboxes[indices].cpu().numpy()
    classes = classes[indices].cpu().type(torch.int32).numpy()
    class_confs = class_confs[indices].cpu().numpy()

    processed = []

    # Drawing each detection on the image
    for i in range(len(detections)):
        bbox = bboxes[i]
        class_conf = class_confs[i]

        # Rounding bbox
        x1 = int(round(bbox[BBOX_X1]))
        y1 = int(round(bbox[BBOX_Y1]))
        x2 = int(round(bbox[BBOX_X2]))
        y2 = int(round(bbox[BBOX_Y2]))
        bbox = (x1, y1, x2 - x1, y2 - y1)

        det = [
            bbox,
            classes[i],
            class_conf
        ]

        processed.append(det)

    return processed

