import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLineEdit, QAction, QMenu,
                             QMainWindow, QFileDialog, QMessageBox, QFrame, QLabel, QRadioButton
                             , QComboBox, QButtonGroup, QStatusBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor, QPalette, QPixmap, QImage
import Fit as fit
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PIL import Image

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('上位机系统')
        self.resize(1000, 800)
        # 设置窗口logo
        icon = QIcon("logo/logo1.jpeg")
        self.setWindowIcon(icon)

        # 菜单栏
        self.main_menu = self.menuBar()
        # 文件菜单
        self.file_menu()
        setting_menu = self.main_menu.addMenu("设置")
        help_menu = self.main_menu.addMenu("帮助")
        self.CentralWidget()
        self.status_menu()

    # 窗口布局
    def CentralWidget(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.outer_layout = QHBoxLayout(central_widget)

        self.left_widget_layout = QVBoxLayout()
        self.left_widget_layout.setSpacing(15)
        self.leftFrame()
        self.left_widget = QWidget()
        self.left_widget.setLayout(self.left_widget_layout)

        self.right_widget_layout = QVBoxLayout()
        self.rightFrame()
        self.right_widget = QWidget()
        self.right_widget.setLayout(self.right_widget_layout)
        # self.right_widget.setStyleSheet("background-color: yellow;")

        self.outer_layout.addWidget(self.left_widget, 1)
        self.outer_layout.addWidget(self.right_widget, 3)

    def leftFrame(self):
        connect_text = QLabel("连接方式")
        connect_button_layout = QHBoxLayout()
        radio_group = QButtonGroup()
        options = ["网络连接", "串口连接"]
        for option in options:
            radio_button = QRadioButton(option)
            radio_group.addButton(radio_button)
            connect_button_layout.addWidget(radio_button)
        radio_group.setExclusive(True)
        self.left_widget_layout.addWidget(connect_text)
        self.left_widget_layout.addLayout(connect_button_layout)
        self.left_widget_layout.addWidget(QLabel("<hr>"))
        # *************************************************************
        serial_text = QLabel("串口设置")

        serial_list_layout = QHBoxLayout()
        serial_list_layout.addWidget(QLabel("设备选择："))
        serial_combobox = QComboBox()
        serial_combobox.addItems(["COM1", "COM2", "COM3", "COM7"])
        serial_list_layout.addWidget(serial_combobox)

        baudrate_list_layout = QHBoxLayout()
        baudrate_list_layout.addWidget(QLabel("波特率："))
        baudrate_combobox = QComboBox()
        baudrate_combobox.addItems(["9600", "19200", "912600"])
        baudrate_list_layout.addWidget(baudrate_combobox)

        serial_button_layout = QHBoxLayout()
        search_button = QPushButton("搜索")
        # search_button.setStyleSheet("min-width: 30px;max-width: 50px;min-height: 10px;max-height: 20px;")
        connect_button = QPushButton("连接")
        serial_button_layout.addWidget(search_button)
        serial_button_layout.addWidget(connect_button)

        self.left_widget_layout.addWidget(serial_text)
        # self.left_widget_layout.addSpacerItem(QSpacerItem(20, 40))
        self.left_widget_layout.addLayout(serial_list_layout)
        self.left_widget_layout.addLayout(baudrate_list_layout)
        self.left_widget_layout.addLayout(serial_button_layout)
        self.left_widget_layout.addWidget(QLabel("<hr>"))
        # *************************************************************
        network_text = QLabel("网络设置")

        home_address_layout = QHBoxLayout()
        home_address_label = QLabel("主机地址：")
        home_address_lineedit = QLineEdit()
        home_address_lineedit.setPlaceholderText("请输入主机地址")
        home_address_layout.addWidget(home_address_label)
        home_address_layout.addWidget(home_address_lineedit)

        port_layout = QHBoxLayout()
        port_text = QLabel("端口号：")
        port_lineedit = QLineEdit()
        port_lineedit.setPlaceholderText("请输入端口号")
        port_layout.addWidget(port_text)
        port_layout.addWidget(port_lineedit)

        network_start_button = QPushButton("开始连接")
        network_start_button.resize(5, 5)

        self.left_widget_layout.addWidget(network_text)
        # self.left_widget_layout.addSpacerItem(QSpacerItem(20, 40))
        self.left_widget_layout.addLayout(port_layout)
        self.left_widget_layout.addWidget(network_start_button)
        self.left_widget_layout.addWidget(QLabel("<hr>"))
        # *************************************************************
        parameter_setting_text = QLabel("参数设置")

        rise_time_layout = QHBoxLayout()
        rise_time_text = QLabel("上升时间Na：")
        rise_time_edit = QLineEdit()
        rise_time_edit.setPlaceholderText("请输入上升时间")
        rise_time_layout.addWidget(rise_time_text)
        rise_time_layout.addWidget(rise_time_edit)

        flat_top_time_layout = QHBoxLayout()
        flat_top_time_text = QLabel("平顶时间Nb：")
        flat_top_time_edit = QLineEdit()
        flat_top_time_edit.setPlaceholderText("请输入平顶时间")
        flat_top_time_layout.addWidget(flat_top_time_text)
        flat_top_time_layout.addWidget(flat_top_time_edit)

        time_constant_layout = QHBoxLayout()
        time_constant_text = QLabel("时间常数d：")
        time_constant_edit = QLineEdit()
        time_constant_edit.setPlaceholderText("请输入时间常数")
        time_constant_layout.addWidget(time_constant_text)
        time_constant_layout.addWidget(time_constant_edit)

        peak_judge_layout = QHBoxLayout()
        peak_judge_text = QLabel("峰判断阈值：")
        peak_judge_edit = QLineEdit()
        peak_judge_edit.setPlaceholderText("请输入峰判断阈值")
        peak_judge_layout.addWidget(peak_judge_text)
        peak_judge_layout.addWidget(peak_judge_edit)

        peak_average_layout = QHBoxLayout()
        peak_average_text = QLabel("峰均值延迟：")
        peak_average_edit = QLineEdit()
        peak_average_edit.setPlaceholderText("请输入峰均值延迟")
        peak_average_layout.addWidget(peak_average_text)
        peak_average_layout.addWidget(peak_average_edit)

        peak_judge_delay_layout = QHBoxLayout()
        peak_judge_delay_text = QLabel("峰判断延迟：")
        peak_judge_delay_edit = QLineEdit()
        peak_judge_delay_edit.setPlaceholderText("请输入峰判断延迟")
        peak_judge_delay_layout.addWidget(peak_judge_delay_text)
        peak_judge_delay_layout.addWidget(peak_judge_delay_edit)

        pre_lease_layout = QHBoxLayout()
        pre_lease_text = QLabel("前放类型：")
        pre_lease_combobox = QComboBox()
        pre_lease_combobox.addItems(["正脉冲", "负脉冲"])
        pre_lease_layout.addWidget(pre_lease_text)
        pre_lease_layout.addWidget(pre_lease_combobox)

        measure_time_layout = QHBoxLayout()
        measure_time_text = QLabel("测量时间(s)：")
        measure_time_edit = QLineEdit()
        measure_time_edit.setPlaceholderText("请输入测量时间")
        measure_time_layout.addWidget(measure_time_text)
        measure_time_layout.addWidget(measure_time_edit)

        measure_start_button = QPushButton("开始测量")

        self.left_widget_layout.addWidget(parameter_setting_text)
        self.left_widget_layout.addLayout(rise_time_layout)
        self.left_widget_layout.addLayout(flat_top_time_layout)
        self.left_widget_layout.addLayout(time_constant_layout)
        self.left_widget_layout.addLayout(peak_judge_layout)
        self.left_widget_layout.addLayout(peak_average_layout)
        self.left_widget_layout.addLayout(peak_judge_delay_layout)
        self.left_widget_layout.addLayout(pre_lease_layout)
        self.left_widget_layout.addLayout(measure_time_layout)
        self.left_widget_layout.addWidget(measure_start_button)
        # *************************************************************

    def rightFrame(self):
        process = fit.dataProcess("data/fitting3.txt")
        plt_figure = process.process()
        self.figure = plt_figure
        self.canvas = FigureCanvas(self.figure)
        self.right_widget_layout.addWidget(self.canvas)

    # 文件菜单
    def file_menu(self):
        file_menu = self.main_menu.addMenu("文件")
        open_file = QAction("打开", self)
        open_file.triggered.connect(self.open_file_dialog)

        save = QAction("保存",self)
        save.triggered.connect(self.save_dialog)

        exit = QAction("退出", self)
        exit.triggered.connect(self.close_dialog)

        file_menu.addAction(open_file)
        file_menu.addAction(save)
        file_menu.addSeparator()
        file_menu.addAction(exit)

    def status_menu(self):
        self.status = QStatusBar()
        self.status_label = QLabel("****************************************************")

        self.setStatusBar(self.status)
        self.status.addPermanentWidget(self.status_label)
        self.status.setStyleSheet("background-color: white")

    # 文件打开窗口
    def open_file_dialog(self):

        # 弹出文件打开对话框（父窗口、对话框标题、初始路径、文件过滤器）
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            '选择要打开的文件',
            '',  # 初始路径（空表示当前目录）
            '所有文件(*.*);;文本文件(*.txt);;图片文件(*.png *.jpg)'  # 文件过滤器
        )
        if file_path:  # 选择了文件
            print(file_path)
        else:  # 取消了选择
            print("No file selected!")

    # 保存窗口
    def save_dialog(self):
        # 保存right_widget中的能谱图
        pixmap = self.right_widget.grab()

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            '保存至',
            '',
            '所有文件(*.*);;文本文件(*.txt);;图片文件(*.png *.jpg)'
        )
        if file_path:
            if pixmap.save(file_path):
                print(f"图片已保存到：{file_path}")
            else:
                print("保存失败，请检查文件路径或权限")

    # 退出窗口
    def close_dialog(self):
        # 创建消息框
        msg_box = QMessageBox()
        msg_box.setText("你确定要退出吗？")
        msg_box.setWindowTitle("退出")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # 获取选择
        user_input = msg_box.exec()
        if user_input == QMessageBox.Yes:
            self.close()  # 选择是，则关闭窗口（退出程序）

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    # 程序进入循环等待状态
    sys.exit(app.exec_())