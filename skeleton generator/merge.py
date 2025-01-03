import argparse
import os
import json

from dict import debug

# This is the template script to merge individial skeleton frames into a procedural one.

def make_data_dict(openpose_save, node=18, hand=False, fhd=False):
    frame_index = 0
    data = []
    files = [i for i in os.listdir(openpose_save) if os.path.isfile(openpose_save + i)]
    files.sort()  # file is a list
    for fname in files:
        f = open(os.path.join(openpose_save, fname))
        json_data = json.load(f)
        people_list = json_data["people"]
        frame_index += 1
        if frame_index >= 300:
            continue
        data_dict = {"frame_index": frame_index}
        mean_score = []
        skel_list = []
        for i in range(len(people_list)):
            skel_dict = dict()
            a = []
            pose_list = []
            score_list = []
            a = people_list[i]["pose_keypoints_2d"]  # 18*3=54 or 25*3
            if node == 18:  # get only the x,y
                pose_list = [a[j] for j in range(54) if not (j + 1) % 3 == 0]
                # pose_list[16:18] = []
            elif node == 25:
                pose_list = [a[j] for j in range(75) if not (j + 1) % 3 == 0]

            if fhd:  # normalization with camera resolution 1920*1080
                for x in range(len(pose_list)):
                    if x % 2 == 0:
                        pose_list[x] = round(pose_list[x] / 1920, 3)
                    else:
                        pose_list[x] = round(pose_list[x] / 1080, 3)

            if node == 18:
                score_list = [round(a[j], 3) for j in range(54) if (j + 1) % 3 == 0]
            elif node == 25:
                score_list = [round(a[j], 3) for j in range(75) if (j + 1) % 3 == 0]
            if hand:
                rhand = []
                lhand = []
                bhand = []
                hand_list = []
                hand_score = []
                rhand = people_list[i]["hand_right_keypoints_2d"][3:]
                lhand = people_list[i]["hand_left_keypoints_2d"][3:]
                bhand = rhand + lhand
                hand_list = [bhand[j] for j in range(120) if (j + 1) % 3 != 0]
                for x in range(len(hand_list)):
                    if x % 2 == 0:
                        hand_list[x] = round(hand_list[x] / 1920, 3)
                    else:
                        hand_list[x] = round(hand_list[x] / 1080, 3)
                pose_list = pose_list + hand_list
                hand_score = [round(bhand[j], 3) for j in range(120) if (j + 1) % 3 == 0]
                score_list = score_list + hand_score

            skel_dict["pose"] = pose_list
            skel_dict["score"] = score_list
            n_of_node = len(score_list) - score_list.count(0)
            try:
                mean_score.append(sum(score_list) / n_of_node)
            except ZeroDivisionError:
                mean_score.append(0)
            skel_list.append(skel_dict)
        while len(mean_score) >= 3:
            k = []
            k = [x for x, y in enumerate(mean_score) if y == min(mean_score)]
            del skel_list[k[0]]
            del mean_score[k[0]]
        data_dict["skeleton"] = skel_list
        data.append(data_dict)
    final_dict = {"data": data}
    return final_dict


def save_json(final_dict, json_path):
    with open(json_path, 'w') as f:
        json.dump(final_dict, f)


def merge_single_video(input_path, output_path, node=18, hand=False, fhd=False):
    openpose_file = os.listdir(input_path)
    openpose_file.sort()
    data_dict = make_data_dict(input_path, node=18, hand=False, fhd=False)
    for f_name in openpose_file:
        split = f_name.split('_')
        frame = int(split[1][-3:])
        label = split[0]
        label_index = zhihao_debug[label]
    data_dict['label'] = label
    data_dict['label_index'] = label_index
    json_name = output_path + input_path.split('/')[-2] + '.json'  # for multi video with one label
    save_json(data_dict, json_name)
    print(json_name + ' saved')


def merge_multiple_video(video_folder, output_path, node=18, hand=False, fhd=False):
    video = os.listdir(video_folder)
    index = 0
    for v in video:
        print(v)
        input_path = video_folder + v + '/' 
        merge_single_video(input_path, output_path, node, hand, fhd)
        index += 1
        print("[%d/%d] %s has been merged successfully!" % (index, len(video), v.split('.')[0]))

video_folder = 'Your Path'
input_path = 'Your Path'

# create a new folder for merged json
output_path = os.path.dirname(input_path) + '_merged/'
if not os.path.exists(output_path):
    os.mkdir(output_path)

output_folder = os.path.dirname(video_folder) + '_merged/'
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

merge_multiple_video(video_folder, output_folder)

