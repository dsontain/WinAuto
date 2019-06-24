# -*-coding:utf-8-*-
import win32gui
import win32api
import win32con
import os
import time
import diskpart_new
import screenPrt
import json
import logging
import re
from PIL import ImageGrab

with open("setting.json", 'r', encoding='utf-8') as json_file:
    tool_dic = json.load(json_file)
    # json.dump(tool_dic,json_file,ensure_ascii=False,indent=4)

# tool_dic = {
#     "ASSD"  : ("AS SSD Benchmark 1.9.5986.35387", r"D:\SSD performance\AS SSD Benchmark\AS SSD Benchmark.exe"),
#     "CDM"   : ("CrystalDiskMark 6.0.1 x64", r"D:\SSD performance\CrystalDiskMark6_0_1\DiskMark64.exe"),
#     #"CDM"   : ("CrystalDiskMark 5.1.2 x64", r"D:\SSD performance\CrystalDiskMark5\DiskMark64.exe"),
#     "ATTO"  : ("Untitled - ATTO Disk Benchmark", r"D:\SSD performance\ATTO Disk Benchmark\ATTO Disk Benchmark.exe"),
#     "TXB"   : ("TxBENCH - New project", r"D:\SSD performance\TxBENCH.exe"),
#     "HDtune": ("HD Tune Pro 5.60 - 硬盘/固态硬盘实用程序 ", r"D:\SSD performance\HD Tune Pro.exe"),
# "Anvil" : ("Anvil's Storage Utilities 1.1.0 (2014-January-1)",
# r"D:\SSD performance\Anvil`s Storage Utilities\AnvilPro.exe"),
#     "CDI"   : ("CrystalDiskInfo 7.6.0 ", r"C:\Program Files (x86)\CrystalDiskInfo\DiskInfo32.exe")
# }
    

def get_child_windows(parent):

    hwnd_child_list = []
    win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd), hwnd_child_list)
    return hwnd_child_list


def get_all_child(tool="Untitled - ATTO Disk Benchmark"):

    hwnd = win32gui.FindWindow(None, tool)
    hwnd_child_list = get_child_windows(hwnd)
    # score_result = {
    #     "Seq": (win32gui.GetWindowText(hwnd_child_list[18]), win32gui.GetWindowText(hwnd_child_list[22])),
    #     "4K": (win32gui.GetWindowText(hwnd_child_list[19]), win32gui.GetWindowText(hwnd_child_list[17])),
    #     "4K-64Thrd": (win32gui.GetWindowText(hwnd_child_list[23]), win32gui.GetWindowText(hwnd_child_list[21])),
    #     "Acc.time": (win32gui.GetWindowText(hwnd_child_list[30]), win32gui.GetWindowText(hwnd_child_list[31])),
    #     "score_r_w": (win32gui.GetWindowText(hwnd_child_list[5]), win32gui.GetWindowText(hwnd_child_list[7])),
    #     "Score": win32gui.GetWindowText(hwnd_child_list[6])
    # }
    # L = [(win32gui.GetWindowText(hwnd_child_list[x])).split()[0] for x in [18, 22, 19 ,17, 23, 21, 30, 31, 5, 7, 6]]
    # print(L)
    # print(hwnd_child_list)
    # print(win32gui.GetWindowRect(hwnd))
    a = ""
    for k in hwnd_child_list:
        b = "[{}]---[{}]---[{}]---[{}]---[{}]".format(hwnd_child_list.index(k), k,
                                                      win32gui.GetWindowText(k),
                                                      win32gui.GetClassName(k), win32gui.GetWindowRect(k))
        # print("{}:{}:{}".format(win32gui.GetWindowText(k),win32gui.GetClassName(k),win32gui.GetWindowRect(k)))
        if k == 134284:
            print(hwnd_child_list.index(k))
        a = a + b + "\n"
    # print(score_result)
    return a


def mouse_move(new_x, new_y):

    point = (new_x, new_y)
    win32api.SetCursorPos(point)


