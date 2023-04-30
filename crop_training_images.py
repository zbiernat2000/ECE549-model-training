import cv2
import json

f = open('ann_subsample/forward.json')


def crop(frame, bbox):
    """
    Crops the frame to only give the bounding box
    :param frame: Image
    :param bbox: [x_min,y_min,width,height]
    :return: Cropped image
    """
    '[0.44759481, 0.44759481, 0.16477829, 0.16282391]'
    y_max, x_max, _ = frame.shape
    min_y = int(bbox[1] * y_max)
    height = int(bbox[3] * y_max + min_y)
    min_x = int(bbox[0] * x_max)
    width = int(min_x + bbox[2] * x_max)

    return frame[min_y:height, min_x:width]


def get_gesture_index(label_list):
    """
    Gets the index for the correct label form the label_list
    :param label_list: List of labels
    :return: Index in which proper label is at
    """
    x = 0
    for i in label_list:
        if i == 'no_gesture':
            x += 1
        else:
            return x
    return -1


def get_bbox(json):
    """
    Extracts correct bbox from json
    :param json: Single json
    :return: bbox list
    """
    idx = get_gesture_index(json['labels'])
    return json['bboxes'][idx]


def crop_by_json(gesture, json_key, json):
    """
    Saves cropped photo into cropped_data folder
    :param gesture: Gesture being cropped
    :param json_key: Single json_key
    :param json: single json
    :return: None
    """
    frame = cv2.imread(f'data/{gesture}/{json_key}.jpg', cv2.IMREAD_COLOR)
    bbox = get_bbox(json)
    frame = crop(frame, bbox)
    cv2.imwrite(f'cropped_data/{gesture}/{json_key}.jpg', frame)


def save_all_by_gesture(gesture):
    """
    saves all imgs of a gesture
    :param gesture: gesture being saved
    :return: none
    """
    f = open(f'ann_subsample/{gesture}.json')
    json_list = json.load(f)
    for i in json_list.keys():
        crop_by_json(gesture, i, json_list[i])


label_list = ['backward','forward','stop','left','right']
for i in label_list:
    save_all_by_gesture(i)