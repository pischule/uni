import cv2
import numpy as np

from lib.mappers.core.context_mapper import ContextMapper
from lib.mappers.core.frame_context import FrameContext


class BackgroundSubtractorDetector(ContextMapper):
    def __init__(self):
        self._background_subtractor = cv2.createBackgroundSubtractorKNN(history=10, detectShadows=False,
                                                                        dist2Threshold=600)

    def map(self, context: FrameContext) -> FrameContext:
        # fg_mask = cv2.fastNlMeansDenoisingColored(context.frame,None,10,10,7,21)

        fg_mask = self._background_subtractor.apply(context.frame)
        cv2.threshold(fg_mask, 254, 255, cv2.THRESH_BINARY, fg_mask)
        # cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), fg_mask)
        # cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)), fg_mask)

        cv2.dilate(fg_mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8)), fg_mask)

        cnts = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        for c in cnts:
            area = cv2.contourArea(c)
            if 200 < area < 100000:
                cv2.drawContours(context.frame, [c], 0, (0, 0, 255), -1)

        # context.frame = fg_mask
        return context