def mouse_click(x, y, idle=1, cnt=1):
    mouse_move(x, y)
    for i in range(cnt):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(idle)


def keybd_input(input_str, idle=1):

    for key in input_str:
        key = ord(key)
        win32api.keybd_event(key, 0, 0, 0)
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(idle)


def keybd_input_combination(*kb_keys):
    """
    Input keyboard combination keys, such as input 16(shift) + 97(1) to get '!'
    :param kb_keys: keyboard keys, (int)
    :return: None
    """

    time.sleep(2)
    for key in kb_keys:
        win32api.keybd_event(key, 0, 0, 0)
        time.sleep(0.2)
    for key in reversed(kb_keys):
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)


def click_edit_and_input(hwnd, message=""):
    if win32gui.GetClassName(hwnd) == "Edit":
        click_handle(hwnd, cnt=2)
        keybd_input(message)
    else:
        raise Exception(f"{hwnd} is not class Edit")


def button_center(phwnd):

    center_xy = win32gui.GetWindowRect(phwnd)
    center_x = (center_xy[0] + center_xy[2]) // 2
    center_y = (center_xy[1] + center_xy[3]) // 2
    return center_x, center_y


def click_handle(phwnd=0, cnt=1, keybd_char=""):
    x, y = button_center(phwnd)
    mouse_click(x, y, cnt=cnt)

    if keybd_char:
        keybd_input(keybd_char, idle=0)


def run_tool(tool="", tool_path="", wait=5):

    cmd = 'start "aa" "{}"'.format(tool_path)
    os.system(cmd)
    time.sleep(wait)

    for cnt in [1, 1, 0]:
        hwnd = win32gui.FindWindow(None, tool)
        if hwnd:
            time.sleep(5)
            break
        elif cnt:
            logging.warning("Open tool failed {} : {}".format(tool_path, hwnd))
            raise Exception("Open tool failed!")
        else:
            time.sleep(10)
    logging.info("run {} : {}".format(tool_path, hwnd))
    return hwnd


def run_assd(target="F", size="1G"):

    tool, tool_path = tool_dic["ASSD"]
    hwnd = run_tool(tool, tool_path)
    if not hwnd:
        logging.warning("run {} failed".format(tool_path))
        return False
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383, 140, 0, 0, win32con.SWP_NOSIZE)

    hwnd_child_list = get_child_windows(hwnd)

    disk_select = hwnd_child_list[10]
    write_aactime = hwnd_child_list[31]
    size_select = hwnd_child_list[0]

    # score_result = {
    #     "Seq": (win32gui.GetWindowText(hwnd_child_list[18]), win32gui.GetWindowText(hwnd_child_list[22])),
    #     "4K": (win32gui.GetWindowText(hwnd_child_list[19]), win32gui.GetWindowText(hwnd_child_list[17])),
    #     "4K-64Thrd": (win32gui.GetWindowText(hwnd_child_list[23]), win32gui.GetWindowText(hwnd_child_list[21])),
    #     "Acc.time": (win32gui.GetWindowText(hwnd_child_list[30]), win32gui.GetWindowText(hwnd_child_list[31])),
    #     "score_r_w": (win32gui.GetWindowText(hwnd_child_list[5]), win32gui.GetWindowText(hwnd_child_list[7])),
    #     "Score": win32gui.GetWindowText(hwnd_child_list[6])
    #
    # }

    click_handle(disk_select, 2, target)
    click_handle(size_select, 2, "3")

    if size == "3G":
        pass
    elif size == "5G":
        keybd_input("5")
    elif size == "10G":
        keybd_input("1")
    elif size == "1G":
        keybd_input("1")
        keybd_input("1")
    else:
        pass

    # 找到 start按键
    hwnd1 = win32gui.FindWindowEx(hwnd, None, None, "Start")
    # xy = button_center(hwnd1)
    # mouse_move(xy[0], xy[1])
    # #开始运行
    # mouse_click(xy[0], xy[1])
    click_handle(hwnd1, 1)

    score = hwnd_child_list[6]
    while win32gui.GetWindowText(score) == r"----" or \
            win32gui.GetWindowText(write_aactime) == r"0.000 ms" or \
            win32gui.GetWindowText(write_aactime) == r"-.-- ms":
        time.sleep(5)
  
    filename = tool
    filename = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename=filename)
    close_window(tool)
    return filename


