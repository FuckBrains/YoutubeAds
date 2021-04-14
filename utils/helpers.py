import re
import datetime
import random



def removeprefix(instr, prefix):
    if instr.startswith(prefix):
        return instr[len(prefix):]
    else:
        return instr[:]

def removesuffix(instr, suffix):

    if suffix and instr.endswith(suffix):
        return instr[:-len(suffix)]
    else:
        return instr[:]

def update_test_id():
    test_file = open('test_id.txt', 'r')
    for line in test_file:
        test_num = int(line)
    # test_num = int(test_file.readline())

    test_file.close()

    test_file = open('test_id.txt', 'w')
    test_file.write(str(test_num + 1))
    test_file.close()

    return test_num + 1


def get_test_id():
    d = datetime.datetime.now()
    test_str = '{date:%Y_%m_%d_%H_%M_%S}'.format(date = d)
    test_id = int('{date:%Y%m%d%H%M%S}'.format(date = d))

    return test_id, test_str

def get_video_list(filename, num_videos):
    infile = open(filename, 'r')
    video_list = []
    for line in infile:
        if line.strip() == "#NAME?":
            continue
        video_list.append(line.strip())

    infile.close()
    print(len(video_list))
    print(video_list[:num_videos])

    random.shuffle(video_list)
    print(video_list[:num_videos])

    return video_list[:num_videos]

def get_descr_link(link_text):
    search = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

    temp = removeprefix(link_text, "https://www.youtube.com/")

    temp = temp.replace("%3A", ":")
    temp = temp.replace("%2F", "/")

    if re.search(search,temp) is None:
        re.search(search,temp)
        return link_text
    else:
        url = re.search(search,temp)[0]

        return url