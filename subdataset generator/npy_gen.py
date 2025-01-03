import os
import sys
import pickle
import argparse
import numpy as np
from numpy.lib.format import open_memmap

# This script build the .npy and .pkl for data and labels in the training subset and the testing subset.
# The .npy and the .pkl files are used to train the deep neural networks with PyTorch or TensorFlow.
# Replace "Your Path to Folder Containing the Traininh Subset and the Testing Subset" and 
# "Your Path to Store the .npy, .pkl, and .json Files" before use!

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from feeder.feeder_custom_dataset import Feeder_custom_dataset

toolbar_width = 30


def print_toolbar(rate, annotation=''):
    sys.stdout.write("{}[".format(annotation))
    for i in range(toolbar_width):
        if i * 1.0 / toolbar_width > rate:
            sys.stdout.write(' ')
        else:
            sys.stdout.write('-')
        sys.stdout.flush()
    sys.stdout.write(']\r')


def end_toolbar():
    sys.stdout.write("\n")


def gendata(
        data_path,
        label_path,
        data_out_path,
        label_out_path,
        num_person_in=1,  # observe the first 5 persons
        num_person_out=1,  # then choose 2 persons with the highest score
        max_frame=300):

    # init a feeder
    feeder = Feeder_custom_dataset(
        data_path=data_path,
        label_path=label_path,
        num_person_in=num_person_in,
        num_person_out=num_person_out,
        window_size=max_frame,
        debug=False)

    sample_name = feeder.sample_name
    print("sample_name", sample_name)
    sample_label = []

    fp = open_memmap(
        data_out_path,
        dtype='float32',
        mode='w+',
        shape=(len(sample_name), 3, max_frame, 18, num_person_out))  # data shape (N, C, T, V, M)

    # MAIN LOOP
    for i, s in enumerate(sample_name):
        data, label = feeder[i]
        print_toolbar(i * 1.0 / len(sample_name),
                      '({:>5}/{:<5}) Processing data: '.format(
                          i + 1, len(sample_name)))
        fp[i, :, 0:data.shape[1], :, :] = data
        sample_label.append(label)

    with open(label_out_path, 'wb') as f:
        pickle.dump((sample_name, list(sample_label)), f)


if __name__ == '__main__':
    # get data_path and the out_folder for generated dataset
    parser = argparse.ArgumentParser(
        description='Subset builder')
    parser.add_argument(
        '--data_path', default='Your Path to Folder Containing the Traininh Subset and the Testing Subset')
    parser.add_argument(
        '--out_folder', default='Your Path to Store the .npy, .pkl, and .json Files')
    arg = parser.parse_args()

    part = ['train', 'val']

    # concatenate the final path for data and label, train and val set
    for p in part:
        data_path = '{}/{}'.format(arg.data_path, p)
        label_path = '{}/{}_label.json'.format(arg.data_path, p)
        data_out_path = '{}/{}_data.npy'.format(arg.out_folder, p)
        label_out_path = '{}/{}_label.pkl'.format(arg.out_folder, p)

        if not os.path.exists(arg.out_folder):
            os.makedirs(arg.out_folder)

        # call the core generate method, from merged json to npy
        gendata(data_path, label_path, data_out_path, label_out_path)

    print("ALL DONE!")

