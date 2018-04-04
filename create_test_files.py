#!/usr/bin/python

import os
import sys
import time

# Generate executable with pyinstaller --onefile connect.py. Install pyinstaller with sudo pip install pyinstaller

ARGS = 4

if len(sys.argv) != ARGS+1:
    print 'This command creates test files with some text'
    print 'Usage: create_test_files num_files num_folders depth root_folder'
    sys.exit(1)

NUM_FILES = int(sys.argv[1])
NUM_FOLDERS = int(sys.argv[2])
DEPTH = int(sys.argv[3])
ROOT_FOLDER = sys.argv[4]


def create_root_folder():
    if ROOT_FOLDER != '.' and not os.path.exists(ROOT_FOLDER):
        os.makedirs(ROOT_FOLDER)

def get_name_folder(depth, root_folder):
    output = list()
    for x in range(NUM_FOLDERS):
        output.append('{}/dir_{}_{}'.format(root_folder, depth, x+1))
    return output

def get_all_folders():
    output = list()
    folders_old = list()

    for x in range(1, DEPTH+1):
        if len(folders_old) == 0:
            folders = get_name_folder(x, ROOT_FOLDER)
            output.extend(folders)
            folders_old = folders
        else:
            tmp = list()
            for f in folders_old:
                folders = get_name_folder(x, f)
                tmp.extend(folders)
            output.extend(tmp)
            folders_old = tmp

    return output

start = time.time()

create_root_folder()
folders_to_create = get_all_folders()

num_folders = len(folders_to_create)
print 'Creating {} folders and {} test files ...'.format(num_folders, num_folders*NUM_FILES)

for folder in folders_to_create:
    if not os.path.exists(folder):
        os.makedirs(folder)

        for x in range(1, NUM_FILES+1):
            open('{}/file{}.txt'.format(folder, x), 'w').write('some text')

elapsed_time = round((time.time() - start), 2)
print 'Processing time: {} sec'.format(elapsed_time)


