#-*-coding:utf-8-*-

import win32gui
import win32api
import win32con
import os
import ctypes
import time
import subprocess
import threading
import diskpart_one
from PIL import Image, ImageGrab

def get_child_windows(parent):
    """    获得parent的所有子窗口句柄


    Arguments:
        parent {int} -- 父窗口句柄号

    Returns:
        [list] -- 返回子窗口句柄列表
    """


    # if not parent:
    #     return
    hwndChildList = []
    win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd), hwndChildList)
    return hwndChildList

def get_all_child(tool="Untitled - ATTO Disk Benchmark"):

    """
    function:列出窗口所有子类，类型，名称
    """

    #tool = "Untitled - ATTO Disk Benchmark"
    hwnd = win32gui.FindWindow(None, tool)
    hwndChildList = get_child_windows(hwnd)
    print(hwndChildList)
    for k in hwndChildList:
        print("{}:{}:{}".format(win32gui.GetWindowText(k),win32gui.GetClassName(k),win32gui.GetWindowRect(k)))



def mouse_move(new_x, new_y):
    """移动鼠标

    Arguments:
        new_x {int} -- 横坐标
        new_y {int} -- 纵坐标
    """

    point = (new_x, new_y)
    win32api.SetCursorPos(point)

def mouse_click(x, y, cnt=1):
    """点击鼠标

    Arguments:
        x {int} -- 横坐标
        y {int} -- 纵坐标

    Keyword Arguments:
        cnt {int} -- 次数 (default: {1})
    """

    mouse_move(x, y)

    while cnt:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        cnt = cnt - 1

def keybd_single_char(input_key, idle=1):
    """键盘输入字符

    Arguments:
        input_key {str} -- 键盘字符

    Keyword Arguments:
        idle {int} -- 字符输入后等待时间 (default: {1})
    """

    input_key = ord(input_key)
    win32api.keybd_event(input_key, 0, 0, 0)
    win32api.keybd_event(input_key, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(idle)


def button_center(phwnd):
    """获取句柄中心点

    Arguments:
        phwnd {int} -- 句柄号

    Returns:
        int -- 中心点坐标
    """

    center_xy = win32gui.GetWindowRect(phwnd)
    center_x = ( center_xy[0] + center_xy[2] ) // 2
    center_y = ( center_xy[1] + center_xy[3] ) // 2
    print(center_xy)
    return center_x, center_y



def run_assd(target = "F"):
    """[summary]

    Keyword Arguments:
        target {str} -- [description] (default: {"F"})
    """


    tool = "AS SSD Benchmark 1.9.5986.35387"
    tool_path = r'start "aa" "D:\SSD performance\AS SSD Benchmark\AS SSD Benchmark.exe"'
    os.system(tool_path)
    time.sleep(5)
    #找到tool 所在的窗口
    hwnd = win32gui.FindWindow(None, tool)
    #设置assd窗口为焦点
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383,140,0,0, win32con.SWP_NOSIZE)


    hwndChildList = get_child_windows(hwnd)
    #磁盘选择窗口/磁盘名称窗口/开始按键
    disk_select = hwndChildList[10]
    disk_name = hwndChildList[25]
    #start_button = hwndChildList[24]
    write_aactime = hwndChildList[31]
    #write_aactime_init = win32gui.GetWindowText(write_aactime)
    disk_select_init = win32gui.GetWindowText(disk_name)
    #选择待测试磁盘
    xy = button_center(disk_select)
    mouse_click(xy[0], xy[1])
    time.sleep(0.5)
    keybd_single_char(target)
    mouse_click(xy[0], xy[1])

    #判断选择磁盘是否成功，若成功，当前磁盘名称应与init不一样

    disk_select_current = win32gui.GetWindowText(disk_name)

    if disk_select_init != disk_select_current:
        print('{0} start testing ! '.format(disk_select_current))
        #
        # 找到 start按键
        hwnd1= win32gui.FindWindowEx(hwnd, None, None, "Start")
        xy = button_center(hwnd1)
        mouse_move(xy[0], xy[1])
        #开始运行
        mouse_click(xy[0], xy[1])
        while True:

            write_aactime_current = win32gui.GetWindowText(write_aactime)
            flag = 0
            #判断当前是否Acc time write 是否 为0
            if write_aactime_current != "0.000 ms" :
                for cnt in range(0, 10):
                    if write_aactime_current != win32gui.GetWindowText(write_aactime):
                        print(write_aactime_current)
                        cnt
                        break
                    else:
                        flag = flag + 1
                        time.sleep(1)

            if flag == 10:
                break

        filename = "{}.png".format(tool)

        x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd)
        x1 = x1 + 7
        x2 = x2 - 9
        y2 = y2 - 8

        screenshot(filename= filename, position=(x1, y1, x2, y2,))
        print(write_aactime_current)
    else:
        pass


def screenshot(filename= "tmp123.png", position= None, filepath= None):
    """截图

    Keyword Arguments:
        filename {str} -- 文件名称 (default: {"tmp123.png"})
        position {tuble} -- 截图坐标 (default: {None})
        filepath {str} -- 文件路径 (default: {None})

    Raises:
        Exception -- Exception("Save screenshot failed!")
    """


    if filepath:
        pass
    else:
        filepath = os.getcwd()

    filename = os.path.join(filepath, filename)

    img = ImageGrab.grab(bbox=position)
    try:
        img.save(filename)
    except:
        raise Exception("Save screenshot failed!")


