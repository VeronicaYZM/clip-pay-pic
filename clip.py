# encoding:utf-8

"""
功能：提取微信支付和支付宝收款码中的二维码部分

作者：追梦人物

版本：0.1.0

修改历史：
    V0.1.0 - 2019/02/13 - 提取微信支付和支付宝收款码中的二维码部分

----------------------------------------------

使用方法：

确保安装了 pillow：`pip install pillow==4.1.0`

1. 将标准的微信支付或者支付宝收款码放到脚本所在目录下

2. 在脚本所在文件夹下创建一个 result 目录

3. 运行脚本：python clip.py

4. result 目录下查看结果

注意：仅在官方默认收款码样式下有测试，其它样式的收款码不保证有效。
"""

import glob
from PIL import Image

if __name__ == '__main__':
    filenames = glob.glob('*.png')  # 微信支付收款码导出为 png 格式
    filenames.extend(glob.glob('*.jpg'))  # 支付宝收款码导出为 jpg 格式

    for filename in filenames:
        with Image.open(filename) as img:
            img.convert('RGBA')
            pix_data = img.load()

            # 图片左上角为原点，横向为 x 轴（向右为正方向），纵向为 y 轴（向下为正方向）
            width, height = img.size  # 图片宽和高
            mid_height = height // 2  # 图片正中纵坐标

            # 确定左边界横坐标：
            x_left = 0
            for x in range(width):
                rgba = pix_data[x, mid_height]
                if rgba[:3] == (255, 255, 255):
                    x_left = x
                    break

            # 确定右边界横坐标：
            x_right = width - 1  # 右边界
            for x in range(width - 1, 0, -1):
                rgba = pix_data[x, mid_height]
                if rgba[:3] == (255, 255, 255):
                    x_right = x
                    break

            h = x_right - x_left  # 白色背景高度（正方形）
            mid_height_rgba = pix_data[x_left, mid_height]
            if filename.endswith('png'):
                # 微信支付往下确定下边界纵坐标，因为当设置了收款金额时，金额显示在上方
                y_bottom = mid_height
                for y in range(mid_height, height):
                    rgba = pix_data[x_left, y]
                    if rgba != mid_height_rgba:
                        y_bottom = y
                        break
                box = (x_left, y_bottom - h, x_right, y_bottom)
            else:
                # 支付宝往上确定上边界纵坐标，因为当设置了收款金额时，金额显示在下方
                y_top = mid_height
                for y in range(mid_height, 0, -1):
                    rgba = pix_data[x_left, y]
                    if rgba != mid_height_rgba:
                        y_top = y
                        break
                box = (x_left, y_top, x_right, y_top + h)
            crop = img.crop(box)  # box 参数为四元组，分别为左上角和右下角的横纵坐标
            crop.save('./result/{}'.format(filename))
