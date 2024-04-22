import numpy as np
import PIL.Image as Image
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import *
import cv2
import sys
from utils.watermark import *


def ToPixmap(arr):
    # 从numpy转为Image
    tmp = Image.fromarray(arr).convert('RGB')
    # 从Image转为QImage
    tmp = QImage(tmp.tobytes(), tmp.width, tmp.height, QImage.Format_RGB888)
    # 返回将QImage转QPixmap
    return QPixmap.fromImage(tmp)


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
        self.ShowImg()
        print("图像信息：")
        print(f"长：{self.src.shape[1]}\t宽：{self.src.shape[0]}\t通道数：{self.src.shape[2]}")

    def ShowImg(self):
        self.ShowImgLabel = QLabel()
        self.ShowImgLabel.setPixmap(ToPixmap(self.src))
        self.scroll = QScrollArea()
        self.scroll.setAlignment(Qt.AlignCenter)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setWidget(self.ui.ShowImgLabel)
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.scroll, 0, 0)
        self.ui.ShowImgWidget.setLayout(self.mainLayout)

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
