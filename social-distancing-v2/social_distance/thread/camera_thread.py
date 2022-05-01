from typing import Optional

from PySide6 import QtCore
from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtGui import QImage

from social_distance.core.camera_model import Camera
from social_distance.core.detector import OpenCVPersonDetector
from social_distance.thread.detector_thread import DetectorThread
from social_distance.util import cv_to_qimage, get_path
from social_distance.core.frame_provider import FrameProvider
from social_distance.core.processing import *


class CameraThread(QThread):
    pixmap_changed = Signal(QImage)
    data_changed = Signal(dict)
    m = QtCore.QMutex()

    def __init__(self, parent: Optional[QtCore.QObject] = None):
        super(CameraThread, self).__init__(parent)
        self.keep_running = False
        self.url = None
        self.fp = FrameProvider()

        self.detector_thread = DetectorThread(self)
        self.detector_thread.done.connect(self.update_current_bb)
        self.detector_thread.start()

        self.current_bb = []
        self.perspective_matrix = np.ones((3, 3), dtype=np.float32)
        self.roi = None
        self.safe_distance = 2

    def run(self):
        self.keep_running = True
        while self.keep_running:
            self.process_tick()

    def process_tick(self) -> None:
        self.m.lock()
        frame = self.fp.get_frame()
        self.m.unlock()
        if frame is None:
            return

        self.detector_thread.pass_image(frame)
        bb = self.current_bb
        bb = filter_except_in_polygon(bb, self.roi)
        points = bb_points(bb)
        ground_points = project_points(points, self.perspective_matrix)
        is_safe = classify_safe_unsafe(ground_points, self.safe_distance)
        draw_bb(frame, is_safe, bb)
        frame = draw_polygon(frame, self.roi)
        stats = calc_statistics(ground_points, self.safe_distance, is_safe)

        qimage = cv_to_qimage(frame)
        self.pixmap_changed.emit(qimage)
        self.data_changed.emit(stats)

    @Slot(Camera)
    def set_camera(self, cam: Camera) -> None:
        self.m.lock()
        self.fp.set_source(cam.address)
        self.perspective_matrix = np.asarray(cam.transform_matrix, dtype=np.float32)
        self.roi = np.asarray(cam.roi, np.int32)
        self.m.unlock()

    @Slot(list)
    def update_current_bb(self, bb: list):
        self.current_bb = bb

    @Slot(float)
    def set_safe_distance(self, distance: float) -> None:
        self.safe_distance = distance

    @Slot(int)
    def set_model(self, index) -> None:
        network = NETWORK_FILENAMES[index]
        detector = OpenCVPersonDetector(get_path('models', f'{network}.cfg'),
                                        get_path('models', f'{network}.weights'),
                                        conf_threshold=0.1, nms_threshold=0.1)
        self.detector_thread.set_detector(detector)

    def quit(self) -> None:
        self.keep_running = False
        self.fp.close()
        self.detector_thread.quit()
        self.detector_thread.wait()
        super(CameraThread, self).quit()