def close_window(window="TxBENCH - New project"):
    """关闭窗口

    Keyword Arguments:
        window {str} -- 窗口名称 (default: {"TxBENCH - New project"})
    """

    win32gui.PostMessage(win32gui.FindWindow(0, window), win32con.WM_CLOSE, 0, 0)



def run_CrystalDiskMark5(target = "T"):

    tool = "CrystalDiskMark 5.1.2 x64"
    tool_path = r'start "aa" "D:\SSD performance\CrystalDiskMark5\DiskMark64.exe"'
    os.system(tool_path)
    time.sleep(5)
    #找到tool 所在的窗口
    hwnd = win32gui.FindWindow(None, tool)
    #设置窗口为焦点
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383,140,0,0, win32con.SWP_NOSIZE)

    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"

    hwndChildList = get_child_windows(hwnd)
    x1, y1, x2 ,y2 = win32gui.GetWindowRect(hwndChildList[0])

    disk_select_xy = [x1 + 300, y1 + 25]
    start_xy = [x1 + 50, y1 + 35]

    mouse_click(disk_select_xy[0], disk_select_xy[1], cnt=2)
    keybd_single_char(target)
    time.sleep(0.5)
    #开始测试
    mouse_click(start_xy[0], start_xy[1])
    time.clock()

    #判断运行状态是否结束，当600s后超时退出
    while win32gui.GetWindowText(hwnd) != "Random Write 4KiB [5/5]":
        time.sleep(1)
        assert time.clock() < 600, "run err or time out!"

    #判断运行状态是否结束，当window name 不等于Random Write 4KiB [5/5]，并且为tool 名称时，则为结束
    while win32gui.GetWindowText(hwnd) == "Random Write 4KiB [5/5]":
        time.sleep(1)
        if win32gui.GetWindowText(hwnd) == tool:
            print("run {} finished!".format(tool))
            break

    filename = "{}.png".format(tool)
    #调整截图边缘
    x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd)
    x1 = x1 + 5
    x2 = x2 - 9
    y2 = y2 - 8

    screenshot(filename= filename, position=(x1, y1, x2, y2,))





def run_ATTO_Disk_Benchmark(target = "T"):

    tool = "Untitled - ATTO Disk Benchmark"
    tool_path = r'start "aa" "D:\SSD performance\ATTO Disk Benchmark\ATTODiskBenchmark.exe"'
    os.system(tool_path)
    time.sleep(5)
    #找到tool 所在的窗口
    hwnd = win32gui.FindWindow(None, tool)
    #设置窗口为焦点
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383,0,0,0, win32con.SWP_NOSIZE)

    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"

    hwndChildList = get_child_windows(hwnd)

    disk_select = button_center(hwndChildList[2])
    mouse_move(disk_select[0], disk_select[1])
    keybd_single_char(target)
    time.sleep(0.5)

    start_button = button_center(hwndChildList[27])
    mouse_click(start_button[0], start_button[1])


    start_time = time.time()
    while  win32gui.GetWindowText(hwndChildList[-10]) == "":
        time.sleep(1)
        elapsed_time = time.time() - start_time
        assert elapsed_time < 600 , "timeout!"
        #print(type(win32gui.GetWindowText(hwndChildList[-10])))
    #print(win32gui.GetWindowText(hwndChildList[-10]))
    #print(type(win32gui.GetWindowText(hwndChildList[-10])))
    filename = "{}.png".format(tool)
    #调整截图边缘
    x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd)
    x1 = x1 + 2
    x2 = x2 - 9
    y2 = y2 - 8
    time.sleep(1)
    screenshot(filename= filename, position=(x1, y1, x2, y2,))

    print("run {} finished!".format(tool))



time.sleep(4)
#get_all_child("TxBENCH - New project")

a = diskpart_1.DiskPart()
a.clean(1)
a.create_partition_primary(disk_number=1, filesystem="ntfs",partition_name = "E")
print(a.scan())

time.sleep(2)

run_assd("E")
time.sleep(2)
run_CrystalDiskMark5("E")
time.sleep(2)
run_ATTO_Disk_Benchmark("E")




#run_ATTO_Disk_Benchmark()

    # x1, y1, x2 ,y2 = win32gui.GetWindowRect(hwndChildList[0])

    # disk_select_xy = [x1 + 300, y1 + 25]
    # start_xy = [x1 + 50, y1 + 35]

    # mouse_click(disk_select_xy[0], disk_select_xy[1], cnt=2)
    # keybd_single_char(target)
    # time.sleep(0.5)
    # #开始测试
    # mouse_click(start_xy[0], start_xy[1])
    # time.clock()



    # while True:
    #     print(win32gui.GetWindowText(hwnd))
    #     time.sleep(1)
    #win32api.get

#run_CrystalDiskMark5()

#run_assd()
# tool = "AS SSD Benchmark 1.9.5986.35387"
# tool_path = r'start "aa" "D:\AS SSD Benchmark\AS SSD Benchmark.exe"'
# #os.system(tool_path)
# run_assd('T')
# hwnd = win32gui.FindWindow(None, tool)
# print(win32gui.GetWindowRect(hwnd))

# tool = "CrystalDiskMark 5.1.2 x64"
# hwnd = win32gui.FindWindow(None, tool)
# #x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd)
# x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd)
# x1 = x1 + 7
# x2 = x2 - 9
# y2 = y2 - 8
# filename = "{}.png".format(tool)
# position=(x1, y1, x2, y2,)
# #position=(100, 100, 200, 200,)
# screenshot(filename= filename, position=position)
# print(hwnd)
