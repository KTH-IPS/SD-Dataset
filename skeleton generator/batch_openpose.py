import argparse
import os
import sys

"""
This generator is used for processing multiple videos in a folder and only one video for one each label, by openpose, from video to skeleton
Please replace "Your Path to Openpose" and "Your Path to Video Clips" before use!
"""

openpose_path = "Your Path to Openpose"
openpose_bin = 'Your Path to Openpose/build/examples/openpose/openpose.bin'
VIDEO_FOLDER = "Your Path to Video Clips"


def run_openpose(video_path, save=None, custom_model=False, custom_model_pose=False, hand=False, show=False, norm=False,
                 two_people=True):
    write_json = ''
    display = ''
    option_hand = ''
    keypoint_scale = None
    max_people = None
    if save != None:
        write_json = '--write_json %s' % (save)
    if custom_model:
        model_folder = '--model_folder Your Path to Openpose/models/'
    if custom_model_pose:
        model_pose = '--model_pose COCO'
    if hand:
        option_hand = '--hand'
    if not show:
        display = '--display 0 --render_pose 0'
    if norm:
        keypoint_scale = '--keypoint_scale 3'
    if two_people:
        max_people = '--number_people_max 2'

    openpose = openpose_bin + ' '
    option = '--video %s %s %s %s %s %s %s %s' % (video_path, option_hand, model_folder, model_pose, write_json,
                                                        display, keypoint_scale, max_people)

    os.system(openpose + option)  # run a shell command

dirname = os.path.dirname(VIDEO_FOLDER) + '_skeleton/'
if not os.path.exists(dirname):
    os.mkdir(dirname)

for (root, dirs, files) in os.walk(VIDEO_FOLDER):
    print((root, dirs, files))
    index = 0
    for fname in files:
        run_openpose(video_path=os.path.join(root, fname),
                     save=dirname + fname.split('.')[0],
                     custom_model=True,
                     custom_model_pose=True,
                     show=False,
                     norm=False,
                     two_people=False)
        index += 1
        print("[%d/%d] %s has been processed by openpose successfully!" % (index, len(files), fname.split('.')[0]))
print("ALL DONE!")
sys.exit()
