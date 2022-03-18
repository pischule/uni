import cv2

from lib.mappers.core.context_mapper import ContextMapper

from lib.mappers.core.frame_context import FrameContext
from lib.mappers.util.custom_types import Color


class DrawBoxes(ContextMapper):
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
