import argparse
import os
import json
import sys

# This script is used for generating data label to json files given the skeleton data. 
# Often, the input folder is either the training set or the testing set.

MERGED_SKELETON_FOLDER = "Your Path to the Training Set or the Testing Set"
summary = {}

for (root, dirs, files) in os.walk(MERGED_SKELETON_FOLDER):
    for fname in files:
        [name, ext] = os.path.splitext(fname)
        if ext != '.json':
            continue

        with open(os.path.join(root, fname)) as f:
            data = json.load(f)

        has_skeleton = (data["data"] != [])
        entry = {"has_skeleton": has_skeleton, "label": data["label"], "label_index": data["label_index"]}
        summary[name] = entry

output_json = os.path.dirname(MERGED_SKELETON_FOLDER)+"_label.json"
print(output_json)
with open(output_json, 'w') as output:
    json.dump(summary, output, indent=4, sort_keys=True)
print("Label Gen Done.")
sys.exit()
