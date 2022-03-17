from enum import Enum
import numpy as np

from lib import util
from lib.mappers.core.context_mapper import GenericMapper
from lib.mappers.core.frame_context import FrameContext
from lib.mappers.detector.opencv_detector import OpenCVDetector
from lib.mappers.detector.tracker import SortTracker
from lib.mappers.calculators.absolute_positions_calculator import AbsolutePositionsCalculator


class Networks(Enum):
    YOLOv3 = 'yolo3'
    YOLOv3_TINY = 'yolo3_tiny'


network = Networks.YOLOv3


class FrameProcessor(GenericMapper[np.ndarray, np.ndarray]):

    def __init__(self):
        self._detector = OpenCVDetector(
            model_config=f'/Users/maksim/Projects/SocialDistance/SocialDistance/models/{network.value}/n.cfg',
            model_weights=f'/Users/maksim/Projects/SocialDistance/SocialDistance/models/{network.value}/n.weights',
            conf_threshold=0.01, nms_threshold=0.01)
        self._tracker = SortTracker(max_age=30, min_hits=10)
        perspective_matrix = util.square_perspective_transform_matrix(
            util.point_to_tetragon((100, 100)),
            0.5
        )
        self._position_calculator = AbsolutePositionsCalculator(perspective_matrix)

    def map(self, frame: np.ndarray) -> FrameContext:
        context = FrameContext()
        context.frame = frame
        context = self._detector.map(context)
        context = self._tracker.map(context)
        context = self._position_calculator.map(context)
        return context
