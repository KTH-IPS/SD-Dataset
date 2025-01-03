import os
import csv
import moviepy.editor as mv

VIDEO_PATH = "Your Path to All the Raw Videos"
FRAME_INFO = "Your Path to procedure_anchors.csv"
TIME_INFO = "Your Path to All the Raw Video Frames"
CLIPS_PATH = "Your Path to Store All the Clips"
NUM_CLIPS_PER_VIDEO = 9
name_dict = {"scenario": 0, "subject": 1, "episode": 2, "task": 3, "date": 4, "time": 5, "camera": 6}


# sort by subject number
def video_order(file_name):
    return int(file_name.split(".")[0].split("_")[name_dict["subject"]][1:])


with open(FRAME_INFO, mode='r') as f:
    reader = csv.reader(f)
    frame_info = list(reader)

    video_list = os.listdir(VIDEO_PATH)
    video_list.sort(key=video_order)

    for i, video in enumerate(video_list):

        print("Video" + str(i+1))
        video_type = video.split(".")[-1]
        video_name = video.split(".")[0].split("_")
        file_full_name = video.split(".")[0]
        assert file_full_name == frame_info[i][0]
        with open(TIME_INFO + file_full_name + '.txt', mode='r') as ti:
            time_info = ti.readlines()
            print(time_info)
            for k in range(0, NUM_CLIPS_PER_VIDEO * 2 - 1, 2):
                head_index = int(frame_info[i][k + 1])
                foot_index = int(frame_info[i][k + 2])
                head = time_info[head_index].split("\t")[0]
                foot = time_info[foot_index].split("\t")[0]
                clip_no = int((k + 2) / 2)
                print("Clip" + str(clip_no))
                print("head=", head)
                print("foot=", foot)
                clip = mv.VideoFileClip(VIDEO_PATH + video).subclip(head, foot)
                video_clipped = mv.CompositeVideoClip([clip])
                video_clipped.write_videofile(CLIPS_PATH + file_full_name + "_c" + str(clip_no) + '.' + video_type, codec='mpeg4', bitrate="18432k")
                print(VIDEO_PATH + video)
                print(CLIPS_PATH + file_full_name + "_c" + str(clip_no) + '.' + video_type)

    print("ALL DONE!")


