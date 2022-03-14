from typing import List
import cv2

import numpy as np

from lib.mappers.core.context_mapper import ContextMapper
from lib.mappers.core.detected_object import DetectedObject
from lib.mappers.core.frame_context import FrameContext

from sort import Sort


class SortTracker(ContextMapper):

    def __init__(self, max_age: int = 10, min_hits: int = 3):
        self._tracker = Sort(max_age=max_age, min_hits=min_hits)

    def map(self, context: FrameContext) -> FrameContext:
        result = self._tracker.update(self._map_objects(context.detected_objects))
        context.detected_objects = self._map_back(result)
        return context

    def _map_objects(self, detections: List[DetectedObject]) -> np.ndarray:
        if detections:
            return np.array(
                [[obj.box[0][0], obj.box[0][1], obj.box[1][0], obj.box[1][1], obj.confidence] for obj in detections])
        else:
            return np.zeros((0, 5))

    def _map_back(self, detections: np.ndarray) -> List[DetectedObject]:
        return [
            DetectedObject(
                box=((o[0], o[1]), (o[2], o[3])),
                class_name="person",
                confidence=1.0,
                track_id=o[4]
            ) for o in detections.astype(np.int32).tolist()
        ]
