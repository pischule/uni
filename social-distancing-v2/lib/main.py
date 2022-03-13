from lib.mappers.capture.video_capture import VideoCapture
from lib.mappers.display.video_display import VideoDisplay
from lib.mappers.overlay.info_overlay import InfoOverlay
from lib.mappers.capture.fps_counter import FpsCounter
from lib.mappers.detector.opencv_detector import PersonDetector
from lib.mappers.overlay.draw_boxes import DrawBoxes


# from pipe.detectors.tf_detector import TensorflowDetector


def yolov3(**kwargs) -> PersonDetector:
    return PersonDetector(model_config='../models/yolov3.cfg', model_weights='../models/yolov3.weights', **kwargs)


def yolov3_tiny(**kwargs) -> PersonDetector:
    return PersonDetector(model_config='../models/yolov3-tiny.cfg', model_weights='../models/yolov3-tiny.weights',
                          **kwargs)


pipeline = [
    VideoCapture(),
    # yolov3(),
    # AddValue('roi', [(10, 10), (640, 10), (640, 500), (10, 400)]),
    yolov3_tiny(src='image', conf_threshold=0.1, nms_threshold=0.1),
    # TensorflowDetector(src='image'),
    # ClassFilter(allowed_classes={'person'}),
    # DrawPolygon('roi'),
    # PolygonFilter(poly_key='roi', obj_key='objects'),
    DrawBoxes(color=(255, 0, 0), thickness=2, label=True),
    FpsCounter(every=5),
    InfoOverlay(),
    VideoDisplay()
]


def execute_pipe():
    try:
        while True:
            data = dict()
            for step in pipeline:
                data = step.map(data)
    except StopIteration:
        print('stop')
    finally:
        for step in pipeline:
            step.cleanup()


def main():
    execute_pipe()


if __name__ == '__main__':
    main()
