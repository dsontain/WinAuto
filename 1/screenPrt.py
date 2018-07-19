import ctypes
from ctypes.wintypes import *
import win32clipboard
from win32con import *
import sys
import win32api
import win32con
import time

#time.sleep(4)


import win32api  
import win32con  
# win32api.keybd_event(18,0,0,0)  #ctrl键位码是17  

# win32api.keybd_event(44,0,0,0)  #v键位码是86  
# win32api.keybd_event(44,0,win32con.KEYEVENTF_KEYUP,0) #释放按键  
# win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0)  



#win32api.keybd_event(win32con.VK_SNAPSHOT, 1)
#time.sleep(0.5)

class BITMAPFILEHEADER(ctypes.Structure):
    _pack_ = 1  # structure field byte alignment
    _fields_ = [
        ('bfType', WORD),  # file type ("BM")
        ('bfSize', DWORD),  # file size in bytes
        ('bfReserved1', WORD),  # must be zero
        ('bfReserved2', WORD),  # must be zero
        ('bfOffBits', DWORD),  # byte offset to the pixel array
    ]
SIZEOF_BITMAPFILEHEADER = ctypes.sizeof(BITMAPFILEHEADER)

class BITMAPINFOHEADER(ctypes.Structure):
    _pack_ = 1  # structure field byte alignment
    _fields_ = [
        ('biSize', DWORD),
        ('biWidth', LONG),
        ('biHeight', LONG),
        ('biPLanes', WORD),
        ('biBitCount', WORD),
        ('biCompression', DWORD),
        ('biSizeImage', DWORD),
        ('biXPelsPerMeter', LONG),
        ('biYPelsPerMeter', LONG),
        ('biClrUsed', DWORD),
        ('biClrImportant', DWORD)
    ]
SIZEOF_BITMAPINFOHEADER = ctypes.sizeof(BITMAPINFOHEADER)






class ScreenPrintWin(object):

    @classmethod
    def keyboard_2(cls, key1=18, key2=44):
        #win32clipboard.EmptyClipboard()
        win32api.keybd_event(key1,0,0,0)  #按下第一个按键
        win32api.keybd_event(key2,0,0,0)  #按下第二个按键
        win32api.keybd_event(key2,0,win32con.KEYEVENTF_KEYUP,0) #释放按键  
        win32api.keybd_event(key1,0,win32con.KEYEVENTF_KEYUP,0) #释放按键  


    @classmethod
    def get_clipboard_bitmap(cls):
        ScreenPrintWin().keyboard_2()
        
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.CloseClipboard()
        ScreenPrintWin().keyboard_2()
        time.sleep(0.1)
        data = 0
        win32clipboard.OpenClipboard()
        #win32clipboard.EmptyClipboard()
        #print(type(win32clipboard.GetClipboardData(win32clipboard.CF_DIB)))
        #print(win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB))
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
            data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
        else:
            data = 0
            #print('clipboard does not contain an image in DIB format')
        win32clipboard.CloseClipboard()
        return data


    @classmethod
    def save_bitmap(cls, bmp_filename = 'clipboard.bmp'):
        SIZEOF_BITMAPFILEHEADER = ctypes.sizeof(BITMAPFILEHEADER)
        SIZEOF_BITMAPINFOHEADER = ctypes.sizeof(BITMAPINFOHEADER)
        
        #data = ScreenPrintWin().get_clipboard_bitmap()

        for cnt in range(0, 3):
            time.sleep(1)
            data = ScreenPrintWin().get_clipboard_bitmap()
            if data:
                break
            if cnt == 2:
                print('Three attempts to capture failed')
                return 0
            time.sleep(0.5)

        bmih = BITMAPINFOHEADER()
        ctypes.memmove(ctypes.pointer(bmih), data, SIZEOF_BITMAPINFOHEADER)
        assert bmih.biCompression == BI_BITFIELDS, 'insupported compression type {}'.format(bmih.biCompression)

        bmfh = BITMAPFILEHEADER()
        ctypes.memset(ctypes.pointer(bmfh), 0, SIZEOF_BITMAPFILEHEADER)  # zero structure
        bmfh.bfType = ord('B') | (ord('M') << 8)
        bmfh.bfSize = SIZEOF_BITMAPFILEHEADER + len(data)  # file size
        SIZEOF_COLORTABLE = 0
        bmfh.bfOffBits = SIZEOF_BITMAPFILEHEADER + SIZEOF_BITMAPINFOHEADER + SIZEOF_COLORTABLE
        with open(bmp_filename, 'wb') as bmp_file:
            bmp_file.write(bmfh)
            bmp_file.write(data)
        print('file "{}" created from clipboard image'.format(bmp_filename))
        return 1



if __name__=="__main__":
    #ScreenPrintWin().keyboard_2()
    ScreenPrintWin().save_bitmap()
