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
import unittest


tool_dic = {
    "ASSD"  : ("AS SSD Benchmark 1.9.5986.35387", r"D:\SSD performance\AS SSD Benchmark\AS SSD Benchmark.exe"),
    "CDM"   : ("CrystalDiskMark 6.0.1 x64", r"D:\SSD performance\CrystalDiskMark6_0_1DiskMark64.exe"),
    #"CDM"   : ("CrystalDiskMark 5.1.2 x64", r"D:\SSD performance\CrystalDiskMark5\DiskMark64.exe"),
    "ATTO"  : ("Untitled - ATTO Disk Benchmark", r"D:\SSD performance\ATTO Disk Benchmark\ATTO Disk Benchmark.exe"),
    "TXB"   : ("TxBENCH - New project", r"D:\SSD performance\TxBENCH.exe"),
    "HDtune": ("HD Tune Pro 5.60 - 硬盘/固态硬盘实用程序 ", r"D:\SSD performance\HD Tune Pro.exe"),
    "Anvil" : ("Anvil's Storage Utilities 1.1.0 (2014-January-1)", r"D:\SSD performance\Anvil`s Storage Utilities\AnvilPro.exe"),
    "CDI"   : ("CrystalDiskInfo 7.6.0 ", r"C:\Program Files (x86)\CrystalDiskInfo\DiskInfo32.exe")
}
    

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
    print(hwndChildList)
    a = ""
    for k in hwndChildList:
        b = "{}---{}---{}---{}---{}".format(hwndChildList.index(k),k,win32gui.GetWindowText(k),win32gui.GetClassName(k),win32gui.GetWindowRect(k))
        #print("{}:{}:{}".format(win32gui.GetWindowText(k),win32gui.GetClassName(k),win32gui.GetWindowRect(k)))
        a = a  + b + "\n"
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



def run_tool(tool="", wait = 5):

    cmd = 'start "aa" "{}"'.format(tool)
    os.system(cmd)
    time.sleep(wait)

def run_assd(target = "F"):


    tool, tool_path= tool_dic["ASSD"]
    run_tool(tool_path)
    #找到tool 所在的窗口
    hwnd = win32gui.FindWindow(None, tool)
    #设置assd窗口为焦点
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383,140,0,0, win32con.SWP_NOSIZE)

    hwndChildList = get_child_windows(hwnd)

    #磁盘选择窗口/磁盘名称窗口/开始按键
    disk_select = hwndChildList[10]
    write_aactime = hwndChildList[31]
    #选择待测试磁盘
    xy = button_center(disk_select)
    mouse_click(xy[0], xy[1])

    keybd_single_char("C")

    keybd_single_char(target)
    mouse_click(xy[0], xy[1])

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
                    break
                else:
                    flag = flag + 1
                    time.sleep(1)
        if flag == 10:
            break

    filename = "{}.bmp".format(tool)
    screenPrt.ScreenPrintWin().save_bitmap(bmp_filename= filename)
    close_window(tool)

def close_window(window="TxBENCH - New project"):
    """关闭窗口

    Keyword Arguments:
        window {str} -- 窗口名称 (default: {"TxBENCH - New project"})
    """
    win32gui.PostMessage(win32gui.FindWindow(0, window), win32con.WM_CLOSE, 0, 0)

def run_CrystalDiskMark5(target = "T"):

    tool = "CrystalDiskMark 5.1.2 x64"
    tool, tool_path= tool_dic["CDM"]
    run_tool(tool_path)
    
    #找到tool 所在的窗口
    hwnd = win32gui.FindWindow(None, tool)
    #设置窗口为焦点
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383,140,0,0, win32con.SWP_NOSIZE)

    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"

    hwndChildList = get_child_windows(hwnd)
    x1, y1, x2 ,y2 = win32gui.GetWindowRect(hwndChildList[0])

    disk_select_xy = [x1 + 300, y1 + 25]
    start_xy = [x1 + 50, y1 + 35]

    mouse_click(disk_select_xy[0], disk_select_xy[1])
    mouse_click(disk_select_xy[0], disk_select_xy[1])
    keybd_single_char(target)

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
        print(status)

    while win32gui.GetWindowText(hwnd) != tool:
        time.sleep(1)

    filename = "{}.bmp".format(tool)
    screenPrt.ScreenPrintWin().save_bitmap(bmp_filename= filename)
    close_window(tool)