def close_window(window="TxBENCH - New project"):
    """关闭窗口

    Keyword Arguments:
        window {str} -- 窗口名称 (default: {"TxBENCH - New project"})
    """
    win32gui.PostMessage(win32gui.FindWindow(0, window), win32con.WM_CLOSE, 0, 0)


def run_crystal__diskmark(target="T", size="1G"):

    tool, tool_path = tool_dic["CDM"]
    hwnd = run_tool(tool, tool_path)
    if not hwnd:
        logging.warning("run {} failed".format(tool_path))
        return False    

    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383, 140, 0, 0, win32con.SWP_NOSIZE)

    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"

    hwnd_child_list = get_child_windows(hwnd)
    x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd_child_list[0])

    disk_select_xy = [x1 + 300, y1 + 25]
    start_xy = [x1 + 50, y1 + 35]
    size_select_xy = [x1 + 150, y1 + 25]

    # mouse_move(x1 + 300, y1 + 25)
    mouse_click(disk_select_xy[0], disk_select_xy[1], idle=2)
    mouse_click(disk_select_xy[0], disk_select_xy[1], idle=2)

    keybd_input(target, idle=2)

    mouse_click(size_select_xy[0], size_select_xy[1], idle=2)
    mouse_click(size_select_xy[0], size_select_xy[1], idle=2)

    keybd_input("3", idle=1)

    if size == "1G":
        keybd_input("1", idle=1)
        keybd_input("1", idle=1)
    elif size == "2G":
        keybd_input("2", idle=1)
    elif size == "4G":
        keybd_input("4", idle=1)
    elif size == "8G":
        keybd_input("8", idle=1)
    elif size == "16G":
        keybd_input("1", idle=1)
        keybd_input("1", idle=1)
        keybd_input("1", idle=1)
    elif size == "32G":
        keybd_input("3", idle=1)
    else:
        pass    

    mouse_click(start_xy[0], start_xy[1])
    if "CrystalDiskMark 5." in tool:
        run_check = (
                    "Sequential Write Multi [5/5]",
                    "Random Write 4KiB Multi [5/5]",
                    "Sequential Write [5/5]",
                    "Random Write 4KiB [5/5]"
        )
    elif "CrystalDiskMark 6." in tool:
        run_check = (
                    "Sequential Write [5/5]",
                    "Interval Time 1/5 sec",
                    "Random Write 4KiB [5/5]",
                    "Interval Time 1/5 sec",
                    "Random Write 4KiB [5/5]",
                    "Interval Time 1/5 sec",
                    "Random Write 4KiB [5/5]"
        )
    else:
        raise Exception("Not support")

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
    filename = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename=filename)
    close_window(tool)
    return filename


def run_anvil(target="T"):

    tool, tool_path = tool_dic["Anvil"]
    hwnd = run_tool(tool, tool_path)
    if not hwnd:
        logging.warning("run {} failed".format(tool_path))
        raise Exception(f"No {tool} ")
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383, 140, 0, 0, win32con.SWP_NOSIZE)
    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"
    hwnd_child_list = get_child_windows(hwnd)
    hwnd_qd_write = win32gui.FindWindow(None, "IO - Threaded QD (Random Write)")
    
    # disk_select = button_center(hwnd_child_list[8])
    # disk_run = button_center(hwnd_child_list[14])
    # disk_tmp = button_center(hwnd_child_list[10])
    disk_select = hwnd_child_list[8]
    disk_run = hwnd_child_list[14]
    disk_tmp = hwnd_child_list[10]
    # mouse_click(disk_select[0], disk_select[1])
    # mouse_click(disk_select[0], disk_select[1])
    click_handle(disk_select, 2)

    keybd_input(target)
    click_handle(disk_run)
    # mouse_click(disk_run[0], disk_run[1])
    # #print(disk_select)
    # mouse_move(disk_select[0], disk_select[1])
    
    for i in range(0, 3):
        while not win32gui.IsWindowVisible(hwnd_qd_write):
            time.sleep(0.1)
        while win32gui.IsWindowVisible(hwnd_qd_write):
            time.sleep(0.1)
    else:
        time.sleep(3)
    # win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383,140,0,0, win32con.SWP_NOSIZE)
    # time.sleep(3)

    # 开始测试
    click_handle(disk_tmp, 1)
    time.sleep(2)
    click_handle(disk_tmp, 1)
    time.sleep(2)
    # mouse_click(disk_tmp[0], disk_tmp[1], 2)
    # mouse_click(disk_tmp[0], disk_tmp[1], 2)
    filename = tool
    # screenPrt.ScreenPrintWin().save_bitmap(bmp_filename= filename)
    filename = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename=filename)
    # time.sleep(10)
    close_window(tool)
    return filename


