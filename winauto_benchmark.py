#-*-coding:utf-8-*-

import win32gui
import win32api
import win32con
import os
import ctypes
import time
import subprocess
import threading
import diskpart_tool
import screenPrt
import json
import fire
import logging
from PIL import Image, ImageGrab

with open("setting.json",'r',encoding='utf-8') as json_file:
        #json.dump(tool_dic,json_file,ensure_ascii=False,indent=4)
        tool_dic = json.load(json_file)

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - [%(levelname)s] - %(message)s')


# tool_dic = {
#     "ASSD"  : ("AS SSD Benchmark 1.9.5986.35387", r"D:\SSD performance\AS SSD Benchmark\AS SSD Benchmark.exe"),
#     "CDM"   : ("CrystalDiskMark 6.0.1 x64", r"D:\SSD performance\CrystalDiskMark6_0_1\DiskMark64.exe"),
#     #"CDM"   : ("CrystalDiskMark 5.1.2 x64", r"D:\SSD performance\CrystalDiskMark5\DiskMark64.exe"),
#     "ATTO"  : ("Untitled - ATTO Disk Benchmark", r"D:\SSD performance\ATTO Disk Benchmark\ATTO Disk Benchmark.exe"),
#     "TXB"   : ("TxBENCH - New project", r"D:\SSD performance\TxBENCH.exe"),
#     "HDtune": ("HD Tune Pro 5.60 - 硬盘/固态硬盘实用程序 ", r"D:\SSD performance\HD Tune Pro.exe"),
#     "Anvil" : ("Anvil's Storage Utilities 1.1.0 (2014-January-1)", r"D:\SSD performance\Anvil`s Storage Utilities\AnvilPro.exe"),
#     "CDI"   : ("CrystalDiskInfo 7.6.0 ", r"C:\Program Files (x86)\CrystalDiskInfo\DiskInfo32.exe")
# }
    

def get_child_windows(parent):
    """    获得parent的所有子窗口句柄


    Arguments:
        parent {int} -- 父窗口句柄号

    Returns:
        [list] -- 返回子窗口句柄列表
    """
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
    score_result = {
        "Seq": (win32gui.GetWindowText(hwndChildList[18]), win32gui.GetWindowText(hwndChildList[22])),
        "4K" : (win32gui.GetWindowText(hwndChildList[19]), win32gui.GetWindowText(hwndChildList[17])),
        "4K-64Thrd" : (win32gui.GetWindowText(hwndChildList[23]), win32gui.GetWindowText(hwndChildList[21])),
        "Acc.time" : (win32gui.GetWindowText(hwndChildList[30]), win32gui.GetWindowText(hwndChildList[31])),
        "score_r_w" : (win32gui.GetWindowText(hwndChildList[5]), win32gui.GetWindowText(hwndChildList[7])),
        "Score" : win32gui.GetWindowText(hwndChildList[6])
    }
    L =[(win32gui.GetWindowText(hwndChildList[x])).split()[0] for x in [18, 22, 19 ,17, 23, 21, 30, 31, 5, 7, 6]]
    print(L)
    print(hwndChildList)
    print(win32gui.GetWindowRect(hwnd))
    a = ""
    for k in hwndChildList:
        b = "[{}]---[{}]---[{}]---[{}]---[{}]".format(hwndChildList.index(k),k,win32gui.GetWindowText(k),win32gui.GetClassName(k),win32gui.GetWindowRect(k))
        #print("{}:{}:{}".format(win32gui.GetWindowText(k),win32gui.GetClassName(k),win32gui.GetWindowRect(k)))
        a = a  + b + "\n"
    print(score_result)
    return a


def mouse_move(new_x, new_y):
    """移动鼠标

    Arguments:
        new_x {int} -- 横坐标
        new_y {int} -- 纵坐标
    """

    point = (new_x, new_y)
    win32api.SetCursorPos(point)

