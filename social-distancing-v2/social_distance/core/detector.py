import cv2 as cv
import numpy as np


class OpenCVPersonDetector:

    def __init__(self, model_config_path, model_weights_path, conf_threshold=0.6, nms_threshold=0.4):
        super().__init__()

        net = cv.dnn.readNetFromDarknet(model_config_path, model_weights_path)
        self.model = cv.dnn_DetectionModel(net)
        self.model.setInputParams(scale=1 / 255, size=(416, 416), swapRB=True)
        self.conf_threshold = conf_threshold
        self.nms_threshold = nms_threshold

    def detect(self, image: np.ndarray) -> list:
        class_ids, _, boxes = self.model.detect(image, confThreshold=self.conf_threshold,
                                                nmsThreshold=self.nms_threshold)
        filtered_by_class = [box for class_id, box in zip(class_ids, boxes) if class_id == 0]
        max_height = image.shape[1] // 2
        filtered_by_size = [box for box in filtered_by_class if box[2] < max_height]
        return filtered_by_size
