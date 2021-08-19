import os

from PIL import Image
from tkinter import filedialog


def cut_half_image(path):
    img = Image.open(path)
    if img.size[0] < 2000 or img.size[1] < 2000:
        print('cut_half_image: The width of the img is less than 2000, no cut')
        return
    print(img.size)
    print(type(img.size))
    print(img.size[0])
    if img.size[0] > img.size[1]:
        cropped = img.crop((0, 0, img.size[0] / 2, img.size[1]))  # (left, upper, right, lower)
    else:
        cropped = img.crop((0, 0, img.size[0], img.size[1] / 2))
    cropped.save(path)


def cut_multi_image(pathA):
    # pathA = filedialog.askdirectory()
    dir_list = os.listdir(pathA)

    for m_dir in dir_list:
        full_path = os.path.join(pathA, m_dir)
        print(full_path)
        filename = os.path.join(full_path, '1-1身份证明.jpg')
        if os.path.exists(filename):
            cut_half_image(filename)  # 对半切图片


if __name__ == '__main__':
    p = filedialog.askopenfilename()
    cut_half_image(p)
    # p = filedialog.askdirectory()
    # cut_multi_image(p)