def mouse_click(x, y, idle=1):

    mouse_move(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(idle)

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
    return center_x, center_y



def click_handle(phwnd, cnt= 2, keybd_char= ""):
    x, y = button_center(phwnd)
    for i in range(0, cnt):
        mouse_click(x, y)
    if keybd_char:
        keybd_single_char(keybd_char)

def run_tool(tool="", tool_path="" , wait = 5):

    cmd = 'start "aa" "{}"'.format(tool_path)
    os.system(cmd)
    time.sleep(wait)

    for cnt in [ 1 ,1, 0,]:
        hwnd = win32gui.FindWindow(None, tool)
        if hwnd:
            time.sleep(5)
            break
        elif cnt:
            logging.warning("Open tool failed {} : {}".format(tool_path, hwnd))
            return False
            #raise Exception("Open tool failed!")
        else:
            time.sleep(10)
    logging.info("run {} : {}".format(tool_path, hwnd))
    return hwnd


def run_assd(target = "F", size = "1G"):


    tool, tool_path= tool_dic["ASSD"]
    hwnd = run_tool(tool , tool_path)
    if not hwnd:
        logging.warning("run {} failed".format(tool_path))
        return False
    #找到tool 所在的窗口
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383,140,0,0, win32con.SWP_NOSIZE)

    hwndChildList = get_child_windows(hwnd)

    #磁盘选择窗口/磁盘名称窗口/开始按键
    disk_select = hwndChildList[10]
    write_aactime = hwndChildList[31]
    size_select = hwndChildList[0]

    score_result = {
        "Seq": (win32gui.GetWindowText(hwndChildList[18]), win32gui.GetWindowText(hwndChildList[22])),
        "4K" : (win32gui.GetWindowText(hwndChildList[19]), win32gui.GetWindowText(hwndChildList[17])),
        "4K-64Thrd" : (win32gui.GetWindowText(hwndChildList[23]), win32gui.GetWindowText(hwndChildList[21])),
        "Acc.time" : (win32gui.GetWindowText(hwndChildList[30]), win32gui.GetWindowText(hwndChildList[31])),
        "score_r_w" : (win32gui.GetWindowText(hwndChildList[5]), win32gui.GetWindowText(hwndChildList[7])),
        "Score" : win32gui.GetWindowText(hwndChildList[6])

    }

    click_handle(disk_select, 2, target)#选择待测试磁盘
    click_handle(size_select, 2, "3")

    if size == "3G":
        pass
    elif size == "5G":
        keybd_single_char("5")
    elif size == "10G":
        keybd_single_char("1")
    elif size == "1G":
        keybd_single_char("1")
        keybd_single_char("1")
    else:
        pass

    # 找到 start按键
    hwnd1= win32gui.FindWindowEx(hwnd, None, None, "Start")
    # xy = button_center(hwnd1)
    # mouse_move(xy[0], xy[1])
    # #开始运行
    # mouse_click(xy[0], xy[1])
    click_handle(hwnd1, 1)

    score = hwndChildList[6]
    while win32gui.GetWindowText(score) == r"----" or win32gui.GetWindowText(write_aactime) == r"0.000 ms" or win32gui.GetWindowText(write_aactime) == r"-.-- ms":
        time.sleep(5)
  
    filename = tool
    filename = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename= filename)
    close_window(tool)
    return filename

def close_window(window="TxBENCH - New project"):
    """关闭窗口

    Keyword Arguments:
        window {str} -- 窗口名称 (default: {"TxBENCH - New project"})
    """
    win32gui.PostMessage(win32gui.FindWindow(0, window), win32con.WM_CLOSE, 0, 0)

