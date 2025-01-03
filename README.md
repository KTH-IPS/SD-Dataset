## Introduction
This is the official repository for MARC-Flex Dataset with Python scripts.

Download the dataset here: URL TO BE RESEALSED AFTER REVIEW.

## Pipeline
The whole pipeline is described as follow. If you want to build a new dataset, or enrich this dataset, it is easy to follow this pipeline.
1. Record raw videos with single or multiple cameras. Raw video frames will be generated at the same time.
2. Clip the raw videos into procedural ones using the anchors. Scripts to clip the video are in **video clipper**.
3. Generate skeleton frames using any skeleton estimator (OpenPose in this dataset), for instance the codes in **skeleton generator**.
4. Merge the skeleton frames into procedural skeketon data using scripts from **skeleton generator**.
5. Build the training and testing subdataset using scripts in **subdataset generator**. X-Sample, X-Subject, and X-Sensor can be used for different research target.

## Folders
 - **video clipper**

    This folder contains scripts to clip the raw video into procedural ones. **procedure_anchors.csv** is required here.
    If you want to use own data, you need to have the **procedure_anchors.csv** by yourself manually. For this dataset, we used Premiere Pro to determime the data in **procedure_anchors.csv**.
 - **skeleton generator**
    
    This folder contains scripts generating skeleton from video and merging the individual skeleton frames into procedural ones.
 - **subdataset generator**
    
    This folder contains scripts dividing the training and testing subsets, and the .npy, .pkl files for network training.

## How to use
 - **video clipper**
    - **clipper.py**

        This script is used for clipping the raw videos into procedural ones, accoring to the manual procedures. **procedure_anchors.csv** is required here.
 - **skeleton generator**
    - **batch_openpose.py**

        This script is used for generating skeleton data from video, no matter raw video or clipped video.
        To use OpenPose as the skeleton estimator, you need to install OpenPose on the computer you are going to use with this script. In this project, we used Openpose 1.6.0 and 1.7.0. There is no specific requirement for the Openpose version.
        In MARC-Flex, we use clipped videos in "procedural video" as the input. The output of this script is saved into "skeleton frames" folder.
    - **dict.py**

        This file contains dictionaries of the procedure names. They will be used in merge_customdata_asbly.py and merge_customdata_dsbly.py.
    - **merge.py**

        This script is the template script for merge_customdata_asbly.py and merge_customdata_dsbly.py. Please refer to them for more details.
    - **merge_customdata_asbly.py**

        This script is the script to merge skeleton frames in several folders to procedural skeleton sequence.
        It needs to be noted that the origanlly generated .json file of skeleton frames only contains skeleton data of single frame. This script is to merge all the skeleton data of one manual procedure into single .json file.
        This script requires the dictionary from **dict.py**. For assembly and disassembly data, use the dictionary accordingly.
        As for the nomalization, set the Boolean normalization to True or False. Normalization is not strictly required, because you can conduct it anywhere before building the final training and testing set. But normalization is strongly reconmmended, for better model generalization on different cameras.
    - **merge_customdata_dsbly.py**

        This script is similiar to **merge_customdata_asbly.py**, but is for disassembly data. Please refer to the note of **merge_customdata_asbly.py**.
 - **subdataset generator**
    - **divider.py**

        This script is used to divide the complete dataset into training and testing subset. Purposes like X-Sample, X-Subject, and X-Sensor need to be realized here.
    - **label_gen.py**

        This script is used to generate the label for the training and testing subset.
    - **npy_gen.py**

        This script build the .npy and .pkl for data and labels in the training subset and the testing subset. The .npy and the .pkl files are used to train the deep neural networks with PyTorch or TensorFlow.

    - **skeleton_mmaction.py**

        This script is about how to build the subdatased of the skeleton data for mmpose training.

    - **video_mmaction.py**
        This script is about how to build the subdatased of the RGB data for mmpose training.


**Note**: 

The camera recording program used is from https://github.com/xuanma/pyqt5_camera_new. 

Please refer to the notes in all the scripts for details that are not included in README.md.

Please refer to our paper for more details like the naming rules.


## License
Shield: [![CC BY-NC 4.0][cc-by-nc-shield]][cc-by-nc]

This work is licensed under a
[Creative Commons Attribution-NonCommercial 4.0 International License][cc-by-nc].

[![CC BY-NC 4.0][cc-by-nc-image]][cc-by-nc]

[cc-by-nc]: https://creativecommons.org/licenses/by-nc/4.0/
[cc-by-nc-image]: https://licensebuttons.net/l/by-nc/4.0/88x31.png
[cc-by-nc-shield]: https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg
