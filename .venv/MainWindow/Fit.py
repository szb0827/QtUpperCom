import matplotlib.pyplot as plt
from itertools import islice
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

class dataProcess():

    def __init__(self, dataFileAddress):
        self.dataFile = open(dataFileAddress,'r')
        self.read = readFile()

    def process(self):
        length = 0
        result = list()
        temp = list()
        maxy = 0
        FWHM = 0
        energyResolution = 0

        # 获取文件整体行数，并除去固定包头长度
        for c in self.dataFile:
            length += 1
        length = length - 28
        # 文件指针跳转到开头
        self.dataFile.seek(0)
        # 从13行开始读取length行
        result = self.read.read_lines_from(self.dataFile,13,length)

        # 除去0数据，并将字符串转换为数字
        for i in range(len(result)):
            maxy = max(maxy,int(result[i]))
            temp.append(int(result[i]))

        x = np.linspace(0, len(temp), len(temp))

        left_index = max(0,temp.index(maxy)-8)
        right_index = min(len(temp),temp.index(maxy)+15)

        x_subset = x[left_index:right_index]
        y_subset = temp[left_index:right_index]

        popt,pcov = curve_fit(self.read.gaosi,x_subset,y_subset,p0=[max(y_subset), x_subset[np.argmax(y_subset)], np.std(x_subset)])
        amp_fit, cen_fit, wid_fit = popt
        # amplitude 初始振幅 = 数据峰谷差值（粗略估计峰高）A，mean 数据均值 = y最大值对应的x的位置（假设峰存在）u，stddev 初始标准差 = x范围的1/10 sigma
        print("A = ",max(y_subset),"u = ",x_subset[np.argmax(y_subset)]," sigma = ",wid_fit+1)
        x_fit = np.linspace(min(x_subset), max(x_subset),len(x_subset))
        y_fit = self.read.gaosi(x_fit,max(y_subset), x_subset[np.argmax(y_subset)], wid_fit+1)


        #  对于高斯函数，半高宽FWHM 与标准差 𝜎 满足下式 FWHM = 2.355 * sigma
        FWHM = 2.355 * (wid_fit + 1)
        print("半高宽FWHM = ",FWHM)
        # 能量分辨等于半高宽FWHM/峰位（峰值对应的道址）,能量分辨越小越好
        energyResolution = FWHM / x_subset[np.argmax(y_subset)]
        print("能量分辨energyResolution = ",energyResolution)


        plt.figure(figsize=(10, 6))
        plt.rcParams['font.sans-serif'] = ['SimHei']    # 解决标题、坐标轴标签不能是中文的问题
        plt.rcParams['axes.unicode_minus'] = False      # 标题等默认是英文输出

        plt.xlim(180,max(x)/4)
        plt.ylim(0,maxy+20)

        plt.scatter(x, temp,  label='原始数据', color='blue')
        plt.plot(x_fit, y_fit, 'r-', label='高斯拟合', linewidth=2)

        plt.xlabel('道址', fontsize=12)
        plt.ylabel('计数', fontsize=12)
        # plt.text(450,1500,f"能量分辨率={energyResolution:.1%}",fontsize=10,bbox={'facecolor':'white','pad':5})
        plt.title('能量分辨测试', fontsize=14)
        plt.legend()    # 显示图例
        plt.grid(True, linestyle='--', alpha=0.5)
        return plt.gcf()

class readFile():
    def read_lines_from(self,file, start_line, n_lines):
        # 跳过前 start_line-1 行，读取后续的 n_lines 行
        lines = list(islice(file, start_line - 1, start_line - 1 + n_lines))
        return [line.strip() for line in lines]

    # 高斯函数
    def gaosi(self,y, amplitude, miu, sigma):
        return amplitude * np.exp(-(y - miu) ** 2 / (2 * sigma ** 2))

