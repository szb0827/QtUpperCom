import numpy as np
import matplotlib.pyplot as plt
import pywt
from itertools import islice

class Smooth():
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

        smoothed_signal = self.wavelet_smoothing(temp)

        # 绘制结果
        plt.figure(figsize=(12, 6))
        plt.xlim(150, 600)
        plt.ylim(0, maxy + 20)

        plt.plot(x, temp, label='Noisy Signal')
        plt.plot(x, smoothed_signal, label='Smoothed Signal (Wavelet Transform)')
        plt.xlabel('Channel')
        plt.ylabel('Counts')
        plt.title('Wavelet Transform Smoothing')
        plt.gcf().canvas.manager.set_window_title("Smooth")
        plt.legend()
        plt.show()

    def read_lines_from(self, file, start_line, n_lines):
        # 跳过前 start_line-1 行，读取后续的 n_lines 行
        lines = list(islice(file, start_line - 1, start_line - 1 + n_lines))
        return [line.strip() for line in lines]

    # 小波变换平滑
    def wavelet_smoothing(self, signal, wavelet='db4', level=1):
        coeffs = pywt.wavedec(signal, wavelet, level=level)
        threshold = np.sqrt(2 * np.log(len(signal)))
        coeffs[1:] = (pywt.threshold(i, value=threshold, mode='soft') for i in coeffs[1:])
        smoothed = pywt.waverec(coeffs, wavelet)
        return smoothed

