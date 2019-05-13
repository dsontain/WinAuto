import shutil
import zipfile
import os
import time
import fire
import sys
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def modify_report(start=None,  output="", template=r'template.docx', path=None):

    if not path:
        path = os.getcwd()
    time_tag = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    if output:
        time_tag = output# + "_" + time_tag
    tmp_path = "{}\\{}".format(path, time_tag)

    if not template.endswith("zip"):

        template = modify_file_postfix(template, "zip")
        shutil.unpack_archive(template, time_tag)
        modify_file_postfix(template, "docx")
    else:
        shutil.unpack_archive(template, time_tag)

    images = []
    for n in range(len(os.listdir("{}\\word\\media".format(tmp_path)))):
        filename = "{}\\word\\media\\image{}.png".format(tmp_path, n+1)
        images.append(filename)

    original_images = ["CrystalDiskInfo",
                       "AS SSD Benchmark",
                       "Untitled",
                       "TxBENCH",
                       "Anvil",
                       "HDtune_read_before",
                       "HDtune_write"
                       "HDtune_read"
                       "PCmark7"
                       "PCmark8"
                       ]

    original_images =[
        'CrystalDiskInfo 7.6.0.png',
        'AS SSD Benchmark 2.0.6694.23026.png',
        'CrystalDiskMark 6.1.0 Beta1 x64.png',
        'Untitled - ATTO Disk Benchmark2.png',
        'TxBENCH - New project.png',
         "Anvil's Storage Utilities 1.1.0 (2014-January-1).png" ,
        'HDtune_read_pre.png',
        'HDtune_write.png',
        'HDtune_read.png',
        'PCmark7.PNG',
        'PCmark8.PNG'
    ]



    step = len(images) // len(original_images)
    print(images)
    for index, image in enumerate(original_images):
        shutil.copyfile(image, images[index*step + start -1])
        #image_add_label(text=time_tag, imagefile=images[index])

    


    output = shutil.make_archive(time_tag, 'zip', tmp_path)

    return modify_file_postfix(output, "docx")

def modify_file_postfix(src="1.txt", dst=None):

    dst = src[:src.find(".")] + "." + dst

    os.rename(src, dst)

    return dst

def image_add_label(text="", imagefile="", output="", 
                    position=(0,0), rgb=(255, 0, 0), size=10, 
                    font=r"C:\Windows\Fonts\simhei.ttf"):


    font = ImageFont.truetype(font, size)

    im1 = Image.open(imagefile)

    draw = ImageDraw.Draw(im1)
    draw.text(position, text, rgb, font=font)    #设置文字位置/内容/颜色/字体
    draw = ImageDraw.Draw(im1)                          #Just draw it!

    #另存图片
    if output:
        im1.save(output)
    else:
        im1.save(imagefile)

    return output



if __name__=="__main__":
    output = modify_report(start=int(input("start:")), output=input("your report name:"), template="template-1.docx")
    # while True:
    #
    #     start = int(input("start:"))
    #     step = int(input("step:"))
    #     if start in [1,2,3] and step in [1,2,3]:
    #         break
    #     else:
    #         print("start and step must be 1/2/3")
    #
    #
    # if 1 == step:
    #     template = r'template-1.docx'
    # elif 2 == step:
    #     template= r'template-2.docx'
    # elif 3 == step:
    #     template= r'template-3.docx'
    # else:
    #    pass
    #
    # output = modify_report(start=start, step=step, output=input("your report name:"), template=template)
    # print("your report : {}".format(output))
    # time.sleep(5)


#shutil.unpack_archive(r'C:\Users\zc\OneDrive\github\WinAuto\report\model.zip', r'C:\Users\zc\OneDrive\github\WinAuto\report')

# shutil.make_archive('archive_name', 'zip', r'C:\Users\zc\OneDrive\github\WinAuto\report')

# 默认模式r,读
# azip = zipfile.ZipFile(r'C:\Users\zc\OneDrive\github\WinAuto\report\model.zip')  # ['bb/', 'bb/aa.txt']
# # 返回所有文件夹和文件
# print(azip.namelist())
# # # 返回该zip的文件名
# print(azip.filename)

# # 压缩文件里bb文件夹下的aa.txt
# # 原来文件大小
# # print(azip_info.file_size)
# # # 压缩后大小
# # print(azip_info.compress_size)

# # # 这样可以求得压缩率，保留小数点后两位
# # print('压缩率为{:.2f}'.format(azip_info.file_size/azip_info.compress_size))
# azip.extractall()

# azip = zipfile.ZipFile('bb.zip', 'w')
# # 必须保证路径存在,将bb件夹（及其下aa.txt）添加到压缩包,压缩算法LZMA
# azip.write('D:/bb/aa.txt', compress_type=zipfile.ZIP_LZMA)
# # 写入一个新文件到压缩包中，data是该文件的具体内容，可以是str或者是byte。
# # 这里是新建一个bb文件夹，其下再新建一个cc.txt,将hello world写入到文本中
# azip.writestr('bb/cc.txt', data='Hello World', compress_type=zipfile.ZIP_DEFLATED)
# # 关闭资源
# azip.close()
