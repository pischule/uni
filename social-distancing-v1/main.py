import cv2

import numpy as np
import math
import json

in_filename = "terrace1-c0.avi"
out_filename = 'output.avi'
safe_distance = 200
model_configuration_filename = 'yolov3-tiny.cfg'
model_weights_filename = 'yolov3-tiny.weights'
picker_window_size = [800, 800]
homography_matrix_filename = 'M.json'

vid = cv2.VideoCapture(in_filename)
FPS = vid.get(cv2.CAP_PROP_FPS)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = None

with open('coco.names') as f:
    classes = f.readlines()


def load_model():
    net = cv2.dnn.readNetFromDarknet(model_configuration_filename, model_weights_filename)
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(scale=1 / 255, size=(416, 416), swapRB=True)
    return model


def scale_frame(img, width=1280, height=720):
    old_height, old_width = img.shape[:2]
    width_ratio = width / old_width
    height_ratio = height / old_height
    ratio = min(width_ratio, height_ratio)
    new_size = (int(old_width * ratio), int(old_height * ratio))
    return cv2.resize(img, new_size, fx=0, fy=0, interpolation=cv2.INTER_CUBIC)


model = load_model()


def draw_box(img, box, color=(0, 255, 0), text=''):
    cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), color=color, thickness=2)
    cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] - 15), color=color, thickness=-1)
    cv2.putText(img, text, (box[0], box[1] - 3), cv2.FONT_HERSHEY_PLAIN, 0.8, color=(255, 255, 255), thickness=1)


def draw_points(img, p, color=(0, 0, 255)):
    cv2.circle(img, (p[0], p[1]), 5, color, -1)


def process_frame(img):
    class_ids, all_scores, all_boxes = model.detect(img, confThreshold=0.6, nmsThreshold=0.4)
    boxes = []
    scores = []
    for (class_id, score, box) in zip(class_ids, all_scores, all_boxes):
        if class_id != 0:
            continue
        boxes.append(box)
        scores.append(score)
    return boxes, scores