def run_Anvil(target = "T"):

    tool = "Anvil's Storage Utilities 1.1.0 (2014-January-1)"
    tool, tool_path= tool_dic["Anvil"]
    run_tool(tool_path,7)
    
    #找到tool 所在的窗口
    hwnd = win32gui.FindWindow(None, tool)
    #设置窗口为焦点
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
    mouse_click(disk_tmp[0], disk_tmp[1],2)
    mouse_click(disk_tmp[0], disk_tmp[1],2)
    filename = "{}.bmp".format(tool)
    screenPrt.ScreenPrintWin().save_bitmap(bmp_filename= filename)
    screenPrt.ScreenPrintWin().save_bitmap(bmp_filename= filename)
    #time.sleep(10)
    #close_window(tool)





def run_ATTO_Disk_Benchmark(target = "T"):

    tool = "Untitled - ATTO Disk Benchmark"
    tool_path = r'start "aa" "D:\SSD performance\ATTO Disk Benchmark\ATTO Disk Benchmark.exe"'
    
    tool, tool_path= tool_dic["ATTO"]
    run_tool(tool_path)
    #找到tool 所在的窗口
    hwnd = win32gui.FindWindow(None, tool)
    #设置窗口为焦点
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383,0,0,0, win32con.SWP_NOSIZE)

    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"

    hwndChildList = get_child_windows(hwnd)

    disk_select = button_center(hwndChildList[2])
    mouse_move(disk_select[0], disk_select[1])
    keybd_single_char(target)

    start_button = button_center(hwndChildList[27])
    mouse_click(start_button[0], start_button[1])

    start_time = time.time()
    while  win32gui.GetWindowText(hwndChildList[-10]) == "":
        time.sleep(1)
        elapsed_time = time.time() - start_time
        assert elapsed_time < 6000 , "timeout!"

    filename = "{}.bmp".format(tool)
    screenPrt.ScreenPrintWin().save_bitmap(bmp_filename= filename)
    print("run {} finished!".format(tool))
    cmd = r'taskkill /F /IM "ATTO Disk Benchmark.exe"'
    os.system(cmd)




def run_TxBENCH(target = "T"):

    tool = "TxBENCH - New project"
    tool_path = r'start "aa" "D:\SSD performance\TxBENCH.exe'

    tool, tool_path= tool_dic["TXB"]
    run_tool(tool_path)
    #找到tool 所在的窗口

    hwnd = win32gui.FindWindow(None, tool)
    #设置窗口为焦点
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383,140,0,0, win32con.SWP_NOSIZE)
    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"
    hwndChildList = get_child_windows(hwnd)

    start_button = button_center(hwndChildList[13])
    start_init = win32gui.GetWindowText(hwndChildList[13])
    mouse_click(start_button[0], start_button[1])
    time.sleep(4)

    start_time = time.time()
    while  win32gui.GetWindowText(hwndChildList[13]) != start_init:
        time.sleep(1)
        elapsed_time = time.time() - start_time
        assert elapsed_time < 6000 , "timeout!"

    filename = "{}.bmp".format(tool)
    screenPrt.ScreenPrintWin().save_bitmap(bmp_filename= filename)

    print("run {} finished!".format(tool))
    close_window(tool)



