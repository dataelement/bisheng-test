# -*- coding: utf-8 -*-
# @Time    : 2025/9/4 12:09
# @Author  : sara
# @Email   : your-email@example.com
# @File    : images.py
import numpy as np
import matplotlib.pyplot as plt


def main():
    # 快速生成sin图
    x = np.linspace(0, 2 * np.pi, 50)
    y = np.sin(x)

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, 'green', linewidth=2)
    plt.title('sin(x) Curve')
    plt.grid(True)

    # 直接保存图片
    filename = 'sin_curve.png'
    plt.savefig(filename)
    plt.close()

    # 返回文件信息
    return {'result': {'image_file': filename}}


# 执行
output = main()
print(f"图片已保存为: {output['result']['image_file']}")