def run_CrystalDiskMark5(target = "T", size="1G"):

    

    #tool = "CrystalDiskMark 5.1.2 x64"
    tool, tool_path= tool_dic["CDM"]
    hwnd = run_tool(tool , tool_path)
    if not hwnd:
        logging.warning("run {} failed".format(tool_path))
        return False    
    #设置窗口为焦点
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383,140,0,0, win32con.SWP_NOSIZE)

    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"

    hwndChildList = get_child_windows(hwnd)
    x1, y1, x2 ,y2 = win32gui.GetWindowRect(hwndChildList[0])

    disk_select_xy = [x1 + 300, y1 + 25]
    start_xy = [x1 + 50, y1 + 35]
    size_select_xy =[ x1 + 150, y1 + 25]


    #mouse_move(x1 + 300, y1 + 25)
    mouse_click(disk_select_xy[0], disk_select_xy[1], idle=2)
    mouse_click(disk_select_xy[0], disk_select_xy[1], idle=2)

    keybd_single_char(target, idle= 2)

    mouse_click(size_select_xy[0], size_select_xy[1], idle=2)
    mouse_click(size_select_xy[0], size_select_xy[1], idle=2)

    keybd_single_char("3", idle= 1)

    if size == "1G":
        keybd_single_char("1", idle= 1)
        keybd_single_char("1", idle= 1)
    elif size == "2G":
        keybd_single_char("2", idle= 1)
    elif size == "4G":
        keybd_single_char("4", idle= 1)
    elif size == "8G":
        keybd_single_char("8", idle= 1)
    elif size == "16G":
        keybd_single_char("1", idle= 1)
        keybd_single_char("1", idle= 1)
        keybd_single_char("1", idle= 1)
    elif size == "32G":
        keybd_single_char("3", idle= 1)
    else:
        pass    
    #开始测试
    mouse_click(start_xy[0], start_xy[1])
    if "CrystalDiskMark 5." in tool:

        run_check = [#"Sequential Read Multi [5/5]", 
                    "Sequential Write Multi [5/5]",
                    #"Random Read 4KiB Multi [5/5]",
                    "Random Write 4KiB Multi [5/5]",
                    #"Sequential Read [5/5]",
                    "Sequential Write [5/5]",
                    "Random Write 4KiB [5/5]"
                    ]
    elif "CrystalDiskMark 6." in tool:

        run_check = [#"Sequential Read Multi [5/5]", 
                    # "Sequential Write Multi [5/5]",
                    # #"Random Read 4KiB Multi [5/5]",
                    # "Random Write 4KiB Multi [5/5]",
                    #"Sequential Read [5/5]",
                    "Sequential Write [5/5]",
                    "Interval Time 1/5 sec",
                    "Random Write 4KiB [5/5]",
                    "Interval Time 1/5 sec",
                    "Random Write 4KiB [5/5]",
                    "Interval Time 1/5 sec",
                    "Random Write 4KiB [5/5]"
                    ]
    for status in run_check:
        while True:
            if win32gui.GetWindowText(hwnd) != status:
                time.sleep(0.1)
            else:
                time.sleep(1)
                break

    while win32gui.GetWindowText(hwnd) != tool:
        time.sleep(1)

    filename = tool
    filename = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename= filename)
    close_window(tool)
    return filename

def run_Anvil(target = "T"):

    tool = "Anvil's Storage Utilities 1.1.0 (2014-January-1)"
    tool, tool_path= tool_dic["Anvil"]
    hwnd = run_tool(tool , tool_path)
    if not hwnd:
        logging.warning("run {} failed".format(tool_path))
        return False    #设置窗口为焦点
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383,140,0,0, win32con.SWP_NOSIZE)
    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"
    hwndChildList = get_child_windows(hwnd)
    hwnd_QD_Write = win32gui.FindWindow(None, "IO - Threaded QD (Random Write)")
    
    disk_select = button_center(hwndChildList[8])
    disk_run = button_center(hwndChildList[14])
    disk_tmp = button_center(hwndChildList[10])
    mouse_click(disk_select[0], disk_select[1])
    mouse_click(disk_select[0], disk_select[1])
    keybd_single_char(target)

    mouse_click(disk_run[0], disk_run[1])
    # #print(disk_select)
    # mouse_move(disk_select[0], disk_select[1])
    
    for i in range(0, 3):
        while not win32gui.IsWindowVisible(hwnd_QD_Write):
            time.sleep(0.1)
        while win32gui.IsWindowVisible(hwnd_QD_Write):
            time.sleep(0.1)
    else:
        time.sleep(3)
   # win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383,140,0,0, win32con.SWP_NOSIZE)
    #time.sleep(3)

 
    #开始测试
    mouse_click(disk_tmp[0], disk_tmp[1], 2)
    mouse_click(disk_tmp[0], disk_tmp[1], 2)
    filename = tool
    #screenPrt.ScreenPrintWin().save_bitmap(bmp_filename= filename)
    filename = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename= filename)
    #time.sleep(10)
    close_window(tool)
    return filename