def get_box_points(boxes):
    box_points = []
    for box in boxes:
        box_point = (box[0] + box[2] // 2, box[1] + box[3])
        box_points.append(box_point)
    return box_points


first_img = None
four_points = []


def on_mouse(event, x, y, flags, param):
    global first_img
    global four_points
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(four_points) < 4:
            four_points.append((x, y))
            cv2.circle(first_img, (x, y), 5, (0, 0, 255), -1)

    if event == cv2.EVENT_MOUSEWHEEL:
        if four_points:
            four_points = four_points[:-1]

    cv2.imshow('points', first_img)


M = None

sq_x = picker_window_size[0] // 2
sq_y = picker_window_size[1] // 2
sq_r = 200

src_pts = None


def update_picker_image():
    src_pts = np.asarray(four_points, dtype=np.float32)
    dst_pts = np.array([[sq_x - sq_r, sq_y - sq_r],
                        [sq_x + sq_r, sq_y - sq_r],
                        [sq_x + sq_r, sq_y + sq_r],
                        [sq_x - sq_r, sq_y + sq_r]], dtype=np.float32)
    global M
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    warp = cv2.warpPerspective(first_img, M, (picker_window_size[0], picker_window_size[1]))
    cv2.imshow('points', warp)


def on_trackbar_sq_x(val):
    global sq_x
    sq_x = val
    update_picker_image()


def on_trackbar_sq_y(val):
    global sq_y
    sq_y = val
    update_picker_image()


def on_trackbar_sq_r(val):
    global sq_r
    sq_r = val
    update_picker_image()


def pick_m(img):
    global first_img
    first_img = img.copy()
    cv2.imshow('points', first_img)
    cv2.namedWindow('points')
    cv2.setMouseCallback('points', on_mouse)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    first_img = img.copy()

    if len(four_points) != 4:
        return

    title_window = 'points'

    cv2.namedWindow('points')
    cv2.createTrackbar('sq_r', title_window, sq_r, max(picker_window_size), on_trackbar_sq_r)
    cv2.createTrackbar('sq_x', title_window, sq_x, picker_window_size[0], on_trackbar_sq_x)
    cv2.createTrackbar('sq_y', title_window, sq_y, picker_window_size[1], on_trackbar_sq_y)
    update_picker_image()
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    with open(homography_matrix_filename, 'w') as f:
        json.dump(M.tolist(), f)


def picker_safe_distance(val):
    global safe_distance
    safe_distance = val


def process_first_frame(img):
    global first_img
    first_img = img
    size = img.shape[-2::-1]
    try:
        with open(homography_matrix_filename) as f:
            m_list = json.load(f)
            global M
            M = np.array(m_list, dtype=np.float32)
    except Exception:
        pick_m(img)

    global out
    out = cv2.VideoWriter(out_filename, fourcc, FPS, size)


def show_wrapped(img, box_points, window_name='warp'):
    warp = cv2.warpPerspective(img, M, (picker_window_size[0], picker_window_size[1]))

    dst_pts = get_real_points(box_points)
    for p in dst_pts:
        cv2.circle(warp, (p[0], p[1]), 5, (0, 0, 255), -1)

    cv2.imshow(window_name, warp)


def get_real_points(box_points):
    if not box_points:
        return []
    src_pts = np.asarray([box_points], dtype=np.float32)
    dst_pts = cv2.perspectiveTransform(src_pts, M)[0]
    return dst_pts.astype(int)


def get_close_indices(points, min_dist):
    indices = [False] * len(points)
    pairs = []
    for i in range(len(points)):
        for j in range(i):
            p1 = points[i]
            p2 = points[j]
            distance = math.hypot(p1[0] - p2[0], p1[1] - p2[1])
            # print(i, j, distance)
            if distance <= min_dist:
                pairs.append((i, j))
                indices[i] = True
                indices[j] = True
    return indices, pairs


def get_color(i):
    return (0, 0, 255) if i else (76, 153, 0)


def get_time(frame_number):
    seconds = int(frame_number // FPS)
    return f'{seconds // 60:01d}:{int(seconds % 60):02d}'


def main():
    skip = True

    ret, img = vid.read()
    img = scale_frame(img)
    process_first_frame(img)

    cv2.namedWindow('frame')
    cv2.namedWindow('warp')
    cv2.createTrackbar('safe_distance', 'warp', safe_distance, picker_window_size[1], picker_safe_distance)

    frame_count = 1

    while True:
        ret, img = vid.read()
        if not ret:
            break
        img = scale_frame(img)
        warp = cv2.warpPerspective(img, M, (picker_window_size[0], picker_window_size[1]))
        if not skip:
            boxes, scores = process_frame(img)
            box_points = get_box_points(boxes)
            real_points = get_real_points(box_points)
            indices, pairs = get_close_indices(real_points, safe_distance)

            for (box, i, score) in zip(boxes, indices, scores):
                draw_box(img, box, color=get_color(i), text=f'person: {score:.2f}')

            for (i, j) in pairs:
                p1 = real_points[i]
                p2 = real_points[j]
                cv2.line(warp, p1, p2, (0, 0, 255), thickness=2)

            for p, i in zip(real_points, indices):
                cv2.circle(warp, p, safe_distance // 2, color=get_color(i), thickness=2)
                cv2.circle(warp, p, 5, get_color(i), thickness=-1)

        picture_offset = 10
        picture_size = 250
        resized_warp = cv2.resize(warp, (picture_size, picture_size))

        cv2.imshow('frame', img)
        cv2.imshow('warp', warp)

        img[picture_offset:picture_size + picture_offset, picture_offset:picture_size + picture_offset] = resized_warp

        out.write(cv2.resize(img, img.shape[-2::-1]))

        key = cv2.waitKey(1)

        if key & 0xFF == ord('t'):
            skip = not skip
        if key & 0xFF == ord('q'):
            break

        frame_count += 1
        if not frame_count % FPS:
            print(get_time(frame_count))

    vid.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
