from enum import Enum
import numpy as np

from lib import util
from lib.mappers.capture.fps_counter import FpsCounter
from lib.mappers.core.context_mapper import ContextMapper, GenericMapper
from lib.mappers.core.frame_context import FrameContext
from lib.mappers.detector.opencv_detector import OpenCVDetector
from lib.mappers.detector.tracker import SortTracker
from lib.mappers.display.frame_scaler import FrameScaler
from lib.mappers.overlay.draw_boxes import DrawBoxes
from lib.mappers.overlay.info_overlay import InfoOverlay
from lib.mappers.calculators.absolute_positions_calculator import AbsolutePositionsCalculator


class Networks(Enum):
    YOLOv3 = 'yolo3'
    YOLOv3_TINY = 'yolo3_tiny'


network = Networks.YOLOv3_TINY


class FrameProcessor(GenericMapper[np.ndarray, np.ndarray]):

    def __init__(self):

        perspective_matrix = util.square_perspective_transform_matrix(
            util.point_to_tetragon((100, 100)),
            0.5
        )

        path_to_models = '/Users/maksim/Projects/SocialDistance/SocialDistance/models/'
        self._pipeline = (
            # yolov3(),
            # AddValue('roi', [(10, 10), (640, 10), (640, 500), (10, 400)]),
            # VideoCapture(os.path.join('..', 'video', 'vid0.mp4'), limit_fps=False),
            FrameScaler((1280, 720)),
            OpenCVDetector(
                model_config=f'/Users/maksim/Projects/SocialDistance/SocialDistance/models/{network.value}/n.cfg',
                model_weights=f'/Users/maksim/Projects/SocialDistance/SocialDistance/models/{network.value}/n.weights',
                conf_threshold=0.01, nms_threshold=0.01),
            SortTracker(max_age=30, min_hits=10),
            AbsolutePositionsCalculator(perspective_matrix),
            FpsCounter(every=5),
            DrawBoxes(color=(0, 200, 0), thickness=2, label=True),
            # FrameScaler((1680, 1050)),
            InfoOverlay(),
            # VideoDisplay()
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def map(self, frame: np.ndarray) -> np.ndarray:
        context = FrameContext()
        context.frame = frame
        for step in self._pipeline:
            context = step.map(context)
        return context.frame

    def cleanup(self):
        for step in self._pipeline:
            step.cleanup()