def run_ATTO_Disk_Benchmark(target = "T", mode = 2, dpeth = 4):

    tool = "Untitled - ATTO Disk Benchmark"
    tool_path = r'start "aa" "D:\SSD performance\ATTO Disk Benchmark\ATTO Disk Benchmark.exe"'
    
    tool, tool_path= tool_dic["ATTO"]
    hwnd = run_tool(tool , tool_path)
    if not hwnd:
        logging.warning("run {} failed".format(tool_path))
        return False    #设置窗口为焦点
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383,0,0,0, win32con.SWP_NOSIZE)

    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"

    mode_hwnd_tag = mode + 10
    hwndChildList = get_child_windows(hwnd)

    disk_select = button_center(hwndChildList[2])
    mouse_click(disk_select[0], disk_select[1])
    mouse_click(disk_select[0], disk_select[1])
    keybd_single_char(target)

    mode_select = button_center(hwndChildList[mode_hwnd_tag])
    mouse_click(mode_select[0], mode_select[1])

    pattern_button =  hwndChildList[15]
    dpeth_button = hwndChildList[18]

    if mode == 1:
        print(1)
        click_handle(pattern_button, 2 ,"R")
    elif mode == 2 :
        click_handle(dpeth_button, 2, chr(dpeth))
    elif mode == 3 :
        print("else")
    else:
        print("else")

    start_button = hwndChildList[27]
    click_handle(start_button, 1, None)

    #start_time = time.time()
    while  win32gui.GetWindowText(hwndChildList[-10]) == "":
        time.sleep(1)
        # elapsed_time = time.time() - start_time
        # assert elapsed_time < 6000 , "timeout!"

    filename = tool + str(mode)
    filename = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename= filename)
    #print("run {} finished!".format(tool))
    cmd = r'taskkill /F /IM "ATTO Disk Benchmark.exe"'
    os.system(cmd)
    return filename

def run_TxBENCH(target = "T"):
    target = target.upper()
    tool, tool_path= tool_dic["TXB"]
    hwnd = run_tool(tool , tool_path)
    if not hwnd:
        logging.warning("run {} failed".format(tool_path))
        return False
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383,140,0,0, win32con.SWP_NOSIZE)
    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"
    hwndChildList = get_child_windows(hwnd)
    start_button = button_center(hwndChildList[13])

    cnt  = win32api.GetLogicalDriveStrings().split(":\\\x00").index(target)
    disk_select = button_center(hwndChildList[10])

    mouse_click(disk_select[0], disk_select[1])
    mouse_click(disk_select[0], disk_select[1])
    

    for k in range(0, cnt):
        keybd_single_char("(")
        time.sleep(1)
    
    start_init = win32gui.GetWindowText(hwndChildList[13])
    mouse_click(start_button[0], start_button[1])
    time.sleep(4)

    start_time = time.time()
    while  win32gui.GetWindowText(hwndChildList[13]) != start_init:
        time.sleep(1)
        elapsed_time = time.time() - start_time
        assert elapsed_time < 6000 , "timeout!"

    filename = tool
    filename = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename= filename)

    print("run {} finished!".format(tool))
    close_window(tool)
    return filename