def run_atto_disk_benchmark(target="T", mode=2, depth=4):

    tool, tool_path = tool_dic["ATTO"]
    hwnd = run_tool(tool, tool_path)
    if not hwnd:
        logging.warning("run {} failed".format(tool_path))
        raise Exception(f"{tool} failed")
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383, 0, 0, 0, win32con.SWP_NOSIZE)

    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"

    mode_hwnd_tag = mode + 10
    hwnd_child_list = get_child_windows(hwnd)

    # disk_select = button_center(hwnd_child_list[2])
    # mouse_click(disk_select[0], disk_select[1])
    # mouse_click(disk_select[0], disk_select[1])
    disk_select = hwnd_child_list[2]
    click_handle(disk_select, 2)
    time.sleep(1)

    keybd_input(target)

    mode_select = button_center(hwnd_child_list[mode_hwnd_tag])
    mouse_click(mode_select[0], mode_select[1])

    pattern_button = hwnd_child_list[15]
    depth_button = hwnd_child_list[18]

    if mode == 1:
        print(1)
        click_handle(pattern_button, 2, "R")
    elif mode == 2:
        click_handle(depth_button, 2, chr(depth))
    elif mode == 3:
        print("else")
    else:
        print("else")

    start_button = hwnd_child_list[27]
    click_handle(start_button, 1)

    while win32gui.GetWindowText(hwnd_child_list[-10]) == "":
        time.sleep(1)
        # elapsed_time = time.time() - start_time
        # assert elapsed_time < 6000 , "timeout!"

    filename = tool + str(mode)
    filename = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename=filename)

    cmd = r'taskkill /F /IM "ATTO Disk Benchmark.exe"'
    os.system(cmd)
    return filename


def run_txbench(target="T"):
    target = target.upper()
    tool, tool_path = tool_dic["TXB"]
    hwnd = run_tool(tool, tool_path)
    if not hwnd:
        logging.warning("run {} failed".format(tool_path))
        return False
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383, 140, 0, 0, win32con.SWP_NOSIZE)
    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"
    hwnd_child_list = get_child_windows(hwnd)
    # start_button = button_center(hwnd_child_list[13])
    start_button = hwnd_child_list[13]

    cnt = win32api.GetLogicalDriveStrings().split(":\\\x00").index(target)
    # disk_select = button_center(hwnd_child_list[10])
    disk_select = hwnd_child_list[10]
    click_handle(disk_select, 2)
    # mouse_click(disk_select[0], disk_select[1])
    # mouse_click(disk_select[0], disk_select[1])
    for k in range(0, cnt):
        keybd_input("(")
        time.sleep(1)
    
    start_init = win32gui.GetWindowText(hwnd_child_list[13])
    # mouse_click(start_button[0], start_button[1])
    click_handle(start_button)
    time.sleep(4)

    start_time = time.time()
    while win32gui.GetWindowText(hwnd_child_list[13]) != start_init:
        time.sleep(1)
        elapsed_time = time.time() - start_time
        assert elapsed_time < 6000, "timeout!"

    filename = tool
    filename = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename=filename)

    close_window(tool)
    return filename


