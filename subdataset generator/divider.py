import os
import shutil
import random
import numpy as np

# This script is used for dividing the data into training subset and testing subset. 

DATA_PATH = "Your Path to the Complete Procedural Skeleton Data"
TRAIN_FOLDER = "Your Path to the Targeted Training Set Folder"
VAL_FOLDER = "Your Path to the Targeted Testing Set Folder"

data_list = os.listdir(DATA_PATH)
print(len(data_list))

for file in data_list:
    rd = np.random.rand()
    if rd > 0.9:
        shutil.copyfile(DATA_PATH+file, VAL_FOLDER+file)
    else:
        shutil.copyfile(DATA_PATH+file, TRAIN_FOLDER+file)

print("ALL DONE!")
