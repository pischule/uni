import cv2

from lib.mappers.core.context_mapper import ContextMapper

from lib.mappers.core.frame_context import FrameContext
from lib.mappers.util.custom_types import Color


class DrawBoxes(ContextMapper[FrameContext]):
    def __init__(self, color: Color = (255, 0, 0), thickness=2, label=False):
        super().__init__()
        self.color = color
        self.thickness = thickness
        self.label = label

    def map(self, context: FrameContext):
        for obj in context.detected_objects:
            pt1, pt2 = obj.box
            text = f"{obj.class_name} : {obj.confidence:.2f}"

            cv2.rectangle(img=context.frame, pt1=pt1, pt2=pt2,
                          color=self.color, thickness=self.thickness)

            if self.label:
                font_face = cv2.FONT_HERSHEY_PLAIN
                font_scale = 1.3
                font_thickness = 1
                text_size = cv2.getTextSize(text=text, fontFace=font_face, fontScale=font_scale,
                                            thickness=font_thickness)[0][0]
                cv2.rectangle(img=context.frame, pt1=pt1, pt2=(pt1[0] + text_size, pt1[1] - 20), color=self.color,
                              thickness=-1)
                cv2.putText(img=context.frame, text=text, org=(pt1[0], pt1[1] - 3),
                            fontFace=font_face, fontScale=font_scale, color=(255, 255, 255),
                            thickness=2)
        return context
