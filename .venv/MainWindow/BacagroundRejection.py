import numpy as np
import matplotlib.pyplot as plt
import pywt
from itertools import islice

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

plt.tight_layout()
plt.show()