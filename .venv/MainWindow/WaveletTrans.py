import numpy as np
import matplotlib.pyplot as plt
import pywt
from itertools import islice

def find_peaks_wavelet(spectrum, wavelet='mexh', scale=5):
    """
    基于小波变换的寻峰算法
    :param spectrum: 能谱数据
    :param wavelet: 小波基（如墨西哥帽小波'mexh'）
    :param scale: 尺度参数（控制峰宽度的敏感性）
    :return: 峰位置列表
    """
    # 计算小波系数
    coeffs, _ = pywt.cwt(spectrum, scales=[scale], wavelet=wavelet)
    coeffs = coeffs[0]  # 单尺度结果

    # 寻找小波系数的局部极大值（绝对值）
    peaks = []
    for i in range(1, len(coeffs) - 1):
        if abs(coeffs[i]) > abs(coeffs[i - 1]) and abs(coeffs[i]) > abs(coeffs[i + 1]):
            peaks.append(i)
    return peaks

def read_lines_from(file, start_line, n_lines):
    # 跳过前 start_line-1 行，读取后续的 n_lines 行
    lines = list(islice(file, start_line - 1, start_line - 1 + n_lines))
    return [line.strip() for line in lines]

dataFile = open('data/fitting3.txt','r')
length = 0
result = list()
temp = list()
maxy = 0
FWHM = 0
energyResolution = 0

# 获取文件整体行数，并除去固定包头长度
for c in dataFile:
    length += 1
length = length - 28
# 文件指针跳转到开头
dataFile.seek(0)
# 从13行开始读取length行
result = read_lines_from(dataFile, 13, length)

# 除去0数据，并将字符串转换为数字
for i in range(len(result)):
    maxy = max(maxy, int(result[i]))
    temp.append(int(result[i]))

x = np.linspace(0, len(temp), len(temp))

# left_index = max(0, temp.index(maxy) - 100)
# right_index = min(len(temp), temp.index(maxy) + 100)
# #
# x_subset = x[left_index:right_index]
# y_subset = temp[left_index:right_index]

# popt, pcov = curve_fit(self.read.gaosi, x_subset, y_subset,
#                        p0=[max(y_subset), x_subset[np.argmax(y_subset)], np.std(x_subset)])
# amp_fit, cen_fit, wid_fit = popt
# # amplitude 初始振幅 = 数据峰谷差值（粗略估计峰高）A，mean 数据均值 = y最大值对应的x的位置（假设峰存在）u，stddev 初始标准差 = x范围的1/10 sigma
# print("A = ", max(y_subset), "u = ", x_subset[np.argmax(y_subset)], " sigma = ", wid_fit + 1)
# x_fit = np.linspace(min(x_subset), max(x_subset), len(x_subset))
# y_fit = self.read.gaosi(x_fit, max(y_subset), x_subset[np.argmax(y_subset)], wid_fit + 1)

# 寻峰（尺度5，墨西哥帽小波）
peaks = find_peaks_wavelet(temp, wavelet='mexh', scale=5)

# 绘制结果
plt.figure(figsize=(12, 6))
plt.xlim(180, max(x) / 4)
plt.ylim(-2000, maxy + 20)

plt.plot(x, temp, label='Noisy Spectrum')
plt.plot(x, pywt.cwt(temp, [5], 'mexh')[0][0], 'g--', label='Wavelet Coefficients')
# for peak in peaks:
#     plt.axvline(x[peak], color='r', linestyle='--', label=f'Peak at {x[peak]:.1f}' if peak == peaks[0] else None)
plt.xlabel('Channel (Energy)')
plt.ylabel('Counts / Wavelet Coefficients')
plt.title('Peak Detection via Wavelet Transform')
plt.legend()
plt.show()