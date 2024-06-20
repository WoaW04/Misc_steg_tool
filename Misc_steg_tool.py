import numpy as np
import PIL.Image as Image
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec
import os
import PIL.ImageOps
from PIL import Image

def getCurrentPath():
    if hasattr(sys, 'frozen'):  # 可执行文件走这里
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)  # 源码走这里


def ToPixmap(img):
    """
    将PIL图像转换为pixmap，用于显示
    """
    if img.mode == "RGBA":
        tmp = QImage(img.tobytes(), img.width, img.height, QImage.Format_RGBA8888)
    elif img.mode == "RGB":
        tmp = QImage(img.tobytes(), img.width, img.height, QImage.Format_RGB888)
    elif img.mode == "L":
        tmp = QImage(img.tobytes(), img.width, img.height, QImage.Format_Alpha8)
    # tmp = ImageQt.toqimage(img)
    # 返回将QImage转QPixmap
    return QPixmap.fromImage(tmp)


class Ui(QtWidgets.QMainWindow):
    PLUGIN_PATH = getCurrentPath() + "/" + "plugins"

    def __init__(self):
        super().__init__()
        self.mainLayout = None
        self.ui = uic.loadUi("mainwindow.ui", self)  # 加载UI
        self.ImgPath = r''  # 文件路径
        self.src = None  # 存储图像信息（PIL），用于进行转换
        self.pixmap = None #存储图像信息（Pixmap），用于展示和保存
        self.importPlugins = {}  # 保存所有已加載的插件名
        self.signals = {} # 保存插件的signal
        self.SwitchTable = ["Origin",
                            "Rev",
                            "GrayBit",
                            "FullRed",
                            "FullGreen",
                            "FullBlue",
                            "FullAlpha",
                            "RedPlane0",
                            "GreenPlane0",
                            "BluePlane0"
                            ]
        self.SwitchTableIndex = 0
        # 正常、反色、灰度、FullR、FullB、FullG、FullA、R0，G0，B0
        
        self.InitUI()
        self.initPlugin()


    def InitUI(self):
        self.ui.OpenImg.clicked.connect(self.OpenImage)
        self.ui.SaveCurrentImg.clicked.connect(self.SaveImg)
        self.ui.CleanCurrentImg.clicked.connect(self.CleanImg)
        self.ui.PlaneSwitchL.clicked.connect(self.SwitchPlaneL)
        self.ui.PlaneSwitchR.clicked.connect(self.SwitchPlaneR)
        self.ui.PlaneSwitchL.setEnabled(False)
        self.ui.PlaneSwitchR.setEnabled(False)


    def initPlugin(self):
        pluginsDirName = self.PLUGIN_PATH.split("/")[-1]
        fileNames = os.listdir(self.PLUGIN_PATH)
        # 将plugins目录添加到sys.path, 防止在插件中出现ImportError
        pluginsPath = os.path.join(getCurrentPath(), "plugins")
        sys.path.append(pluginsPath)

        for fileName in fileNames:
            if fileName.endswith(".py"):
                self.loadPlugin(f"{pluginsDirName}.{fileName.split('.')[0]}")


    def loadPlugin(self, pluginName):

        self.importPlugins[pluginName] = True
        try:
            # py动态加载模块
            module = import_module(pluginName)
            # 获取模块加载的ui
            moduleUI = module.Ui()

            # 保存插件的signalsignal, 用于两者之间的信息传递
            self.signals[pluginName] = moduleUI.signal

            print(f"loading plugin: {pluginName}")
            # 添加到Tab中
            self.ui.Tab.addTab(moduleUI, moduleUI.NAME)
        except:
            print(f"load plugin: {pluginName} failed :(")


    def OpenImage(self):
        """
        打开图片并转为PIL格式
        """
        self.CleanImg()
        self.ImgPath, _ = QFileDialog.getOpenFileName(self.centralwidget, "选择图片",
                                                                 "./", "Image files (*.jpg *.gif *.png *.jpeg)")

        if self.ImgPath == r'':
            warning = QMessageBox()  # 创建QMessageBox()对象
            warning.setIcon(QMessageBox.Warning)  # 设置弹窗的QMessageBox.Icon类型
            warning.setWindowTitle('警告')  # 设置弹窗标题
            warning.setText("未指定文件")  # 设置弹窗提示信息
            quit = warning.addButton('关闭', QMessageBox.RejectRole)
            warning.setDefaultButton(quit)    # 设置默认按钮
            warning.exec_()  # 指定退出键；返回选中按钮的值
        else:
            self.src = Image.open(self.ImgPath, 'r')
            self.ShowImg("原图",self.src)
            self.ui.PlaneSwitchL.setEnabled(True)
            self.ui.PlaneSwitchR.setEnabled(True)

    def ShowImg(self,text,src):
        """
        展示图片
        图片小于窗口则居中，否则出现滚动条
        """
        self.ShowImgLabel = QLabel()
        self.pixmap = ToPixmap(src)
        imgsize = self.pixmap.size()
        self.ShowImgLabel.setPixmap(self.pixmap)
        self.ShowImgLabel.resize(imgsize)
        self.scroll = QScrollArea()
        self.scroll.setAlignment(Qt.AlignCenter)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setWidget(self.ui.ShowImgLabel)
        if self.mainLayout == None:
            self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.scroll, 0, 0)
        self.ui.ShowImgWidget.setLayout(self.mainLayout)
        self.ui.CurrentPlane.setText(text)
        

    def SaveImg(self):
        """
        保存图片
        """
        if self.ImgPath == r'':
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
                self.pixmap.save(filepath)

    def CleanImg(self):
        """
        清除当前展示的图片
        """
        if self.ui.ShowImgWidget.layout() is not None:
            self.ShowImgLabel.clear()
            self.ShowImgLabel.resize(QSize(200, 100))
            self.mainLayout.removeWidget(self.scroll)
            self.src = None  # 存储图像信息
            self.pixmap = None
            self.ImgPath = r''
            self.ui.PlaneSwitchL.setEnabled(False)
            self.ui.PlaneSwitchR.setEnabled(False)
            self.ui.CurrentPlane.setText("")
            
    def SwitchPlane(self,flag):
        """
        切换显示的位
        """
        self.SwitchTableIndex=(self.SwitchTableIndex + flag)%10
        CurrentPlane = self.SwitchTable[self.SwitchTableIndex]
        # self.SwitchTable = ["Origin",
        #                     "Rev",
        #                     "GrayBit",
        #                     "FullRed",
        #                     "FullGreen",
        #                     "FullBlue",
        #                     "FullAlpha",
        #                     "RedPlane0",
        #                     "GreenPlane0",
        #                     "BluePlane0"
        #                     ]
        if CurrentPlane == "Origin":
            self.ShowImg("原图",self.src)
        elif CurrentPlane == "Rev":
            rev = self.src.convert("RGB")
            rev = PIL.ImageOps.invert(rev)
            self.ShowImg("反色",rev)
        elif CurrentPlane == "GrayBit":
            # r==g==b则保留，否则设为白色
            gb = self.src.convert("RGB")
            width, height = gb.size
            for x in range(width):
                for y in range(height):
                    # 获取像素的RGB值
                    r, g, b = gb.getpixel((x, y))
                    if r == g == b:
                        continue
                    else:
                        gb.putpixel((x, y), (0, 0, 0))  
            self.ShowImg("GrayBits",gb)
        elif CurrentPlane == "FullRed":
            fr = self.src.convert("RGB")
            width, height = fr.size
            for x in range(width):
                for y in range(height):
                    # 获取像素的RGB值
                    r, g, b = fr.getpixel((x, y))
                    fr.putpixel((x, y), (r, 0, 0))#仅保留红色通道
            self.ShowImg("FullRed",fr)
        elif CurrentPlane == "FullGreen":
            fg = self.src.convert("RGB")
            width, height = fg.size
            for x in range(width):
                for y in range(height):
                    # 获取像素的RGB值
                    r, g, b = fg.getpixel((x, y))
                    fg.putpixel((x, y), (0, g, 0))
            self.ShowImg("FullGreen",fg)
        elif CurrentPlane == "FullBlue":
            fb = self.src.convert("RGB")
            width, height = fb.size
            for x in range(width):
                for y in range(height):
                    # 获取像素的RGB值
                    r, g, b = fb.getpixel((x, y))
                    fb.putpixel((x, y), (0, 0, b))
            self.ShowImg("FullBlue",fb)
        elif CurrentPlane == "FullAlpha":
            fa = self.src.convert("RGBA")
            fa = fa.getchannel('A')
            self.ShowImg("FullAlpha",fa)
        elif CurrentPlane == "RedPlane0":
            rp0 = self.src.convert("RGB")
            width, height = rp0.size
            for x in range(width):
                for y in range(height):
                    # 获取像素的RGB值
                    r, g, b = rp0.getpixel((x, y))
                    if r %2 == 1:
                        #如果红色通道最低有效位为1则该像素置黑。否则置白
                        rp0.putpixel((x, y), (255, 255, 255))
                    else:
                        rp0.putpixel((x, y), (0, 0, 0))
            self.ShowImg("RedPlane0",rp0)
        elif CurrentPlane == "GreenPlane0":
            gp0 = self.src.convert("RGB")
            width, height = gp0.size
            for x in range(width):
                for y in range(height):
                    # 获取像素的RGB值
                    r, g, b = gp0.getpixel((x, y))
                    if g %2 == 1:
                        gp0.putpixel((x, y), (255, 255, 255))
                    else:
                        gp0.putpixel((x, y), (0, 0, 0))
            self.ShowImg("GreenPlane0",gp0)
        elif CurrentPlane == "BluePlane0":
            bp0 = self.src.convert("RGB")
            width, height = bp0.size
            for x in range(width):
                for y in range(height):
                    # 获取像素的RGB值
                    r, g, b = bp0.getpixel((x, y))
                    if b %2 == 1:
                        bp0.putpixel((x, y), (255, 255, 255))
                    else:
                        bp0.putpixel((x, y), (0, 0, 0))
            self.ShowImg("BluePlane0",bp0)
    
    def SwitchPlaneL(self):
        """
        获取上一种变换
        """
        self.SwitchPlane(-1)
    
    def SwitchPlaneR(self):
        """
        获取下一种变换
        """
        self.SwitchPlane(1)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())
