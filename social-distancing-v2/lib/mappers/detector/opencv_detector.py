import cv2

from lib.mappers.core.context_mapper import ContextMapper
from lib.mappers.core.detected_object import DetectedObject
from lib.mappers.core.frame_context import FrameContext

coco_names = ('person', 'bicycle', 'car', 'motorbike', 'aeroplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
              'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
              'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
              'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
              'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
              'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'sofa',
              'pottedplant', 'bed', 'diningtable', 'toilet', 'tvmonitor', 'laptop', 'mouse', 'remote', 'keyboard',
              'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
              'teddy bear', 'hair drier', 'toothbrush')


class PersonDetector(ContextMapper[FrameContext]):

    def __init__(self, model_config, model_weights, conf_threshold=0.6, nms_threshold=0.4):
        super().__init__()

        net = cv2.dnn.readNetFromDarknet(model_config, model_weights)
        self.model = cv2.dnn_DetectionModel(net)
        self.model.setInputParams(scale=1 / 255, size=(416, 416), swapRB=True)

        self.conf_threshold = conf_threshold
        self.nms_threshold = nms_threshold

    def map(self, context: FrameContext):
        class_ids, confidences, boxes = self.model.detect(context.frame,
                                                          confThreshold=self.conf_threshold,
                                                          nmsThreshold=self.nms_threshold)
        objects = []
        for class_id, confidence, box in zip(class_ids, confidences, boxes):
            box_as_tuples = ((box[0], box[1]), (box[0] + box[2], box[1] + box[3]))
            objects.append(DetectedObject(box_as_tuples, coco_names[class_id], confidence))
        context.detected_objects = objects
        return context
