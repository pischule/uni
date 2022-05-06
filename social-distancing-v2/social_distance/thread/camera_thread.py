from typing import Optional

from PySide6 import QtCore
from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtGui import QImage

from social_distance.core.camera import Camera
from social_distance.core.detector import OpenCVPersonDetector
from social_distance.thread.detector_thread import DetectorThread
from social_distance.util import cv_to_qimage, get_path
from social_distance.core.frame_provider import FrameProvider
from social_distance.core.processing import *

import cv2 as cv


class CameraThread(QThread):
    pixmap_changed = Signal(QImage)
    data_changed = Signal(Stats)
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
        self.distance_matrix = np.ones((3, 3), dtype=np.float32)
        self.preview_matrix = np.ones((3, 3), dtype=np.float32)
        self.preview_matrix_inv = np.ones((3, 3), dtype=np.float32)
        self.roi = None
        self.safe_distance = 2
        self.pixel_per_meter = 1
        self.view_mode = 0

        self.data = []
        self.points = []
        self.ground_points = []
        self.is_safe = []

        self.background_subtractor = cv.createBackgroundSubtractorKNN(detectShadows=True)

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
        fgmask = self.background_subtractor.apply(frame)
        fgmask = cv.GaussianBlur(fgmask, (15, 15), 0)
        fgmask = cv.threshold(fgmask, 175, 255, cv.THRESH_BINARY)[1]
        frame = draw_polygon(frame, self.roi)
        preview_points = project_points(self.points, self.preview_matrix)
        if self.view_mode == 0:
            draw_bb(frame, self.is_safe, self.current_bb)
        elif self.view_mode == 1:
            frame = cv.warpPerspective(frame, self.preview_matrix, (1000, 1000))
            draw_circles(frame, preview_points, self.is_safe, self.pixel_per_meter * self.safe_distance / 2)
        else:
            warped = np.zeros((1000, 1000, 3), np.uint8)
            draw_circles(warped, preview_points, self.is_safe, self.pixel_per_meter * self.safe_distance / 2, with_points=False)
            unwarped = cv.warpPerspective(warped, self.preview_matrix_inv, (frame.shape[1], frame.shape[0]))
            cv.bitwise_not(fgmask, fgmask)
            cv.add(frame, unwarped, frame, fgmask)


        qimage = cv_to_qimage(frame)
        self.pixmap_changed.emit(qimage)

    @Slot(Camera)
    def set_camera(self, cam: Camera) -> None:
        self.m.lock()
        self.fp.set_source(cam.address)
        self.distance_matrix = getPerspectiveTransform(cam.square, distance_square(cam.side_length))
        self.preview_matrix = getPerspectiveTransform(cam.square, cam.preview_square)
        self.preview_matrix_inv = np.linalg.inv(self.preview_matrix)
        self.roi = np.asarray(cam.roi, np.int32)
        self.pixel_per_meter = cam.preview_side_length / cam.side_length
        self.m.unlock()
        self.data = []

    @Slot(list)
    def update_current_bb(self, bb: list):
        bb = filter_except_in_polygon(bb, self.roi)
        self.current_bb = bb
        self.points = bb_points(bb)
        self.ground_points = project_points(self.points, self.distance_matrix)
        self.is_safe = classify_safe_unsafe(self.ground_points, self.safe_distance)

        stats = calc_statistics(self.ground_points, self.safe_distance, self.is_safe)
        self.data.append(stats)
        self.data_changed.emit(stats)

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

    @Slot(int)
    def set_view_mode(self, index) -> None:
        self.view_mode = index

    def quit(self) -> None:
        self.keep_running = False
        self.fp.close()
        self.detector_thread.quit()
        self.detector_thread.wait()
        super(CameraThread, self).quit()

