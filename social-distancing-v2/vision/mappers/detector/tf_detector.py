
# import tensorflow_hub as hub

from vision.mappers.core.context_mapper import ContextMapper

import cv2

import numpy as np


# TODO: Implement this class
class TensorflowDetector(ContextMapper):
    def __init__(self, src):
        super().__init__()
        # self.detector = hub.load("/Users/maksim/PycharmProjects/code/ssd_mobilenet_v2_2")
        print('start load model')
        # self.detector = hub.Module("/Users/maksim/PycharmProjects/code/openimages_v4_ssd_mobilenet_v2_1")
        print('stop load model')
        # self.detector = hub.load("https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2")
        self.src = src

    def map(self, data):
        img_rgb = cv2.cvtColor(data[self.src], cv2.COLOR_BGR2RGB)
        # img_tensor = np.array(img_rgb).reshape((1, 720, 1280, 3)).astype(np.uint8)
        img_tensor = np.array(img_rgb).reshape((1, 720, 1280, 3)).astype(np.float32)
        detector_output = self.detector(img_tensor)
        data['detect_result'] = detector_output
        return data
