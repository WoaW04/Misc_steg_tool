import numpy as np
import PIL.Image as Image
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
import cv2
import sys
from utils.watermark import *


def ToPixmap_1(arr):  # arr对应四通道图片。额外使用PIL.Image模块
    # https://blog.csdn.net/ielcome2016/article/details/105798279
    from PIL import Image
    arr = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGRA)
    return Image.fromarray(arr).toqpixmap()


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("mainwindow.ui", self)
        self.ImgPath = ''
        self.src = np.array(0)
        self.InitUI()

    def InitUI(self):
        self.ui.OpenImg.clicked.connect(self.openimg)
        self.ui.SaveCurrentImg.clicked.connect(self.saveimg)

    def openimg(self):
        self.ImgPath, _ = QFileDialog.getOpenFileName(self.centralwidget, "选择图片",
                                                      "./", "Image files (*.jpg *.gif *.png *.jpeg)")
        self.ReadImg(self.ImgPath)

    def ReadImg(self, path):
        self.src = np.array(Image.open(path))
        self.ui.ShowImgLabel.setPixmap(ToPixmap_1(self.src))

        print("图像信息：")
        print(f"长：{self.src.shape[1]}\t宽：{self.src.shape[0]}\t通道数：{self.src.shape[2]}")

    def saveimg(self):
        Img = self.src
        filepath, _ = QFileDialog.getSaveFileName(self, "文件保存", "/", 'Image files (*.jpg *.gif *.png *.jpeg)')
        file = open(filepath, 'w')
        print(filepath)
        file.write(Img)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())
