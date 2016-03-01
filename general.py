import os


# Each website is a separate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


# Remove queue and crawled files (if exist)
def remove_data_files(project_name):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'
    remove_file(queue)
    remove_file(crawled)


def remove_file(file):
    try:
        os.remove(filename)
    except OSError:
        pass


# Create queue and crawled files (if not created)
def create_data_files(project_name, base_url):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')


# Create a new file
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


# Read a file and convert each line to set items
def file_to_set(file_name):
    with open(file_name, 'rt') as f:
        results = {line.replace('\n', '') for line in f}
    return results


# Iterate through a set, each item will be a line in a file
def set_to_file(links, file):
    with open(file, 'w') as f:
    for link in sorted(links):
        f.write(link + '\n')
