from PIL import Image
import win32gui, win32api,win32con
import csv
from PIL import ImageDraw, ImageGrab
import time
import os
import datetime
import logging


def mouse_move(new_x, new_y):
    point = (new_x, new_y)
    win32api.SetCursorPos(point)


def mouse_click(x, y, idle=1):
    mouse_move(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(idle)


def keybd_single_char(input_key, idle=1):
    input_key = ord(input_key)
    win32api.keybd_event(input_key, 0, 0, 0)
    win32api.keybd_event(input_key, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(idle)


def button_center(phwnd):
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
        else:
            time.sleep(10)
    return hwnd


def run_assd(target="F", size="1G"):
    tool = "AS SSD Benchmark 2.0.6694.23026"
    tool_path = r"D:\AS-SSD-Benchmark2.0.6694\AS SSD Benchmark.exe"
    hwnd = run_tool(tool, tool_path)
    if not hwnd:
        logging.warning("run {} failed".format(tool_path))
        return False

    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 383, 140, 0, 0, win32con.SWP_NOSIZE)

    hwndChildList = []
    win32gui.EnumChildWindows(hwnd, lambda hwnd, param: param.append(hwnd), hwndChildList)

    disk_select = hwndChildList[10]
    write_aactime = hwndChildList[31]
    size_select = hwndChildList[0]

    click_handle(disk_select, 2, target)

    hwnd1 = win32gui.FindWindowEx(hwnd, None, None, "Start")

    click_handle(hwnd1, 1)
    score = hwndChildList[6]
    while win32gui.GetWindowText(score) == r"----" or win32gui.GetWindowText(
            write_aactime) == r"0.000 ms" or win32gui.GetWindowText(write_aactime) == r"-.-- ms":
        time.sleep(5)
    capture_window = win32gui.FindWindow(0, tool)

    svn = "svn333"
    time_tag = time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time()))
    context = [svn, time_tag] + \
           [(win32gui.GetWindowText(hwndChildList[x])).split()[0] for x in [18, 22, 19, 17, 23, 21, 30, 31, 5, 7, 6]]
    assd_csv(context)

    filename = "{}-{}.PNG".format(time_tag, svn)
    ImageGrab.grab(bbox=win32gui.GetWindowRect(capture_window)).save(filename)
    win32gui.PostMessage(win32gui.FindWindow(0, tool), win32con.WM_CLOSE, 0, 0)
    return filename





class AssdResult(object):

    def __init__(self, img=""):
        self.img = Image.open(img)
        self.draw = ImageDraw.Draw(self.img)


    def add_arrow(self, xy=(), up_or_down=0):
        """
        :param xy: top center point (x, y)
        :param up_or_down: arrow direction
        :return: None
        """
        size = 5
        x, y = xy
        if up_or_down == 0:
            color = "yellow"
            up = -1
        else:
            color = "red"
            up = 1
        points = [(x, y + 5 * size * up_or_down),
                  (x + 2 * size, y - 2 * size * up + 5 * size * up_or_down),
                  (x + 1 * size, y - 2 * size * up + 5 * size * up_or_down),
                  (x + 1 * size, y - 5 * size * up + 5 * size * up_or_down),
                  (x - 1 * size, y - 5 * size * up + 5 * size * up_or_down),
                  (x - 1 * size, y - 2 * size * up + 5 * size * up_or_down),
                  (x - 2 * size, y - 2 * size * up + 5 * size * up_or_down)]
        self.draw.polygon(points, fill=color)

    def save(self, filename=""):
        self.img.save(filename, "PNG")
        return filename


def get_result(tool="AS SSD Benchmark 2.0.6694.23026"):
    hwnd = win32gui.FindWindow(None, tool)
    hwndChildList = []
    win32gui.EnumChildWindows(hwnd, lambda hwnd, param: param.append(hwnd), hwndChildList)
    return ["svn333", "2018-1-1"] + \
           [(win32gui.GetWindowText(hwndChildList[x])).split()[0] for x in [18, 22, 19, 17, 23, 21, 30, 31, 5, 7, 6]]


def assd_csv(context=[], file="log.csv"):
    csvfile = open(file, 'ab')
    writer = csv.writer(csvfile)
    writer.writerow(context)
    csvfile.close()


def get_show_picture(original=r"C:\Users\zc\OneDrive\Goke\2302LT\winbench_2019-04-04-12-31-01\AS SSD Benchmark 2.0.6694.23026_2019-04-04-12-33-23.png" ,file="log.csv"):
    points = [
        (318, 168),
        (478, 168),
        (318, 204),
        (478, 204),
        (318, 240),
        (478, 240),
        (318, 276),
        (478, 276),
        (318, 318),
        (478, 318),
        (398, 348)
    ]

    csvfile = open(file, 'r')
    reader = list(csv.reader(csvfile))
    basic = reader[1][2:]
    today = reader[-1][2:]
    csvfile.close()

    im = AssdResult(original)
    for i in range(0, 11):
        difference = (float(today[i]) - float(basic[i])) / float(basic[i])
        if difference > 0.01:
            im.add_arrow(points[i], 0)
        elif difference < -0.01:
            im.add_arrow(points[i], 1)
        else:
            pass
    im.img.save("Assd.png","PNG")


if __name__ == "__main__":
    #assd_csv(get_result())
    #get_show_picture("ASSSD-1.png")
    get_show_picture(run_assd("E"))

