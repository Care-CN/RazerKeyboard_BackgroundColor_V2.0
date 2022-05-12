# -*- coding:utf-8 -*-
# ! python3
# 获取1921*678像素大小的键盘颜色图中，以113为1像素块单位的各像素16进制颜色
from PIL import Image
import PySimpleGUI as sg
import xlsxwriter
import datetime

# 需满足的条件
# length/block_size=17
# width/block_size=6
length = 1921  # 图片规范化后的长
width = 678  # 图片规范化后的宽
block_size = 113  # 大像素块尺寸


def ima(file_path, saveimg, dif_fontcolor):
    global length
    global width
    global block_size
    img_name = ''
    old_img = Image.open(file_path)  # 读取系统的内照片
    old_img = old_img.resize((17, 6), resample=Image.Resampling.BILINEAR)
    img = old_img.resize((length, width), Image.Resampling.NEAREST)
    # img = Image.open(file_path)
    if saveimg:
        img_name = file_path.split('.')[0] + '_pixelate.' + file_path.split('.')[1]
        img.save(img_name)
    starter = int(block_size / 2) + 1  # 初始像素点
    i = 0  # 列
    j = 0  # 行
    mult = block_size  # 倍数
    # print(img.size)  # 打印图片大小
    new_width = img.size[0]  # 长度
    new_height = img.size[1]  # 宽度
    xls_name = file_path.split('.')[0] + '_pixelate.' + 'xlsx'
    workbook = xlsxwriter.Workbook(xls_name)
    worksheet = workbook.add_worksheet('RAZER')
    for k in range(6):
        worksheet.set_row(k, 50)  # 行高单位为字符高度
    cell_format = [[i for j in range(20)] for i in range(20)]
    while (starter + i * mult) <= new_width:
        j = 0
        while (starter + j * mult) <= new_height:
            a = img.getpixel((starter + i * mult, starter + j * mult))
            # 判断是否需要区分冷暖色来决定文字颜色
            if dif_fontcolor:
                # RGB转YUV模式，Y为明亮度（灰阶），因此只需要获得 Y 的值而判断他是否足够亮，RGB_YUV_Y越小，颜色越深，阈值为自定值
                RGB_YUV_Y = a[0] * 0.299 + a[1] * 0.587 + a[2] * 0.114
                if RGB_YUV_Y > 107:
                    font_color = 'black'
                else:
                    font_color = 'white'
            else:
                font_color = 'black'
            rgb = str(a[0]) + ',' + str(a[1]) + ',' + str(a[2])
            RGB = rgb.split(',')  # 将RGB格式划分开来
            color = ''
            for a in RGB:
                num = int(a)
                # 将R、G、B分别转化为16进制拼接转换并大写  hex() 函数用于将10进制整数转换成16进制，以字符串形式表示
                color += str(hex(num))[-2:].replace('x', '0').upper()
            cell_format[j][i] = workbook.add_format(
                {'bg_color': color, 'align': 'vcenter', 'font_color': font_color})
            worksheet.write(j, i, color, cell_format[j][i])
            j += 1
        i += 1
    name = [img_name, xls_name]
    workbook.close()
    return name


def main():
    sg.theme('DarkPurple1')
    layout = [
        [sg.Text('RAZER黑寡妇V2——图片像素化转背景色', font=('微软雅黑', 12))],
        [sg.Text('', key='filename', size=(80, 1), font=('微软雅黑', 10), text_color='white')],
        [sg.Output(size=(80, 10), font=('微软雅黑', 10), key='output')],
        [sg.Checkbox('保存像素块图片', key='saveimg', default=True, font=('微软雅黑', 10)),
         sg.Checkbox('开启文字对比度', key='fontcolor', default=False, font=('微软雅黑', 10))],
        [sg.FileBrowse('选择文件', key='file', target='filename'),
         sg.Button('开始转换'),
         sg.Button('退出'),
         sg.Button('使用须知')]
    ]
    window = sg.Window('图片像素化转背景色', layout, font=('微软雅黑', 15), default_element_size=(50, 1))
    while True:
        event, values = window.read()
        if event in (None, '退出'):
            break
        if event == '使用须知':
            window.FindElement('output').Update('')  # 清空输出框
            print('#########################')
            print('--使用须知：')
            print('-请先选择文件后再点击开始转换；')
            print('-"保存像素块图片"为可选内容，默认保存，保存位置为原图片所在文件夹；')
            print('-像素块图片名称：原图名称+“_pixelate.jpg/.png”')
            print('-表格文件名称：原图名称+“_pixelate.xls”')
            print('-可能存在未知bug。')
            print('-推荐使用的调色网站：\n'
                  '  ColorSpace:    https://mycolor.space/\n'
                  '  coolors:  https://coolors.co/\n'
                  '  uigradients:  https://uigradients.com/\n'
                  '  coolhue 2.0:  https://webkul.github.io/coolhue/\n'
                  '  WebGradients:  https://webgradients.com')
            print('#########################')
        if event == '开始转换':
            time = datetime.datetime.now()
            if values['file'] and values['file'].split('.')[1] in ['png', 'jpg']:
                name = ima(values['file'], values['saveimg'], values['fontcolor'])
                print('*************************' + '\n' + '转换成功   ' + '   ^_^')
                print('时间：  ', time)
                if values['saveimg']:
                    print('png/jpg文件位置：', name[0])
                print('xls文件位置：', name[1] + '\n' + '*************************')
            else:
                print('!!!!!!!!!!!!!!!!!!!!!!!!!\n'
                      '时间：  ', time, '\n'
                      '未选取文件或文件非"png"、"jpg"格式  T^T\n'
                      '请先选择正确的文件\n'
                      '!!!!!!!!!!!!!!!!!!!!!!!!!')
    window.close()


if __name__ == "__main__":
    main()
