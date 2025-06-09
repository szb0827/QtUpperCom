import numpy as np
import matplotlib.pyplot as plt
import pywt
from itertools import islice

class BackgroundRejection():
    def __init__(self, file_path):
        self.file_path = open(file_path, 'r')

    def file_process(self):
        length = 0
        temp = list()
        maxy = 0

        # 获取文件整体行数，并除去固定包头长度
        for c in self.file_path:
            length += 1
        length = length - 28
        # 文件指针跳转到开头
        self.file_path.seek(0)
        # 从13行开始读取length行
        result = self.read_lines_from(self.file_path, 13, length)

        # 除去0数据，并将字符串转换为数字
        for i in range(len(result)):
            maxy = max(maxy, int(result[i]))
            temp.append(int(result[i]))

        x = np.linspace(0, len(temp), len(temp))

        # 小波分解
        coeffs = pywt.wavedec(temp, 'db4', level=4)

        # 保留低频分量作为本底
        background_coeffs = [coeffs[0]] + [np.zeros_like(c) for c in coeffs[1:]]
        background_estimate = pywt.waverec(background_coeffs, 'db4')

        # 扣除本底
        net_spectrum = temp - background_estimate

        # 绘制结果
        plt.figure(figsize=(12, 6))
        plt.subplot(2, 1, 1)
        plt.plot(x, temp, label='Total Spectrum')
        plt.plot(x, background_estimate, label='Estimated Background')
        plt.xlabel('Channel')
        plt.ylabel('Counts')
        plt.title('Total Spectrum and Estimated Background')
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.plot(x, net_spectrum, label='Net Spectrum')
        plt.xlabel('Channel')
        plt.ylabel('Counts')
        plt.title('Net Spectrum after Background Subtraction')
        plt.legend()

        plt.gcf().canvas.manager.set_window_title("Background Rejection")
        plt.tight_layout()
        plt.show()

    def read_lines_from(self, file, start_line, n_lines):
        # 跳过前 start_line-1 行，读取后续的 n_lines 行
        lines = list(islice(file, start_line - 1, start_line - 1 + n_lines))
        return [line.strip() for line in lines]

