import cv2
import numpy as np

from social_distance.lib.types import DetectedObject, Rectangle

PERSON_CLASS_ID = 0


class OpenCVDetector:

    def __init__(self, model_config, model_weights, conf_threshold=0.6, nms_threshold=0.4):
        super().__init__()

        net = cv2.dnn.readNetFromDarknet(model_config, model_weights)
        self._model = cv2.dnn_DetectionModel(net)
        self._model.setInputParams(scale=1 / 255, size=(416, 416), swapRB=True)

        self._conf_threshold = conf_threshold
        self._nms_threshold = nms_threshold


    def detect(self, image: np.ndarray):
        class_ids, confidences, boxes = self._model.detect(image,
                                                           confThreshold=self._conf_threshold,
                                                           nmsThreshold=self._nms_threshold)
        objects = []
        for class_id, confidence, box in zip(class_ids, confidences, boxes):
            if class_id == PERSON_CLASS_ID:
                rect = Rectangle(box[0], box[1], box[2], box[3])
                objects.append(DetectedObject(rect))
        return objects