def get_diskinfo(target):
    if isinstance(target, int):
        target = f"Disk {target}"
    elif re.match("[a-zA-Z]", target):
        if target.upper() in win32api.GetLogicalDriveStrings().split(":\\\x00"):
            target = f"{target.upper()}:"
        else:
            raise Exception(f"target: {target} does not exists !")
    else:
        raise Exception(f"target: {target} wrong")

    tool, tool_path = tool_dic["CDI"]
    hwnd = run_tool(tool, tool_path)
    if not hwnd:
        logging.warning("run {} failed".format(tool_path))
        return False
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 2000, 800, win32con.SWP_SHOWWINDOW)
    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"
    hwnd_child_list = get_child_windows(hwnd)

    for i in hwnd_child_list[2: 9]:
        if target in win32gui.GetWindowText(i).split("\n")[-1]:
            logging.info(f"click_handle {target} {i}")
            click_handle(i)
            break
        if i == hwnd_child_list[9]:
            raise Exception(f"target: {target} not find")

    filename = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename=tool)
    close_window(tool)
    time.sleep(1)
    return filename


def run_hdtune(disk_number=100):

    tool, tool_path = tool_dic["HDtune"]
    hwnd = run_tool(tool, tool_path)
    if not hwnd:
        logging.warning("run {} failed".format(tool_path))
        return False

    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383, 0, 0, 0, win32con.SWP_NOSIZE)
    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"
    hwnd_child_list = get_child_windows(hwnd)

    disk_select = button_center(hwnd_child_list[0])
    mouse_click(disk_select[0], disk_select[1], 2)
    dp = diskpart_new.Diskpart()
    disk_select_move_cnt = dp.list_disk().index(str(disk_number))
    dp.quit_diskpart()
    mouse_click(disk_select[0], disk_select[1] + 14 * (disk_select_move_cnt + 1))

    x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd_child_list[6])
    if win32gui.GetWindowText(hwnd_child_list[12]) != "基准":
        print(win32gui.GetWindowText(hwnd_child_list[12]))
        hwnd_child_list = get_child_windows(hwnd)
        mouse_click(x1 + 2, y1 + 2)
        time.sleep(2)

    start_button = hwnd_child_list[13]
    read_button = hwnd_child_list[14]
    write_button = hwnd_child_list[15]

    start_init = win32gui.GetWindowText(hwnd_child_list[13])
    click_handle(read_button, 1)
    click_handle(start_button, 1)
    while win32gui.GetWindowText(hwnd_child_list[13]) != start_init:
        time.sleep(1)
    time.sleep(1)
    filename = "HDtune_read_pre"
    screenPrt.ScreenPrintWin().save_bitmap(bmp_filename=filename)

    click_handle(write_button, 1)
    click_handle(start_button, 1)
    
    hwnd_write_yes_window = win32gui.FindWindow(None, "警告!")
    hwnd_child_list = get_child_windows(hwnd_write_yes_window)
    run_write_button = hwnd_child_list[3]
    confirm_button = hwnd_child_list[0]
    click_handle(run_write_button, 1)
    time.sleep(2)
    click_handle(confirm_button, 1)
    time.sleep(5)

    while win32gui.GetWindowText(hwnd_child_list[13]) != start_init:
        time.sleep(1)
        # elapsed_time = time.time() - start_time
        # assert elapsed_time < 600 , "timeout!"
    time.sleep(2)
    filename = "HDtune_write"
    output_w = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename=filename)
    time.sleep(5)

    click_handle(read_button, 1)
    click_handle(start_button, 1)

    while win32gui.GetWindowText(hwnd_child_list[13]) != start_init:
        time.sleep(1)

    time.sleep(1)
    filename = "HDtune_read"
    output_r = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename=filename)
    close_window(tool)
    return output_w, output_r


