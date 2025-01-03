import numpy as np
import cv2
import json
import pickle
import os
import shutil
from moviepy.video.io.VideoFileClip import VideoFileClip


def trim_video(input_dir, start_percent, end_percent):
    for item in os.listdir(input_dir):
        # Load the video clip
        video_clip = VideoFileClip(os.path.join(input_dir, item))

        # Calculate the start and end times based on percentages
        total_duration = video_clip.duration
        start_time = start_percent / 100 * total_duration
        end_time = end_percent / 100 * total_duration

        # Trim the video clip
        trimmed_clip = video_clip.subclip(start_time, end_time)

        # Write the trimmed clip to a new file
        trimmed_clip.write_videofile(os.path.join(input_dir+str(int(end_percent)), item), codec="libx264", audio_codec="aac")

        # Close the clips to free up resources
        video_clip.close()
        trimmed_clip.close()


def make_video_dataset(root_dir, new_dir, percentage=''):
    # xsam_train_list = [item.split('.')[0] for item in os.listdir(os.path.join(root_dir, 'XSample', 'train'))]
    # xsam_val_list = [item.split('.')[0] for item in os.listdir(os.path.join(root_dir, 'XSample', 'val'))]
    # xsub_train_list = [item.split('.')[0] for item in os.listdir(os.path.join(root_dir, 'XSub', 'train'))]
    # xsub_val_list = [item.split('.')[0] for item in os.listdir(os.path.join(root_dir, 'XSub', 'val'))]
    # xview_train_list = [item.split('.')[0] for item in os.listdir(os.path.join(root_dir, 'XView', 'train'))]
    # xview_val_list = [item.split('.')[0] for item in os.listdir(os.path.join(root_dir, 'XView', 'val'))]

    train_val_ratio = 0.7
    files_list = [item.split('.')[0] for item in os.listdir(os.path.join(root_dir, 'clips'+percentage))]
    subs_list = list(set([int(item.split('_')[1].replace('p', '')) for item in files_list]))
    # cams_list = list(set([int(item.split('_')[-2]) for item in files_list]))
    subs_train_list, subs_val_list = subs_list[:int(train_val_ratio*len(subs_list))], subs_list[int(train_val_ratio*len(subs_list)):]
    # cams_train_list, cams_val_list = cams_list[:int(train_val_ratio*len(cams_list))], cams_list[int(train_val_ratio*len(cams_list)):]
    xsub_train_list = [item for item in files_list if int(item.split('_')[1].replace('p', '')) in subs_train_list]
    xsub_val_list = [item for item in files_list if int(item.split('_')[1].replace('p', '')) in subs_val_list]
    xview_train_list = [item for item in files_list if int(item.split('_')[-2]) in [2, 3]]
    xview_val_list = [item for item in files_list if int(item.split('_')[-2]) in [1]]
    print(len(xsub_train_list), len(xsub_val_list), len(xview_train_list), len(xview_val_list))

    # os.makedirs(os.path.join(new_dir, 'xsam_train'+percentage), exist_ok=True)
    # os.makedirs(os.path.join(new_dir, 'xsam_val'+percentage), exist_ok=True)
    os.makedirs(os.path.join(new_dir, 'xsub_train'+percentage), exist_ok=True)
    os.makedirs(os.path.join(new_dir, 'xsub_val'+percentage), exist_ok=True)
    os.makedirs(os.path.join(new_dir, 'xview_train'+percentage), exist_ok=True)
    os.makedirs(os.path.join(new_dir, 'xview_val'+percentage), exist_ok=True)
    # xsam_train_file = open(os.path.join(new_dir, 'xsam_train{}_list_videos.txt'.format(percentage)), 'w')
    # xsam_val_file = open(os.path.join(new_dir,'xsam_val{}_list_videos.txt'.format(percentage)), 'w')
    xsub_train_file = open(os.path.join(new_dir,'xsub_train{}_list_videos.txt'.format(percentage)), 'w')
    xsub_val_file = open(os.path.join(new_dir,'xsub_val{}_list_videos.txt'.format(percentage)), 'w')
    xview_train_file = open(os.path.join(new_dir,'xview_train{}_list_videos.txt'.format(percentage)), 'w')
    xview_val_file = open(os.path.join(new_dir,'xview_val{}_list_videos.txt'.format(percentage)), 'w')

    for vclip in os.listdir(os.path.join(root_dir, 'clips'+percentage)):
        clip_name = vclip.split('.')[0]
        class_label = clip_name[-1]
        # if clip_name in xsam_train_list:
        #     xsam_train_file.write(os.path.join(new_dir, 'xsam_train'+percentage, vclip) + ' ' + class_label + '\n')
        #     shutil.copy(os.path.join(root_dir, 'clips'+percentage, vclip), os.path.join(new_dir, 'xsam_train'+percentage))
        # if clip_name in xsam_val_list:
        #     xsam_val_file.write(os.path.join(new_dir, 'xsam_val'+percentage, vclip) + ' ' + class_label + '\n')
        #     shutil.copy(os.path.join(root_dir, 'clips'+percentage, vclip), os.path.join(new_dir, 'xsam_val'+percentage))
        if clip_name in xsub_train_list:
            xsub_train_file.write(os.path.join(new_dir, 'xsub_train'+percentage, vclip) + ' ' + class_label + '\n')
            shutil.copy(os.path.join(root_dir, 'clips'+percentage, vclip), os.path.join(new_dir, 'xsub_train'+percentage))
        if clip_name in xsub_val_list:
            xsub_val_file.write(os.path.join(new_dir, 'xsub_val'+percentage, vclip) + ' ' + class_label + '\n')
            shutil.copy(os.path.join(root_dir, 'clips'+percentage, vclip), os.path.join(new_dir, 'xsub_val'+percentage))
        if clip_name in xview_train_list:
            xview_train_file.write(os.path.join(new_dir, 'xview_train'+percentage, vclip) + ' ' + class_label + '\n')
            shutil.copy(os.path.join(root_dir, 'clips'+percentage, vclip), os.path.join(new_dir, 'xview_train'+percentage))
        if clip_name in xview_val_list:
            xview_val_file.write(os.path.join(new_dir, 'xview_val'+percentage, vclip) + ' ' + class_label + '\n')
            shutil.copy(os.path.join(root_dir, 'clips'+percentage, vclip), os.path.join(new_dir, 'xview_val'+percentage))
    
    # xsam_train_file.close()
    # xsam_val_file.close()
    xsub_train_file.close()
    xsub_val_file.close()
    xview_train_file.close()
    xview_val_file.close()


if __name__ == '__main__':
    '''
    trim the videos with percentage
    '''
    # input_dir = '/home/ips-gpu-server/tianyuwang/har-dataset/MARC-Flex/clipped_video/scenario_s/disassembly/video_clips/clips'
    # start_percentage = 0.0
    # end_percentage = 25.0
    # trim_video(input_dir, start_percentage, end_percentage)
    # exit()
    
    '''
    format the mmaction dataset
    '''
    root_dir = '/home/ips-gpu-server/tianyuwang/har-dataset/MARC-Flex/clipped_video/scenario_s/disassembly/video_clips'
    new_dir = '/home/ips-gpu-server/tianyuwang/mmaction2/data/marcflex-rgb/disassembly/static'
    make_video_dataset(root_dir=root_dir, new_dir=new_dir, percentage='25')