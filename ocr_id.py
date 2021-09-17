# coding=utf-8
import datetime
import io
import sys
import json
import base64
import requests
import os
from PIL import Image
from tkinter import filedialog

# 保证兼容python2以及python3
import cut_image

list_create_time = []
test_list = []

IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode

# 防止https证书校验不正确
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# use your own api key
API_KEY = 'YOUR API KEY'
# use your own secret key
SECRET_KEY = 'YOUR SECRET KEY'

OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"

"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'

msg_error = []


def fetch_token():
    """
        获取token
    """
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    if (IS_PY3):
        result_str = result_str.decode()

    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print('please overwrite the correct API_KEY and SECRET_KEY')
        exit()


def read_file(image_path):
    """
        读取文件
    """
    f = None
    try:
        f = open(image_path, 'rb')
        return f.read()
    except:
        print('read image file fail')
        return None
    finally:
        if f:
            f.close()


def request(url, data):
    """
        调用远程服务
    """
    req = Request(url, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        if (IS_PY3):
            result_str = result_str.decode()
        return result_str
    except  URLError as err:
        print(err)


def get_householder_name(filename, access_token):
    """
    通过百度api，获取身份证json，
    如果有response， 保存json在对应的路径，并返回未经处理的字典;
    如果没有，返回 None

    :param access_token: 百度api的access token
    :param filename: 图片路径
    :return: 未经处理的字典 或 None
    """
    if not os.path.exists(filename):
        print("{} 缺失身份证照片，无法识别。".format(filename))
        msg_error.append("{} 缺失身份证照片，无法识别。".format(get_code_name_number(filename)))
        return
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/idcard"
    # 二进制方式打开图片文件
    my_file = open(filename, 'rb')
    img = base64.b64encode(my_file.read())

    params = {"id_card_side": "front", "image": img}
    # access_token = fetch_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        dict1 = response.json()
        # print(dict1)
        out_file = open(filename_jpg_to_json(filename), "w")
        json.dump(dict1, out_file, indent=6, ensure_ascii=False)
        # print('type', type(dict1))
        out_file.close()
        return dict1
    else:
        msg_error.append('{} 身份证识别没有回复'.format(get_code_name_number(filename)))
        print("No response!")


def get_householder_book(filename, access_token):
    """
    通过百度api，获取户口本json，
    如果有response， 保存json在对应的路径，并返回未经处理的字典;
    如果没有，返回 None

    :param access_token: 百度api的access_token
    :param filename: 图片路径
    :return: 未经处理的字典 或 None
    """
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/household_register"
    # 二进制方式打开图片文件
    f = open(filename, 'rb')
    img = base64.b64encode(f.read())
    img = compress_image_bs4(img)
    params = {"image": img}
    # access_token = fetch_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    dict1 = {}
    if response:
        dict1 = response.json()
        # print(dict1)
        out_file = open(filename_jpg_to_json(filename), "w")
        json.dump(dict1, out_file, indent=6, ensure_ascii=False)
        # print('type', type(dict1))
        out_file.close()
        return dict1
    else:
        msg_error.append('{} 户口本识别没有回复'.format(get_code_name_number(filename)))
        return dict1


def compress_image_bs4(b64, mb=2048, k=0.9):
    """压缩base64的图片。不改变图片尺寸压缩到指定大小

    :param k: 每次压缩率？
    :param b64: 原来的base64图片
    :param mb: 压缩目标，KB
    :return: 压缩文件地址，压缩文件大小
     """
    f = base64.b64decode(b64)
    with io.BytesIO(f) as im:
        o_size = len(im.getvalue()) // 1024
        if o_size <= mb:
            return b64
        im_out = im
        while o_size > mb:
            img = Image.open(im_out)
            x, y = img.size
            out = img.resize((int(x * k), int(y * k)), Image.ANTIALIAS)
            im_out.close()
            im_out = io.BytesIO()
            out.save(im_out, 'jpeg')
            o_size = len(im_out.getvalue()) // 1024
        b64 = base64.b64encode(im_out.getvalue())
        im_out.close()
        return str(b64, encoding='utf8')


def get_one_dict(member_dict):
    """
    从原始的户口本json转为的字典中，获取姓名，关系，身份证号码，生成并返回新的字典

    :param member_dict:原始的户口本json转为的字典
    :return:由姓名，关系，身份证号码组成的字典
    """
    name = get_atr(member_dict, 'Name')
    relationship = get_atr(member_dict, 'Relationship')
    cardNo = get_atr(member_dict, 'CardNo')
    return {'姓名': name, '关系': relationship, '身份证号码': cardNo}


def get_atr(dict_a, string):
    """
    从原始的户口本json转为的字典中，获取string对应的value
    :param dict_a:原始的户口本json转为的字典
    :param string:key
    :return:value
    """
    words = 'words'
    if dict_a is not None and dict_a.get('words_result') is not None and dict_a.get('words_result').get(
            string) is not None:
        return dict_a.get('words_result').get(string).get(words)


def get_dict_from_json_file(path, need_replace=True):
    """
    从路径为path的json文件中，载入并返回字典。如果路径不存在，返回None
    :param need_replace: 是否需要替换jpg为json 默认为True
    :param path:json文件的路径
    :return:路径存在时返回字典，不存时返回None
    """
    if need_replace:
        path = filename_jpg_to_json(path)

    print('get_dict_from_json_file.path', path)
    if not os.path.exists(path):
        print('没有' + path)
        return
    with open(path, 'r') as f:
        print(path)
        my_dict = json.loads(f.read())
        print(my_dict)
        return my_dict


def get_code_name_number(path):
    """
    从E:/照片核对/礼亭4/02电子档案\\110000001001JC00001郭团结 得到 00001郭团结 2-1户口本.jpg

    :param path: 路径
    :return: 结果
    """
    return os.path.split(os.path.split(path)[0])[1][14:] + ' ' + os.path.split(path)[1]


def get_family(village_name, is_http=False):
    """
    使用百度api或保存的json文件，生成所选文件夹（一般为"02电子档案"）中每个家庭对应的字典，
    并将各个字典以json形式保存在程序根目录中，然后将字典组成数字。
    如果使用百度api，还会将接收的原始json文件保存在json文件夹中（一般为"02电子档案json"）

    :param village_name: 村小组名称
    :param is_http: 是否使用百度api。若为否，则读取选择的图片文件夹所对应的json文件夹中的json文件
    :return: 一个数组，每个元素都是一个家庭的字典
    """
    string = ''
    to_print = 'ocr识别：请选择[02电子档案]文件夹' if is_http else '本地数据：请选择[02电子档案]文件夹'
    pathA = filedialog.askdirectory(title=to_print)
    if pathA == '':
        print(to_print)
        return None
    dir_list = os.listdir(pathA)
    mylist = []
    count_family = 0
    create_time = datetime.datetime.now()
    string = village_name + create_time.strftime("%Y-%m-%d %H-%M-%S")
    access_token = fetch_token()
    # print('ocr_id.dir_list', dir_list)

    for m_dir in dir_list:

        count_family += 1
        full_path = os.path.join(pathA, m_dir)
        code_parcel = m_dir[0:19]
        name_right_man = m_dir[19:]

        if os.path.exists(os.path.join(full_path, '1-1身份证明.jpg')):
            cut_image.cut_half_image(os.path.join(full_path, '1-1身份证明.jpg'))  # 对半切图片

        if is_http:
            dict_id_card = get_householder_name(os.path.join(full_path, '1-1身份证明.jpg'), access_token)
        else:
            dict_id_card = get_dict_from_json_file(os.path.join(full_path, '1-1身份证明.jpg'))
        # hh_name = get_atr(dict_id_card, '姓名')
        hh_id = get_atr(dict_id_card, '公民身份号码')
        family_dict = {'权利人姓名': name_right_man, '宗地号': code_parcel, '权利人证件编号': hh_id, '权利人关系': '无'}
        members_list = {}
        count = 0
        if os.path.isdir(full_path):
            print(full_path)
            files = os.listdir(full_path)
            members_list = []

            for index in range(len(files)):

                file = files[index]
                if '户口本.jpg' in file:
                    print(file)

                    f_file = os.path.join(full_path, file)
                    if is_http:
                        dict_a = get_householder_book(f_file, fetch_token())
                    else:
                        dict_a = get_dict_from_json_file(f_file)
                    dict_member = get_one_dict(dict_a)
                    if dict_member.get('姓名') is not None and dict_member.get('关系') is not None and dict_member.get(
                            '身份证号码') is not None and len(dict_member.get('身份证号码')) > 10:
                        count += 1
                        members_list.append(dict_member)
                        print("dict_member.get姓名", dict_member.get("姓名"))
                        print('name_right_man', name_right_man)
                        if dict_member.get('姓名') == name_right_man:
                            family_dict['权利人关系'] = dict_member.get('关系')
                    else:
                        msg_error.append('{} 户口本识别错误'.format(get_code_name_number(f_file)))
                        print('成员错误', f_file)
        if count < 1:
            print('when count < 1: ', name_right_man)
            members_list.append({"姓名": name_right_man, "关系": None, "身份证号码": hh_id})
            msg_error.append('{} 没有有效户口本'.format(full_path))

        family_dict['家庭成员'] = members_list
        family_dict['家庭总人数'] = len(members_list)

        time_path = os.path.join("json", string)
        if not os.path.exists(time_path):
            os.makedirs(time_path)
        out_file = open(os.path.join(time_path, str(count_family) + '.json'), "w")
        json.dump(family_dict, out_file, indent=6, ensure_ascii=False)
        mylist.append(family_dict)
        out_file.close()
        path_results = os.path.join('结果', string)
        if not os.path.exists(path_results):
            os.makedirs(path_results)
        write_error_msg(msg_error, os.path.join(path_results, r'识别错误信息.txt'))
    print('获取信息完成')
    return mylist, string


def get_family_id_card_only(village_name, is_http=False):
    """
    类似于get_family(is_http=False)，但只指挥获取身份证信息，字典和json文件也有所不同。

    :param village_name: 村小组名称
    :param is_http: is_http: 是否使用百度api。若为否，则读取选择的图片文件夹所对应的json文件夹中的json文件
    :return: 一个数组，每个元素都是一个家庭的字典（没有名为"家庭成员"的key）
    """
    access_token = fetch_token()
    pathA = filedialog.askdirectory()
    dir_list = os.listdir(pathA)
    mylist = []
    count_family = 0
    create_time = datetime.datetime.now()
    string = village_name + create_time.strftime("%Y-%m-%d %H-%M-%S")

    for m_dir in dir_list:
        count_family += 1
        full_path = os.path.join(pathA, m_dir)
        code_parcel = m_dir[0:19]
        name_right_man = m_dir[19:]

        cut_image.cut_half_image(os.path.join(full_path, '1-1身份证明.jpg'))    # 对半切图片

        if is_http:
            dict_id_card = get_householder_name(os.path.join(full_path, '1-1身份证明.jpg'), access_token)
        else:
            dict_id_card = get_dict_from_json_file(os.path.join(full_path, '1-1身份证明.jpg'))
        # hh_name = get_atr(dict_id_card, '姓名')
        hh_id = get_atr(dict_id_card, '公民身份号码')
        family_dict = {'权利人姓名': name_right_man, '宗地号': code_parcel, '权利人证件编号': hh_id}
        members_list = {}
        count = 0

        if count < 1:
            msg_error.append('{} 没有有效户口本'.format(full_path))
        else:
            family_dict['家庭成员'] = members_list
            family_dict['家庭总人数'] = len(members_list)

            time_path = os.path.join("json", string)
            if not os.path.exists(time_path):
                os.makedirs(time_path)
            out_file = open(os.path.join(time_path, str(count_family) + '.json'), "w")
            json.dump(family_dict, out_file, indent=6, ensure_ascii=False)
            mylist.append(family_dict)
            out_file.close()
    print('获取信息完成')
    return mylist, string


def get_family_from_json_folder(village_name):
    """
    通过选择原始json文件夹，生成家庭的字典

    :param village_name: 村小组的名称
    :return: (家庭的字典, 创建时间的字符串)
    """
    to_print = '本地数据json：请选择[02电子档案json]文件夹'
    pathA = filedialog.askdirectory(title=to_print)
    if pathA == '':
        print(to_print)
        return None
    dir_list = os.listdir(pathA)
    mylist = []
    count_family = 0
    create_time = datetime.datetime.now()
    string = village_name + create_time.strftime("%Y-%m-%d %H-%M-%S")

    for m_dir in dir_list:
        count_family += 1
        full_path = os.path.join(pathA, m_dir)
        code_parcel = m_dir[0:19]
        name_right_man = m_dir[19:]

        dict_id_card = get_dict_from_json_file(os.path.join(full_path, '1-1身份证明.json'), need_replace=False)
        hh_id = get_atr(dict_id_card, '公民身份号码')
        family_dict = {'权利人姓名': name_right_man, '宗地号': code_parcel, '权利人证件编号': hh_id, '权利人关系': '无'}
        members_list = {}
        count = 0

        if os.path.isdir(full_path):
            print(full_path)
            files = os.listdir(full_path)
            members_list = []

            if os.path.isdir(full_path):
                print(full_path)
                files = os.listdir(full_path)
                members_list = []

                for index in range(len(files)):
                    file = files[index]
                    if '户口本.json' in file:
                        print(file)
                        f_file = os.path.join(full_path, file)
                        dict_a = get_dict_from_json_file(f_file, need_replace=False)
                        dict_member = get_one_dict(dict_a)

                        if dict_member.get('姓名') is not None and dict_member.get('关系') is not None and dict_member.get(
                                '身份证号码') is not None and len(dict_member.get('身份证号码')) > 10:
                            count += 1
                            members_list.append(dict_member)
                            print("dict_member.get姓名", dict_member.get("姓名"))
                            print('name_right_man', name_right_man)
                            if dict_member.get('姓名') == name_right_man:
                                family_dict['权利人关系'] = dict_member.get('关系')
                        else:
                            msg_error.append('{} 户口本识别错误'.format(get_code_name_number(f_file)))
                            print('成员错误', f_file)

        if count < 1:
            print('when count < 1: ', name_right_man)
            members_list.append({"姓名": name_right_man, "关系": None, "身份证号码": hh_id})
            msg_error.append('{} 没有有效户口本'.format(full_path))

        family_dict['家庭成员'] = members_list
        family_dict['家庭总人数'] = len(members_list)

        time_path = os.path.join("json", string)
        if not os.path.exists(time_path):
            os.makedirs(time_path)
        out_file = open(os.path.join(time_path, str(count_family) + '.json'), "w")
        json.dump(family_dict, out_file, indent=6, ensure_ascii=False)
        mylist.append(family_dict)
        out_file.close()
        path_results = os.path.join('结果', string)
        if not os.path.exists(path_results):
            os.makedirs(path_results)
        write_error_msg(msg_error, os.path.join(path_results, r'识别错误信息.txt'))

    print('获取信息完成')
    return mylist, string


def read_jsons(path):
    """
    读取整理后的json文件夹中的json文件

    :param path: json文件夹
    :return: 读取json获得的字典的数组
    """
    my_list = []
    files = os.listdir(path)
    print(files)
    for file in files:
        if '.json' in file:
            full_path = os.path.join(path, file)
            print(file)
            print(full_path)
            with open(full_path, 'r') as f:
                temp = json.loads(f.read())
                print(temp)
                my_list.append(temp)
    return my_list


def write_error_msg(alist, apath):
    """
    将alist中的错误信息写入apath，若apath存在，则覆盖原有文件；若不存在，则创建新文件。

    :param alist: 元素为错误信息的数组
    :param apath: 保存的路径
    """
    with open(apath, 'w+') as f:
        for i in alist:
            f.write(i + '\n')


def filename_jpg_to_json(filename):
    """
    将图片的路径转为json的路径\n
    比如"02电子档案\\\\469028200204JC00001卓亚才\\\\1-1身份证明.jpg"\n
    转为"02电子档案json\\\\469028200204JC00001卓亚才\\\\1-1身份证明.json"

    :param filename:图片路径
    :return:json路径
    """
    up_one = os.path.split(filename)[0]
    up_two = os.path.split(up_one)[0]
    new_path = os.path.join(up_two + 'json', os.path.split(up_one)[1])
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    return os.path.join(new_path, os.path.split(filename)[1]).replace('.jpg', '.json')


if __name__ == '__main__':
    print("hello")
    # get_householder_book(r'C:\Users\sc\Documents\飞行者科技\房地一体\test\469034200002JC00001故意的\2-2户口本.jpg')
    # out_path = filedialog.askdirectory()

    # path = filedialog.askdirectory()
    # dir_list = os.listdir(path)
    # for m_dir in dir_list:
    #     full_path = os.path.join(path, m_dir)
    #     if os.path.isdir(full_path):
    #         print(full_path)
    #         dir_in_list = os.listdir(full_path)
    #         for i_dir in dir_in_list:
    #             print(i_dir)

    # print(create_json())

    # filename = filedialog.askopenfilename()
    # dict_id = get_householder_name(filename)
    # out_file = open("id.json", "w")
    # json.dump(dict_id, out_file, indent=6, ensure_ascii=False)

    # with open(r"C:\Users\sc\PycharmProjects\real_estate_integration/id.json", 'r') as load_f:
    #     load_dict = json.load(load_f)
    #
    # print(load_dict.get('words_result').get('公民身份号码').get('words'))
    # print(get_family())
    # write_error_msg(msg_error, r'识别错误信息.txt')
    # create_json()

    # path = filedialog.askdirectory()
    # read_jsons(path)
    # path = filedialog.askopenfilename()
    # get_householder_book(path)
