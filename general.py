import os
from config import *

# Each website is in a folder depending on status
def create_project_dir():
    if not os.path.exists(CRAWLED_PATH):
        print('Creating directory : ['+CRAWLED_PATH+']')
        os.makedirs(CRAWLED_PATH)
    if not os.path.exists(QUEUE_PATH):
        print('Creating directory : ['+QUEUE_PATH+']')
        os.makedirs(QUEUE_PATH)

# Create project file inside queue and crawled folders (if not created)
def create_data_files():
    create_project_dir()
    if not os.path.isfile(QUEUE_FILE):
        write_file(QUEUE_FILE, HOMEPAGE)
    if not os.path.isfile(CRAWLED_FILE):
        write_file(CRAWLED_FILE, '')


# Create a new file
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


# Add data onto an existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


# Delete the contents of a file
def delete_file_contents(path):
    open(path, 'w').close()


# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# Iterate through a set, each item will be a line in a file
def set_to_file(links, file_name):
    with open(file_name,"w") as f:
        for l in sorted(links):
            f.write(l+"\n")