def get_DiskInfo(target = 0, image = ""):

    tool, tool_path= tool_dic["CDI"]
    hwnd = run_tool(tool , tool_path)
    if not hwnd:
        logging.warning("run {} failed".format(tool_path))
        return False
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,2000,800, win32con.SWP_SHOWWINDOW)#设置窗口为焦点
    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"
    hwndChildList = get_child_windows(hwnd)

    target_button = button_center(hwndChildList[2 + target]) #获取所需磁盘的按键
    mouse_click(target_button[0], target_button[1])

    #filename = "{}-{}".format(image, tool)

    filename = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename=tool)
    #print("run {} finished!".format(tool))
    close_window(tool)
    time.sleep(1)
    return filename

def run_HDtune(disk_number=100):


    tool, tool_path= tool_dic["HDtune"]
    hwnd = run_tool(tool , tool_path)
    if not hwnd:
        logging.warning("run {} failed".format(tool_path))
        return False

    #设置窗口为焦点
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383,0,0,0, win32con.SWP_NOSIZE)
    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"
    hwndChildList = get_child_windows(hwnd)


    disk_select = button_center(hwndChildList[0])
    mouse_click(disk_select[0], disk_select[1], 2)
    mouse_click(disk_select[0], disk_select[1] + 14 *(disk_number + 1))

    start_button = button_center(hwndChildList[13])
    read_button = button_center(hwndChildList[14])
    write_button = button_center(hwndChildList[15])
    
    start_init = win32gui.GetWindowText(hwndChildList[13])
    #print(start_init)

    mouse_click(read_button[0], read_button[1])
    mouse_click(start_button[0], start_button[1])

    start_time = time.time()
    while win32gui.GetWindowText(hwndChildList[13]) != start_init:
        time.sleep(1)
        # elapsed_time = time.time() - start_time
        # assert elapsed_time < 600 , "timeout!"
    time.sleep(1)
    filename = "HDtune_read_pre"
    output_r = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename=filename)

    mouse_click(write_button[0],write_button[1])
    mouse_click(start_button[0],start_button[1])

    
    hwnd_write_yes_window = win32gui.FindWindow(None, "警告!")
    hwnd_ChildList = get_child_windows(hwnd_write_yes_window)
    run_write_button = button_center(hwnd_ChildList[3])
    confirm_button =  button_center(hwnd_ChildList[0])
    mouse_click(run_write_button[0], run_write_button[1],2)

    
    mouse_click(confirm_button[0], confirm_button[1], 5)

    start_time = time.time()
    while  win32gui.GetWindowText(hwndChildList[13]) != start_init:
        time.sleep(1)
        #elapsed_time = time.time() - start_time
        #assert elapsed_time < 600 , "timeout!"
    time.sleep(2)
    filename = "HDtune_write"
    output_w = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename= filename)


    time.sleep(4)
    mouse_click(read_button[0], read_button[1])
    mouse_click(start_button[0],start_button[1])

 
    start_time = time.time()
    while  win32gui.GetWindowText(hwndChildList[13]) != start_init:
        time.sleep(1)
        #elapsed_time = time.time() - start_time
        #assert elapsed_time < 600 , "timeout!"
    time.sleep(1)
    filename = "HDtune_read"
    output_r = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename= filename)
    close_window(tool)
    return output_w, output_r