def run_hdtune_fs(target="X"):
    tool, tool_path = tool_dic["HDtune"]
    hwnd = run_tool(tool, tool_path)
    if not hwnd:
        logging.warning("run {} failed".format(tool_path))
        return False

    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383, 0, 0, 0, win32con.SWP_NOSIZE)
    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"
    hwnd_child_list = get_child_windows(hwnd)
    disk_select = button_center(hwnd_child_list[0])
    mouse_click(disk_select[0], disk_select[1], 2)

    dp = diskpart_new.Diskpart()
    disk_select_move_cnt = dp.volume_to_disk(target)
    dp.quit_diskpart()

    mouse_click(disk_select[0], disk_select[1] + 14 * (disk_select_move_cnt + 1))

    x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd_child_list[6])
    if win32gui.GetWindowText(hwnd_child_list[12]) != "文件基准":
        print(win32gui.GetWindowText(hwnd_child_list[12]))
        hwnd_child_list = get_child_windows(hwnd)
        mouse_click(x1 + 2, y1 + 2)
        time.sleep(2)

    print(win32gui.GetWindowText(hwnd_child_list[12]))
    hwnd_child_list = get_child_windows(hwnd)

    start_button = hwnd_child_list[14]
    start_init = win32gui.GetWindowText(hwnd_child_list[14])

    click_handle(start_button, 1)

    while win32gui.GetWindowText(hwnd_child_list[14]) != start_init:
        time.sleep(1)
    time.sleep(1)

    filename = "HDtune_fs"
    output_r = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename=filename)
    close_window(tool)
    return output_r


def run_pc_mark7(target=0):

    tool = "PCMark 7 Professional Edition v1.4.0"
    tool_path = r"C:\Program Files\Futuremark\PCMark 7\bin\PCMark7.exe"
    hwnd = run_tool(tool, tool_path, 15)
    if not hwnd:
        logging.warning("run {} failed".format(tool_path))
        return False
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 10, 10, 1038, 746, win32con.SWP_SHOWWINDOW)
    assert win32gui.GetWindowText(hwnd) == tool, "run tool name wrong!"
    window_base = win32gui.GetWindowRect(hwnd)
    disk_select = (window_base[0] + 171, window_base[1] + 478)
    run_button = (window_base[0] + 825, window_base[1] + 215)
    cnt = win32api.GetLogicalDriveStrings().split(":\\\x00").index(target)
    mouse_click(disk_select[0], disk_select[1])
    time.sleep(1)
    mouse_click(disk_select[0], disk_select[1] + (cnt + 1) * 21)
    mouse_click(run_button[0], run_button[1])
    
    # stop_flag = (window_base[0] + 600, window_base[1] + 220)
    time.sleep(10)
    stop_flag = (window_base[0] + 365, window_base[1] + 111)
    mouse_move(window_base[0] + 365, window_base[1] + 111)
    mouse_move(window_base[0], window_base[1])
    init_rgb = ImageGrab.grab(bbox=win32gui.GetWindowRect(hwnd)).getpixel((stop_flag))
    while ImageGrab.grab(bbox=win32gui.GetWindowRect(hwnd)).getpixel((stop_flag)) == init_rgb:
        # print(ImageGrab.grab(bbox=win32gui.GetWindowRect(hwnd)).getpixel((stop_flag)))
        time.sleep(5)

    filename = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename=tool)
    close_window(tool)
    return filename


