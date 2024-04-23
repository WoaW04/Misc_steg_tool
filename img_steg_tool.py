import numpy as np
import PIL.Image as Image
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import *
import sys
from utils.watermark import *


def ToPixmap(arr):
    """
    将numpyarr转换为pixmap，用于显示
    """
    # 从numpy转为Image
    tmp = Image.fromarray(arr).convert('RGB')
    # 从Image转为QImage
    tmp = QImage(tmp.tobytes(), tmp.width, tmp.height, QImage.Format_RGB888)
    # 返回将QImage转QPixmap
    return QPixmap.fromImage(tmp)


class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.mainLayout = None
        self.ui = uic.loadUi("mainwindow.ui", self)  # 加载UI
        self.ImgPath = ''  # 文件路径
        self.ImgType = ''  # 文件类型
        self.ImgSrc = np.array([])  # 存储图像二进制信息数组
        self.InitUI()

    def InitUI(self):
        self.ui.OpenImg.clicked.connect(self.OpenImge)
        self.ui.SaveCurrentImg.clicked.connect(self.SaveImg)
        self.ui.CleanCurrentImg.clicked.connect(self.CleanImg)

    def OpenImge(self):
        """
        打开图片并转为numpyarray
        """
        self.ImgPath, self.ImgType = QFileDialog.getOpenFileName(self.centralwidget, "选择图片",
                                                                 "./", "Image files (*.jpg *.gif *.png *.jpeg)")
        if self.ImgPath == '':
            warning = QMessageBox()  # 创建QMessageBox()对象
            warning.setIcon(QMessageBox.Warning)  # 设置弹窗的QMessageBox.Icon类型
            warning.setWindowTitle('警告')  # 设置弹窗标题
            warning.setText("未指定文件")  # 设置弹窗提示信息
            quit = warning.addButton('关闭', QMessageBox.RejectRole)
            warning.setDefaultButton(quit)    # 设置默认按钮
            warning.exec_()  # 指定退出键；返回选中按钮的值
        else:
            self.CleanImg()
            self.src = np.array(Image.open(self.ImgPath))
            self.ShowImg()
            print("图像信息：")
            print(f"长：{self.src.shape[1]}\t宽：{self.src.shape[0]}\t通道数：{self.src.shape[2]}")

    def ShowImg(self):
        """
        展示图片
        图片小于窗口则居中，否则出现滚动条
        """
        self.ShowImgLabel = QLabel()
        pixmap = ToPixmap(self.src)
        imgsize = pixmap.size()
        self.ShowImgLabel.setPixmap(pixmap)
        self.ShowImgLabel.resize(imgsize)
        self.scroll = QScrollArea()
        self.scroll.setAlignment(Qt.AlignCenter)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setWidget(self.ui.ShowImgLabel)
        if self.mainLayout == None:
            self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.scroll, 0, 0)
        self.ui.ShowImgWidget.setLayout(self.mainLayout)

    def SaveImg(self):
        """
        保存图片
        """
        if self.src.shape == (0,):
            warning = QMessageBox()  # 创建QMessageBox()对象
            warning.setIcon(QMessageBox.Warning)  # 设置弹窗的QMessageBox.Icon类型
            warning.setWindowTitle('警告')  # 设置弹窗标题
            warning.setText("未打开文件")  # 设置弹窗提示信息
            quit = warning.addButton('关闭', QMessageBox.RejectRole)
            warning.setDefaultButton(quit)    # 设置默认按钮
            warning.exec_()  # 指定退出键；返回选中按钮的值
        else:
            filepath, _ = QFileDialog.getSaveFileName(self, "文件保存", f"{self.ImgPath}", 'Image files (*.jpg *.gif *.png *.jpeg)')
            if filepath == '':
                pass
            else:
                img = Image.fromarray(self.src)
                img.save(filepath)

    def CleanImg(self):
        """
        清除当前展示的图片
        """
        if self.ui.ShowImgWidget.layout() is not None:
            self.ShowImgLabel.clear()
            self.ShowImgLabel.resize(QSize(200, 100))
            self.mainLayout.removeWidget(self.scroll)
            self.src = np.array([])


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())