def run_PCmark7(target = 0, image = ""):

    # tool, tool_path= tool_dic["CDI"]
    # hwnd = run_tool(tool , tool_path)
    tool = "PCMark 7 Professional Edition v1.4.0"
    tool_path = r"C:\Program Files\Futuremark\PCMark 7\bin\PCMark7.exe"
    hwnd = run_tool(tool , tool_path)
    if not hwnd:
        logging.warning("run {} failed".format(tool_path))
        return False
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 10,10,1038,746, win32con.SWP_SHOWWINDOW)#设置窗口为焦点
    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"
    window_base = win32gui.GetWindowRect(hwnd)
    disk_select = (window_base[0] + 171, window_base[1] + 478)
    run_button = (window_base[0] + 825, window_base[1] + 215)
    cnt = win32api.GetLogicalDriveStrings().split(":\\\x00").index(target)
    mouse_click(disk_select[0], disk_select[1])
    time.sleep(1)
    mouse_click(disk_select[0] , disk_select[1]+ (cnt+1)*21)
    mouse_click(run_button[0], run_button[1])
    
    #stop_flag = (window_base[0] + 600, window_base[1] + 220)
    time.sleep(10)
    stop_flag = (window_base[0] + 365, window_base[1] + 111)
    mouse_move(window_base[0] + 365, window_base[1] + 111)
    mouse_move(window_base[0], window_base[1])
    init_rgb = ImageGrab.grab(bbox=win32gui.GetWindowRect(hwnd)).getpixel((stop_flag))
    while ImageGrab.grab(bbox=win32gui.GetWindowRect(hwnd)).getpixel((stop_flag)) == init_rgb :
        print(ImageGrab.grab(bbox=win32gui.GetWindowRect(hwnd)).getpixel((stop_flag)))
        time.sleep(1)

    filename = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename= tool)
    close_window(tool)
    return filename
    #(171 478)
    # 825 215

    #625 222
    #target_button = button_center(hwndChildList[2 + target]) #获取所需磁盘的按键
    #mouse_click(target_button[0] + (cnt+1)*21, target_button[1])

    # #filename = "{}-{}".format(image, tool)

    # filename = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename=tool)
    # #print("run {} finished!".format(tool))
    # close_window(tool)
    # time.sleep(1)
    # return filenamer


def run_PCmark8(target = 0, image = ""):

    # tool, tool_path= tool_dic["CDI"]
    # hwnd = run_tool(tool , tool_path)
    tool = "PCMark 8 Professional Edition "
    tool_path = r"C:\Program Files\Futuremark\PCMark 8\bin\PCMark8.exe"
    hwnd = run_tool(tool , tool_path)
    if not hwnd:
        logging.warning("run {} failed".format(tool_path))
        return False
    hwnd_xy = win32gui.GetWindowRect(hwnd)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, hwnd_xy[0],hwnd_xy[1],hwnd_xy[2]-hwnd_xy[0] ,hwnd_xy[3]-hwnd_xy[1], win32con.SWP_SHOWWINDOW)#设置窗口为焦点
    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"
    window_base = win32gui.GetWindowRect(hwnd)

    mouse_click(window_base[0] + 999, window_base[1] + 66)
    mouse_click(window_base[0] + 900, window_base[1] + 200)
    
    disk_select = (window_base[0] + 900, window_base[1] + 450)
    run_button = (window_base[0] + 1100, window_base[1] + 660)
    
    cnt = win32api.GetLogicalDriveStrings().split(":\\\x00").index(target)
    mouse_click(disk_select[0], disk_select[1])
    time.sleep(1)

    mouse_click(disk_select[0] , disk_select[1]+ (cnt+1)*21)
    mouse_click(run_button[0], run_button[1])
    
    #stop_flag = (window_base[0] + 600, window_base[1] + 220)
    while win32gui.GetWindowRect(hwnd)[0] >= 0:
        time.sleep(1)

    while win32gui.GetWindowRect(hwnd)[0] < 0:
        time.sleep(1)

    filename = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename= tool)
    close_window(tool)
    cmd = r'taskkill /F /IM "PCmark8.exe"'
    os.system(cmd)
    return filename
    
if __name__ == "__main__" :
    #print(get_all_child("AS SSD Benchmark 2.0.6694.23026"))
    print(win32api.GetLogicalDriveStrings())
    # run_assd("H")
    # fire.Fire({
    #       'assd': run_assd,
    #       'cdm' : run_CrystalDiskMark5,
    #       'atto': run_ATTO_Disk_Benchmark,
    #       'txb' : run_TxBENCH,
    #       'avl' : run_Anvil,
    #       'HDtune': run_HDtune
    # }
    # )
