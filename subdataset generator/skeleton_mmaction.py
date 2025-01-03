import numpy as np
import cv2
import json
import pickle
import os

def make_pkl_2d(root_dir, percentage=100.0):
    data_dict = {}
    data_dict['annotations'] = []

    train_val_ratio = 0.7
    files_list = [item.split('.')[0] for item in os.listdir(os.path.join(root_dir, 'clips_skeleton_merged'))]
    subs_list = list(set([int(item.split('_')[1].replace('p', '')) for item in files_list]))
    # cams_list = list(set([int(item.split('_')[-2]) for item in files_list]))
    subs_train_list, subs_val_list = subs_list[:int(train_val_ratio*len(subs_list))], subs_list[int(train_val_ratio*len(subs_list)):]
    # cams_train_list, cams_val_list = cams_list[:int(train_val_ratio*len(cams_list))], cams_list[int(train_val_ratio*len(cams_list)):]
    xsub_train_list = [item for item in files_list if int(item.split('_')[1].replace('p', '')) in subs_train_list]
    xsub_val_list = [item for item in files_list if int(item.split('_')[1].replace('p', '')) in subs_val_list]
    xview_train_list = [item for item in files_list if int(item.split('_')[-2]) in [2, 3]]
    xview_val_list = [item for item in files_list if int(item.split('_')[-2]) in [1]]
    data_dict['split'] = {'xsub_train': xsub_train_list, 'xsub_val': xsub_val_list, 
                          'xview_train': xview_train_list, 'xview_val': xview_val_list}
    
    for item in sorted(os.listdir(os.path.join(root_dir, 'clips_skeleton_merged'))):
        print(item)
        with open(os.path.join(root_dir, 'clips_skeleton_merged', item), 'rb') as f:
            d = json.load(f)

        all_poses = []
        all_scores = []
        frame_num = 0
        for frame in d['data']:
            if len(frame['skeleton']) == 0: continue
            frame_num += 1

        tmp_frame_num = 0
        for frame in d['data']:
            if len(frame['skeleton']) == 0: continue
            if tmp_frame_num > frame_num * percentage / 100.0: break
            pose = np.array(frame['skeleton'][0]['pose'])
            pose = pose.reshape(int(len(pose)/2), 2)
            score = np.array(frame['skeleton'][0]['score'])
            all_poses.append(pose)
            all_scores.append(score)
            tmp_frame_num += 1
        all_poses = np.expand_dims(np.stack(all_poses), axis=0)
        all_scores = np.expand_dims(np.stack(all_scores), axis=0)

        clip_data = {'frame_dir': item.split('.')[0], 'label': d['label_index'], 'img_shape': (480, 640), 'original_shape': (480, 640),
                     'total_frames': tmp_frame_num, 'keypoint': all_poses, 'keypoint_score': all_scores}
        data_dict['annotations'].append(clip_data)
    
    with open('/home/ips-gpu-server/tianyuwang/mmaction2/data/marcflex-skeleton/assembly/dynamic/our_2d_{}.pkl'.format(int(percentage)), 'wb') as handle:
        pickle.dump(data_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

def make_pkl_3d(root_dir, percentage=100.0):
    data_dict = {}
    data_dict['annotations'] = []

    train_val_ratio = 0.7
    files_list = [item.split('.')[0] for item in os.listdir(os.path.join(root_dir, 'clips_skeleton_merged_3d'))]
    subs_list = list(set([int(item.split('_')[1].replace('p', '')) for item in files_list]))
    # cams_list = list(set([int(item.split('_')[-2]) for item in files_list]))
    subs_train_list, subs_val_list = subs_list[:int(train_val_ratio*len(subs_list))], subs_list[int(train_val_ratio*len(subs_list)):]
    # cams_train_list, cams_val_list = cams_list[:int(train_val_ratio*len(cams_list))], cams_list[int(train_val_ratio*len(cams_list)):]
    xsub_train_list = [item for item in files_list if int(item.split('_')[1].replace('p', '')) in subs_train_list]
    xsub_val_list = [item for item in files_list if int(item.split('_')[1].replace('p', '')) in subs_val_list]
    xview_train_list = [item for item in files_list if int(item.split('_')[-2]) in [2, 3]]
    xview_val_list = [item for item in files_list if int(item.split('_')[-2]) in [1]]
    data_dict['split'] = {'xsub_train': xsub_train_list, 'xsub_val': xsub_val_list, 
                          'xview_train': xview_train_list, 'xview_val': xview_val_list}
    
    for item in sorted(os.listdir(os.path.join(root_dir, 'clips_skeleton_merged_3d'))):
        print(item)
        with open(os.path.join(root_dir, 'clips_skeleton_merged_3d', item), 'rb') as f:
            d = json.load(f)

        all_poses = []
        all_scores = []
        frame_num = 0
        for frame in d:
            if len(frame['instances']) == 0: continue
            frame_num += 1

        tmp_frame_num = 0
        for frame in d:
            if len(frame['instances']) == 0: continue
            if tmp_frame_num > frame_num * percentage / 100.0: break
            pose = np.array(frame['instances'][0]['keypoints'])
            score = np.array(frame['instances'][0]['keypoint_scores'])
            all_poses.append(pose)
            all_scores.append(score)
            tmp_frame_num += 1
        all_poses = np.expand_dims(np.stack(all_poses), axis=0)
        all_scores = np.expand_dims(np.stack(all_scores), axis=0)

        clip_data = {'frame_dir': item.split('.')[0], 'label': int(item.split('.')[0][-1])-1, 'img_shape': (480, 640), 'original_shape': (480, 640),
                     'total_frames': tmp_frame_num, 'keypoint': all_poses}
        data_dict['annotations'].append(clip_data)
    
    with open('/home/ips-gpu-server/tianyuwang/mmaction2/data/marcflex-skeleton/disassembly/static/our_3d_{}.pkl'.format(int(percentage)), 'wb') as handle:
        pickle.dump(data_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    # root_dir = '/home/ips-gpu-server/tianyuwang/har-dataset/MARC-Flex/clipped_video/scenario_d/assembly/video_clips'
    # percentage = 75.0
    # make_pkl_2d(root_dir=root_dir, percentage=percentage)

    root_dir = '/home/ips-gpu-server/tianyuwang/har-dataset/MARC-Flex/clipped_video/scenario_s/disassembly/video_clips'
    percentage = 50.0
    make_pkl_3d(root_dir=root_dir, percentage=percentage)