def get_DiskInfo(target = 0, image = ""):

    tool, tool_path= tool_dic["CDI"]
    run_tool(tool_path)

    hwnd = win32gui.FindWindow(None, tool)#找到tool 的句柄
    print(hwnd)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,2000,2000, win32con.SWP_SHOWWINDOW)#设置窗口为焦点
    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"
    hwndChildList = get_child_windows(hwnd)

    target_button = button_center(hwndChildList[2 + target]) #获取所需磁盘的按键
    mouse_click(target_button[0], target_button[1])

    filename = "{}-{}.bmp".format(image,tool)
    screenPrt.ScreenPrintWin().save_bitmap(bmp_filename= filename)

    print("run {} finished!".format(tool))
    #close_window(tool)
    return filename

def run_HDtune(disk_number=100):

    a= diskpart_tool.DiskPart()
    a.clean(disk_number)

    tool = "HD Tune Pro 5.60 - 硬盘/固态硬盘实用程序 "
    tool_path = r'start "aa" "D:\SSD performance\HD Tune Pro.exe'

    tool, tool_path= tool_dic["HDtune"]
    run_tool(tool_path)
    
    hwnd = win32gui.FindWindow(None, tool)

    #设置窗口为焦点
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383,0,0,0, win32con.SWP_NOSIZE)
    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"
    hwndChildList = get_child_windows(hwnd)


    disk_select = button_center(hwndChildList[0])
    mouse_click(disk_select[0], disk_select[1])
    mouse_click(disk_select[0], disk_select[1] + 14 *(disk_number + 1))

    start_button = button_center(hwndChildList[13])
    read_button = button_center(hwndChildList[14])
    write_button = button_center(hwndChildList[15])
    
    start_init = win32gui.GetWindowText(hwndChildList[13])
    print(start_init)
    
    mouse_click(write_button[0],write_button[1])
    time.sleep(0.5)
    mouse_click(start_button[0],start_button[1])
    time.sleep(0.5)
    
    hwnd_write_yes_window = win32gui.FindWindow(None, "警告!")
    hwnd_ChildList = get_child_windows(hwnd_write_yes_window)
    run_write_button = button_center(hwnd_ChildList[3])
    confirm_button =  button_center(hwnd_ChildList[0])
    mouse_click(run_write_button[0], run_write_button[1])
    time.sleep(2)
    
    mouse_click(confirm_button[0], confirm_button[1])

    time.sleep(5)
    start_time = time.time()
    while  win32gui.GetWindowText(hwndChildList[13]) != start_init:
        time.sleep(1)
        elapsed_time = time.time() - start_time
        assert elapsed_time < 600 , "timeout!"
    time.sleep(2)
    filename = "HDtune_write.bmp"
    screenPrt.ScreenPrintWin().save_bitmap(bmp_filename= filename)


    time.sleep(4)
    mouse_click(read_button[0], read_button[1])
    time.sleep(0.5)
    mouse_click(start_button[0],start_button[1])
    time.sleep(5)
 
    start_time = time.time()
    while  win32gui.GetWindowText(hwndChildList[13]) != start_init:
        time.sleep(1)
        elapsed_time = time.time() - start_time
        assert elapsed_time < 600 , "timeout!"
    time.sleep(1)
    filename = "HDtune_read.bmp"
    screenPrt.ScreenPrintWin().save_bitmap(bmp_filename= filename)
    close_window(tool)
    return filename

def run_performance(disk_number=100, partition_name = "A"):
    # a = diskpart_tool.DiskPart()
    # a.clean(disk_number)
    # a.create_partition_primary(disk_number=disk_number, filesystem="ntfs",partition_name =partition_name)
    #print(a.scan())
    time.sleep(2)
    run_assd(partition_name)
    time.sleep(2)
    run_CrystalDiskMark5(partition_name)
    time.sleep(2)
    run_ATTO_Disk_Benchmark(partition_name)
    time.sleep(2)
    run_TxBENCH(partition_name)
    time.sleep(2)
    #run_HDtune(disk_number=disk_number)










if __name__ == "__main__" :

    get_DiskInfo(2, "ss")
 

    