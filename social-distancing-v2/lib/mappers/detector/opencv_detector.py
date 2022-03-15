import cv2

from lib.mappers.core.context_mapper import ContextMapper
from lib.mappers.core.detected_object import DetectedObject
from lib.mappers.core.frame_context import FrameContext

PERSON_CLASS_ID = 0


class OpenCVDetector(ContextMapper):

    def __init__(self, model_config, model_weights, conf_threshold=0.6, nms_threshold=0.4):
        super().__init__()

        net = cv2.dnn.readNetFromDarknet(model_config, model_weights)
        self._model = cv2.dnn_DetectionModel(net)
        self._model.setInputParams(scale=1 / 255, size=(416, 416), swapRB=True)

        self._conf_threshold = conf_threshold
        self._nms_threshold = nms_threshold

    def map(self, context: FrameContext):
        class_ids, confidences, boxes = self._model.detect(context.frame,
                                                           confThreshold=self._conf_threshold,
                                                           nmsThreshold=self._nms_threshold)
        objects = []
        for class_id, confidence, box in zip(class_ids, confidences, boxes):
            if class_id == PERSON_CLASS_ID:
                box_as_tuples = ((box[0], box[1]), (box[0] + box[2], box[1] + box[3]))
                objects.append(DetectedObject(box_as_tuples, confidence, 0))
        context.detected_objects = objects
        return context
