import time
from typing import Optional

import cv2 as cv
import numpy as np


class FrameProvider:
    def __init__(self):
        self.cap = None
        self.wait_time = 0

    def get_frame(self) -> Optional[np.ndarray]:
        if self.cap is None:
            return None
        ret, frame = self.cap.read()
        if ret:
            time.sleep(self.wait_time)
            return frame
        else:
            return None

    def set_source(self, source: str) -> bool:
        source = 0 if source == '0' else source
        new_cap = cv.VideoCapture(source)
        if not new_cap.isOpened():
            return False
        if self.cap:
            self.cap.release()
        self.cap = new_cap
        self.wait_time = 1.0 / self.cap.get(cv.CAP_PROP_FPS)
        return True

    def close(self):
        if self.cap:
            self.cap.release()


if __name__ == '__main__':
    fp = FrameProvider()
    # fp.set_source('/Users/maksim/Projects/SocialDistance/SocialDistance/data/video/vid1.mp4')
    fp.set_source('0')

    while True:
        frame = fp.get_frame()
        if frame is None:
            break
        cv.imshow('frame', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    fp.close()
    cv.destroyAllWindows()