def run_pc_mark8(target=0):

    # tool, tool_path= tool_dic["CDI"]
    # hwnd = run_tool(tool , tool_path)
    tool = "PCMark 8 Professional Edition "
    tool_path = r"C:\Program Files\Futuremark\PCMark 8\bin\PCMark8.exe"
    hwnd = run_tool(tool, tool_path, 10)
    if not hwnd:
        logging.warning("run {} failed".format(tool_path))
        return False
    hwnd_xy = win32gui.GetWindowRect(hwnd)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, hwnd_xy[0], hwnd_xy[1], hwnd_xy[2] - hwnd_xy[0],
                          hwnd_xy[3] - hwnd_xy[1], win32con.SWP_SHOWWINDOW)
    window_base = win32gui.GetWindowRect(hwnd)

    mouse_click(window_base[0] + 999, window_base[1] + 66)
    mouse_click(window_base[0] + 900, window_base[1] + 200)
    
    disk_select = (window_base[0] + 900, window_base[1] + 450)
    run_button = (window_base[0] + 1100, window_base[1] + 660)
    
    cnt = win32api.GetLogicalDriveStrings().split(":\\\x00").index(target)
    mouse_click(disk_select[0], disk_select[1])
    time.sleep(1)

    mouse_click(disk_select[0], disk_select[1] + (cnt+1)*21)
    mouse_click(run_button[0], run_button[1])
    
    # stop_flag = (window_base[0] + 600, window_base[1] + 220)
    while win32gui.GetWindowRect(hwnd)[0] >= 0:
        time.sleep(1)

    while win32gui.GetWindowRect(hwnd)[0] < 0:
        time.sleep(1)
    time.sleep(5)
    filename = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename=tool)
    close_window(tool)
    cmd = r'taskkill /F /IM "PCmark8.exe"'
    os.system(cmd)
    return filename


def run_h2testw(target="H", test_range=0):
    """
    run h2testw
    :param target: volume letter
    :param test_range: 0- all; 1-99  percent of all ,  >100  real size,  test_range =110 ,test size is 110m;
    :return: image name
    """

    tool = "H2testw"
    tool_path = r"D:\SSD performance\h2testw_1.4\h2testw.exe"
    hwnd = run_tool(tool, tool_path, 4)

    hwnd_child_list = get_child_windows(hwnd)
    click_handle(hwnd_child_list[14])  # english
    click_handle(hwnd_child_list[0])  # select target
    time.sleep(4)
    hwnd_select = win32gui.FindWindow(None, "浏览文件夹")
    hwnd_select_childlist = get_child_windows(hwnd_select)
    print(hwnd_select_childlist)
    click_handle(hwnd_select_childlist[6], cnt=2)  # click path
    keybd_input(target, idle=0)
    keybd_input_combination(16, 186)  # input ：
    click_handle(hwnd_select_childlist[9])  # cofrim

    hwnd_child_list = get_child_windows(hwnd)
    if target not in win32gui.GetWindowText(hwnd_child_list[9]):
        raise Exception(f"Select {target} failed")
    if "Existing test data" in win32gui.GetWindowText(hwnd_child_list[11]):
        raise Exception(win32gui.GetWindowText(hwnd_child_list[11]))

    if test_range == 0:
        click_handle(hwnd_child_list[1])  # all avaliable space
    else:
        click_handle(hwnd_child_list[2])  # only some space
        if test_range < 100:  # test_range % by all avaliable space, if test_range = 50，test size is 50%
            test_size = int(win32gui.GetWindowText(hwnd_child_list[1]).split()[3][1:])*test_range//100
            click_edit_and_input(hwnd_child_list[3], str(test_size))

        elif test_range < int(win32gui.GetWindowText(hwnd_child_list[1]).split()[3][1:]):  # test size 1000M
            click_edit_and_input(hwnd_child_list[3], str(test_range))
        else:
            raise Exception("run err")

    click_handle(hwnd_child_list[5])  # start

    click_handle(get_child_windows(win32gui.FindWindow(None, "h2testw"))[0])
    progress_childlist = get_child_windows(win32gui.FindWindow(None, r"H2testw | Progress"))

    while not win32gui.GetWindowText(progress_childlist[9]):
        time.sleep(1)
    while "remaining" in win32gui.GetWindowText(progress_childlist[9]):
        time.sleep(1)
    time.sleep(5)
    filename = screenPrt.ScreenPrintWin().save_bitmap(bmp_filename=tool)
    click_handle(progress_childlist[0])
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    return filename


if __name__ == "__main__":
    # #print(get_all_child("H2testw | Progress"))
    # #print(get_all_child("浏览文件夹"))
    # #run_HDtune_fs("H")
    get_diskinfo("z")
    # run_h2testw("H",1000)
    # #print(win32api.GetLogicalDriveStrings())
