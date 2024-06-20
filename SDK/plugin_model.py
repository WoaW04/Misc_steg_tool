import os
from PyQt5 import QtWidgets, uic

import sys
def getCurrentPath():
    if hasattr(sys, 'frozen'):  # 可执行文件走这里
        return os.path.dirname(sys.executable) + "/plugins/"
    return os.path.dirname(__file__)  # 源码走这里

class Ui(QtWidgets.QMainWindow):
    # 显示在主程序Tab中的标题
    NAME = "PLUGIN_NAME"
    # plugin的UI路径
    UI_PATH = os.path.join(getCurrentPath(), "PLUGIN_UI_PATH")
    signal = None

    def __init__(self):
        super().__init__()
        self.mainLayout = None
        self.ui = uic.loadUi(self.UI_PATH, self)
        self.initUi()