import os
from shutil import copy




def copy_one_dir(path):
    # path = r'C:\Users\sc\Documents\飞行者科技\房地一体\测试数据\46坡田仔\02电子档案\469034200002JC00001陈昌盛'
    print('os.path.split(path)', os.path.split(path))
    new_path = os.path.join(os.path.split(path)[0] + 'json', os.path.split(path)[1])
    print('new_path', new_path)
    try:
        os.makedirs(new_path)
    except OSError as error:
        print("Directory '%s' can not be created" % new_path)

    path_list = os.listdir(path)
    print(path_list)
    for p in path_list:
        f_p = os.path.join(path, p)
        if os.path.isfile(f_p) and '.json' in f_p:
            print(p)
            copy(f_p, os.path.join(new_path, p))


def copy_multi_dir(path):
    path_list = os.listdir(path)
    for p in path_list:
        f_p = os.path.join(path, p)
        if os.path.isdir(f_p):
            print(f_p)
            copy_one_dir(f_p)


if __name__ == '__main__':
    # print(save_json(r'C:\Users\sc\Documents\飞行者科技\房地一体\测试数据\46坡田仔\02电子档案json\469034200002JC00001陈昌盛json\2-2户口本.json'))
    # copy_one_dir(r'C:\Users\sc\Documents\飞行者科技\房地一体\测试数据\46坡田仔\02电子档案\469034200002JC00001陈昌盛')
    copy_multi_dir(r'C:\Users\sc\Documents\飞行者科技\房地一体\02电子档案')
