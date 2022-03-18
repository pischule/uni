import numpy as np

from lib.mappers.core.context_mapper import ContextMapper

import cv2


class TopDownView(ContextMapper):
    def __init__(self, perspective_matrix):
        self._perspective_matrix = perspective_matrix
        self._window_name = "Top Down View"

    def map(self, context):
        warp = cv2.warpPerspective(context.frame, self._perspective_matrix, (600, 600))
        cv2.imshow(self._window_name, warp)
        return context

    def cleanup(self):
        cv2.destroyWindow(self._window_name)
