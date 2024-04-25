import time
import numpy as np
import PIL.Image as Image
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from utils.watermark import *
from io import BytesIO


class Thread(QThread):
    trigger = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Thread, self).__init__(parent)

    def run_(self, message):
        self.trigger.emit(message)


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
        self.ImgPath = r''  # 文件路径
        self.ImgType = r''  # 文件类型
        self.src = None  # 存储图像信息
        self.bin = np.array([])  # 存储图像二进制信息的np数组
        self.showbin = Thread(self)  # 创建线程以打印图片二进制信息
        self.showbin.trigger.connect(self.update_text)
        self.timer = QTimer()
        self.InitUI()

    def InitUI(self):
        self.ui.OpenImg.clicked.connect(self.OpenImge)
        self.ui.SaveCurrentImg.clicked.connect(self.SaveImg)
        self.ui.CleanCurrentImg.clicked.connect(self.CleanImg)

    def OpenImge(self):
        """
        打开图片并转为numpyarray
        """
        self.CleanImg()
        self.ImgPath, self.ImgType = QFileDialog.getOpenFileName(self.centralwidget, "选择图片",
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
            self.bin = np.array(self.src)
            self.ShowImg()
            print("图像信息：")
            print(f"长：{self.bin.shape[1]}\t宽：{self.bin.shape[0]}\t通道数：{self.bin.shape[2]}")
            self.ShowBinary()

    def ShowImg(self):
        """
        展示图片
        图片小于窗口则居中，否则出现滚动条
        """
        self.ShowImgLabel = QLabel()
        pixmap = ToPixmap(self.bin)
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
            self.src = None  # 存储图像信息
            self.bin = np.array([])  # 存储图像二进制信息的np数组
            self.ui.ShowBinaryBrowser.setText("")
            self.ImgPath = r''

    def ShowBinary(self):
        self.hexdump(self.bin, self.ImgPath)

    # def hexdump(self, nparr, path, bytes_per_line=16):
    #     bin = nparr.tobytes()
    #     tmppath = path
    #     offset = 0
    #     dump = ""
    #     while offset <= len(bin):
    #         # chunk = f.read(bytes_per_line)
    #         chunk = bin[offset: offset + bytes_per_line]
    #         if not chunk or tmppath != self.ImgPath:
    #             break
    #         hex_line = ' '.join(['{:02x}'.format(byte) for byte in chunk])
    #         ascii_line = ''.join([chr(byte) if 32 <= byte <= 126 else '.' for byte in chunk])

    #         # self.ui.ShowBinaryBrowser.append('{:08x}  {:48s}  {}'.format(offset, hex_line, ascii_line))
    #         dump += ('{:08x}  {:48s}  {}'.format(offset, hex_line, ascii_line))+'\n'
    #         offset += bytes_per_line
    #         QApplication.processEvents()
    #     print("dump:", dump)
    #     self.showbin.run_(dump)
    #     # self.ui.ShowBinaryBrowser.setPlainText(dump)


    def hexdump(self, nparr, path, bytes_per_line=16):
        import concurrent.futures
        import threading

        lock = threading.Lock()
        dumpDict = {}
        def process_chunk(chunk, offset, idx):
            hex_line = ' '.join(['{:02x}'.format(byte) for byte in chunk])
            ascii_line = ''.join([chr(byte) if 32 <= byte <= 126 else '.' for byte in chunk])
            # print(hex_line)
            # QApplication.processEvents()
            currentLine = '{:08x}  {:48s}  {}'.format(offset, hex_line, ascii_line)
            lock.acquire()
            dumpDict[idx] = currentLine
            lock.release()
        bin = nparr.tobytes()
        tmppath = path
        offset = 0

        idx = 0

        with concurrent.futures.ThreadPoolExecutor(50) as t:
            while offset <= len(bin):
                chunk = bin[offset: offset + bytes_per_line]
                if not chunk or tmppath != self.ImgPath:
                    break
                
                t.submit(process_chunk, chunk=chunk, offset=offset, idx=idx)
                idx = idx + 1
                offset += bytes_per_line
                QApplication.processEvents()

        # print("dump:", dumpDict)
        self.showbin.run_("\n".join(dumpDict.values()))

    def update_text(self, message):
        self.ui.ShowBinaryBrowser.setPlainText(message)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())
