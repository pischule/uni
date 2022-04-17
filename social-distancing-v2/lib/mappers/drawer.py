import cv2
import numpy as np

from lib.types import Color, ContextMapper, FrameContext, Point


class PolygonDrawer(ContextMapper):
    def __init__(self, polygon=None, color: Color = (0, 255, 0), alpha=0.5, inverted=False):
        if polygon is None:
            polygon = list()
        self._color = color
        self._polygon = polygon
        self._alpha = alpha
        self._inverted = inverted

    def map(self, context: FrameContext) -> FrameContext:
        if self._inverted:
            img_red = np.zeros_like(context.frame)
            img_red[:, :, -1] = 255
            mask = np.full_like(context.frame, (1, 1, 1), dtype=np.float32)
            mask = cv2.fillPoly(mask, [self.polygon], (0, 0, 0), lineType=cv2.LINE_AA)
            result = cv2.add(context.frame * (1 - mask), img_red * mask).astype(np.uint8)
            context.frame = cv2.addWeighted(context.frame, 1 - self._alpha, result, self._alpha, 0)
        else:
            # frame = cv2.polylines(context.frame.copy(), [self.polygon], True, self._color, 2)
            frame = cv2.fillPoly(context.frame.copy(), [self.polygon], self._color, lineType=cv2.LINE_AA)
            context.frame = cv2.addWeighted(context.frame, 1 - self._alpha, frame, self._alpha, 0)
        return context

    @property
    def polygon(self):
        return self._polygon

    @polygon.setter
    def polygon(self, polygon: list):
        self._polygon = np.asarray(polygon, np.int32).reshape((-1, 1, 2))


class BoxesDrawer(ContextMapper):
    def __init__(self, safe_color: Color = (0, 255, 0), unsafe_color=(0, 0, 255), thickness=2, label=False,
                 only_tracked=True):
        super().__init__()
        self._safe_color = safe_color
        self._unsafe_color = unsafe_color
        self._thickness = thickness
        self._label = label
        self._only_tracked = only_tracked

    def map(self, context: FrameContext):
        for obj in context.detected_objects:
            if obj.track_id == 0 and self._only_tracked:
                continue

            color = {
                True: self._safe_color,
                False: self._unsafe_color
            }[obj.safe]

            pt1, pt2 = obj.box
            text = f"{obj.track_id}"

            cv2.rectangle(img=context.frame, pt1=pt1, pt2=pt2,
                          color=color, thickness=self._thickness)

            if self._label:
                font_face = cv2.FONT_HERSHEY_PLAIN
                font_scale = 1.3
                font_thickness = 1
                text_size = cv2.getTextSize(text=text, fontFace=font_face, fontScale=font_scale,
                                            thickness=font_thickness)[0][0]
                cv2.rectangle(img=context.frame, pt1=pt1, pt2=(pt1[0] + text_size, pt1[1] - 20), color=color,
                              thickness=-1)
                cv2.putText(img=context.frame, text=text, org=(pt1[0], pt1[1] - 3),
                            fontFace=font_face, fontScale=font_scale, color=(255, 255, 255),
                            thickness=2)
        return context


class FrameScaler(ContextMapper):
    def __init__(self, new_size: Point):
        self.new_size = new_size

    def map(self, context: FrameContext) -> FrameContext:
        min_scale = min(self.new_size[0] / context.frame.shape[0], self.new_size[1] / context.frame.shape[1])
        context.frame = cv2.resize(context.frame, (0, 0), fx=min_scale, fy=min_scale)
        return context