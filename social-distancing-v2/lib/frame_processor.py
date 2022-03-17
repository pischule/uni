from enum import Enum
from typing import Iterable, ContextManager

from lib import util
from lib.mappers.capture.fps_counter import FpsCounter
from lib.mappers.capture.video_capture import VideoCapture
from lib.mappers.core.frame_context import FrameContext
from lib.mappers.detector.opencv_detector import OpenCVDetector
from lib.mappers.detector.tracker import SortTracker
from lib.mappers.display.video_display import VideoDisplay
from lib.mappers.overlay.draw_boxes import DrawBoxes
from lib.mappers.overlay.info_overlay import InfoOverlay
from lib.mappers.calculators.absolute_positions_calculator import AbsolutePositionsCalculator


class Networks(Enum):
    YOLOv3 = 'yolo3'
    YOLOv3_TINY = 'yolo3_tiny'


network = Networks.YOLOv3

print('Loading network...')
print(f'Network : {network.value}')


class FrameProcessor(Iterable[FrameContext], ContextManager):

    def __iter__(self):
        return self

    def __next__(self):
        return self._execute()

    def __enter__(self):

        perspective_matrix = util.square_perspective_transform_matrix(
            util.point_to_tetragon((100, 100)),
            0.5
        )

        self.pipeline = (
            # yolov3(),
            # AddValue('roi', [(10, 10), (640, 10), (640, 500), (10, 400)]),
            VideoCapture(0, limit_fps=False),
            # VideoCapture(os.path.join('..', 'video', 'vid0.mp4'), limit_fps=False),
            OpenCVDetector(model_config=f'../models/{network.value}/n.cfg',
                           model_weights=f'../models/{network.value}/n.weights',
                           conf_threshold=0.6, nms_threshold=0.4),
            SortTracker(max_age=30, min_hits=10),
            AbsolutePositionsCalculator(perspective_matrix),
            FpsCounter(every=5),
            DrawBoxes(color=(0, 200, 0), thickness=2, label=True),
            # FrameScaler((1680, 1050)),
            InfoOverlay(),
            VideoDisplay()
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def _execute(self):
        context = FrameContext()
        for step in self.pipeline:
            context = step.map(context)
        return context

    def cleanup(self):
        for step in self.pipeline:
            step.cleanup()


if __name__ == '__main__':
    with FrameProcessor() as fp:
        for frame in fp:
            pass
