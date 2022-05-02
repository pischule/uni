import os.path

import cv2
from PySide6.QtGui import QImage, Qt, QPolygonF


def get_frame(address):
    cap = None
    try:
        real_address = 0 if address == '0' else address
        cap = cv2.VideoCapture(real_address)
        if cap.isOpened():
            for _ in range(15):
                cap.read()
            ret, frame = cap.read()
            if ret:
                return frame
    finally:
        if cap:
            cap.release()
    return None


def cv_to_qimage(frame) -> QImage:
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    return QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)


def qpolygonf_to_list(qpolygon: QPolygonF) -> list:
    return [p.toTuple() for p in qpolygon]


def get_path(*segments) -> str:
    return os.path.join('data', *segments)


def qpolygon_to_list(qpolygon: QPolygonF) -> list:
    return [p.toTuple() for p in qpolygon]