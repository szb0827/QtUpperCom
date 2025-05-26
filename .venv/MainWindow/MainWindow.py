import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLineEdit, QAction, QMenu,
                             QMainWindow, QFileDialog, QMessageBox, QFrame, QLabel, QRadioButton, QGroupBox, QGridLayout
                             , QComboBox, QButtonGroup )
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor, QPalette

class LeftFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        left_module = QVBoxLayout()

        # 连接方式组
        connect_layout = QVBoxLayout()

        connect_text = QLabel("连接方式")
        connect_layout.addWidget(connect_text)

        connect_button_layout = QHBoxLayout()
        radio_group = QButtonGroup()
        options = ["网络连接","串口连接"]
        for option in options:
            radio_button = QRadioButton(option)
            radio_group.addButton(radio_button)
            connect_button_layout.addWidget(radio_button)
        radio_group.setExclusive(True)
        connect_layout.addWidget(connect_button_layout)

        connection_group.setLayout(connection_layout)

        # 串口设置分组
        serial_group = QGroupBox("串口设置")
        serial_layout = QGridLayout()
        serial_layout.addWidget(QLabel("设备选择："), 0, 0)
        self.serial_combobox = QComboBox()
        self.serial_combobox.addItems(["COM1", "COM2", "COM3", "COM7"])
        serial_layout.addWidget(self.serial_combobox, 0, 1)
        serial_layout.addWidget(QLabel("波特率："), 1, 0)
        self.baudrate_combobox = QComboBox()
        self.baudrate_combobox.addItems(["9600", "19200", "912600"])
        serial_layout.addWidget(self.baudrate_combobox, 1, 1)
        serial_group.setLayout(serial_layout)

        # 网络设置分组
        network_group = QGroupBox("网络设置")
        network_layout = QGridLayout()
        network_layout.addWidget(QLabel("TCP Client"), 0, 0, 1, 2)
        network_layout.addWidget(QLabel("主机地址："), 1, 0)
        self.host_edit = QLineEdit("192.168.1.10")
        network_layout.addWidget(self.host_edit, 1, 1)
        network_layout.addWidget(QLabel("端口号："), 2, 0)
        self.port_edit = QLineEdit("7")
        network_layout.addWidget(self.port_edit, 2, 1)
        network_group.setLayout(network_layout)

        # 参数设置分组
        param_group = QGroupBox("参数设置")
        param_layout = QGridLayout()
        param_layout.addWidget(QLabel("上升时间(Ns)："), 0, 0)
        self.rise_edit = QLineEdit("20")
        param_layout.addWidget(self.rise_edit, 0, 1)
        param_layout.addWidget(QLabel("平波时间(Ns)："), 1, 0)
        self.flat_edit = QLineEdit("100")
        param_layout.addWidget(self.flat_edit, 1, 1)
        param_layout.addWidget(QLabel("时间间隔(us)："), 2, 0)
        self.interval_edit = QLineEdit("200")
        param_layout.addWidget(self.interval_edit, 2, 1)
        param_layout.addWidget(QLabel("蜂鸣器阈值："), 3, 0)
        self.buzzer_edit = QLineEdit("500")
        param_layout.addWidget(self.buzzer_edit, 3, 1)
        param_layout.addWidget(QLabel("蜂鸣器延迟："), 4, 0)
        self.delay_edit = QLineEdit("20")
        param_layout.addWidget(self.delay_edit, 4, 1)
        param_layout.addWidget(QLabel("蜂鸣器频次："), 5, 0)
        self.freq_edit = QLineEdit("6")
        param_layout.addWidget(self.freq_edit, 5, 1)
        param_layout.addWidget(QLabel("前段类型："), 6, 0)
        self.type_combobox = QComboBox()
        self.type_combobox.addItems(["正脉冲", "负脉冲"])
        param_layout.addWidget(self.type_combobox, 6, 1)
        param_layout.addWidget(QLabel("质量测量时间："), 7, 0)
        self.time_edit = QLineEdit("1800")
        param_layout.addWidget(self.time_edit, 7, 1)
        param_group.setLayout(param_layout)

        # 添加到主布局
        left_module.addWidget(connection_group)
        left_module.addWidget(serial_group)
        left_module.addWidget(network_group)
        left_module.addWidget(param_group)

        self.setLayout(left_module)
        self.setStyleSheet("QGroupBox { font-size: 14px; margin-top: 8px; }")

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
        self.FileMenu()
        spec_peak = self.main_menu.addMenu("谱寻峰")
        setting_menu = self.main_menu.addMenu("设置")
        help_menu = self.main_menu.addMenu("帮助")
        self.CentralWidget()


    def CentralWidget(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.outer_layout = QGridLayout(central_widget)

        # 连接方式组
        connect_layout = QVBoxLayout()
        connect_text = QLabel("连接方式")
        connect_layout.addWidget(connect_text)

        connect_button_layout = QHBoxLayout()
        radio_group = QButtonGroup()
        options = ["网络连接", "串口连接"]
        for option in options:
            radio_button = QRadioButton(option)
            radio_group.addButton(radio_button)
            connect_button_layout.addWidget(radio_button)
        radio_group.setExclusive(True)
        connect_layout.addLayout(connect_button_layout)

        connect_widget = QWidget()
        connect_widget.setLayout(connect_layout)
        connect_widget.setStyleSheet("background-color: rgb(100, 100, 240);")
        self.outer_layout.addWidget(connect_widget,1,1,1,1);

        right_widget = QWidget()

        right_widget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.outer_layout.addWidget(right_widget, 1, 2, 5, 3);
        print("")

    # 文件菜单
    def FileMenu(self):
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

    # 文件打开窗口
    def open_file_dialog(self):
        # 弹出文件打开对话框（父窗口、对话框标题、初始路径、文件过滤器）
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            '选择要打开的文件',
            '',  # 初始路径（空表示当前目录）
            '所有文件(*.*);;文本文件(*.txt);;图片文件(*.png *.jpg)'  # 文件过滤器
        )
        if fileName:  # 选择了文件
            # self.status_label.setText(f'已选择文件: {fileName}')
            print(fileName)
        else:  # 取消了选择
            # self.status_label.setText('用户取消了文件选择')
            print("No file selected!")

    # 保存窗口
    def save_dialog(self):
        fileName, _ = QFileDialog.getSaveFileName(
            self,
            '保存至',
            '',
            '所有文件(*.*);;文本文件(*.txt);;图片文件(*.png *.jpg)'
        )
        if fileName:
            print(fileName)
        else:
            print("No file saved!")

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