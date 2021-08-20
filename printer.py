import os
import tempfile
import time

import win32api
import win32print
from tkinter import filedialog

def printer_loading(filename):
    # open(filename, "r")
    win32api.ShellExecute(
        0,
        "print",
        filename,
        #
        # If this is None, the default printer will
        # be used anyway.
        #
        '/d:"%s"' % win32print.GetDefaultPrinter(),
        ".",
        0
    )

    time.sleep(20)

# printer_loading(r'F:\打印\469034200003JC00453陈功强\01不动产权籍调查表.docx')


def print_family(path):
    printer_loading(os.path.join(path, '01不动产权籍调查表.docx'))
    printer_loading(os.path.join(path, '02房屋基本信息调查表.docx'))
    printer_loading(os.path.join(path, '03宗地图.pdf'))
    printer_loading(os.path.join(path, '04界址点成果表.docx'))
    printer_loading(os.path.join(path, '469034200003JC00453F00010001房屋平面图.pdf'))
    printer_loading(os.path.join(path, '06土地权属来源证明.docx'))
    printer_loading(os.path.join(path, '07保证质量安全具结书.docx'))
    printer_loading(os.path.join(path, '08不动产登记申请表.docx'))
    printer_loading(os.path.join(path, '09不动产登记审批表.docx'))
    printer_loading(os.path.join(path, '10农村宅基地使用权申请申批表.docx'))
    printer_loading(os.path.join(path, '11房屋实体照片.docx'))


if __name__ == '__main__':
    path = filedialog.askdirectory()
    pl = os.listdir(path)

    for p in pl:
        p = os.path.join(path, p)
        if os.path.isdir(p):
            print_family(p)

