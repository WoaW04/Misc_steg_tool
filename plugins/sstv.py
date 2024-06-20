import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PIL import Image

from pathvalidate import *
from sstv_module import sstv_decode
# from sstv_decode import SSTVDecoder
from sstv_module import sstv_encode

import sys
def getCurrentPath():
    if hasattr(sys, 'frozen'):  # 可执行文件走这里
        return os.path.dirname(sys.executable) + "/plugins/"
    return os.path.dirname(__file__)  # 源码走这里

SSTV_MODULES = [sstv_encode]
def build_module_map():
            try:
                from collections import OrderedDict
                module_map = OrderedDict()
            except ImportError:
                module_map = {}
            for module in SSTV_MODULES:
                for mode in module.MODES:
                    module_map[mode.__name__] = mode
            return module_map

class Ui(QtWidgets.QMainWindow):
    # 显示在主程序Tab中的标题
    NAME = "SSTV隐写模块"
    UI_PATH = os.path.join(getCurrentPath(), "sstv.ui")
    signal = None

    def __init__(self):
        super().__init__()
        self.module_map = build_module_map()
        self.mainLayout = None
        self.ui = uic.loadUi(self.UI_PATH, self)
        self.initUi()

    def initUi(self):
        self.ui.SelectPic.clicked.connect(self.onSelectPicClick)
        self.ui.PTSBtn.clicked.connect(self.onPTSBtnClick)
        self.ui.SelectWav.clicked.connect(self.onSelectWavClick)
        self.ui.STPBtn.clicked.connect(self.onSTPBtnClick)
        regExp = QRegExp('^(320|3[0-1][0-9]|[0-1]?[0-9]?[0-9])$')
        uCharValidator = QRegExpValidator(regExp)
        self.ui.PTSWidthLine.setValidator(uCharValidator)
        self.ui.PTSHeightLine.setValidator(uCharValidator)
        self.ui.STPWidthLine.setValidator(uCharValidator)
        self.ui.STPHeightLine.setValidator(uCharValidator)

    
    def onSelectPicClick(self):
        ImgPath, _ = QFileDialog.getOpenFileName(self.centralwidget, "选择图片",
                                                                 "./", "Image files (*.jpg *.gif *.png *.jpeg)")
        self.ui.PTSFilePath.setText(ImgPath)
    
    def onSelectWavClick(self):
        WavPath, _ = QFileDialog.getOpenFileName(self.centralwidget, "选择音频",
                                                                 "./", "Image files (*.wav)")
        self.ui.STPFilePath.setText(WavPath)
    
    def onPTSBtnClick(self):
        """
        将图片转换为SSTV
        """
        self.ui.STPBtn.setEnabled(False)
        self.ui.PTSBtn.setEnabled(False)
        ImgPath = self.ui.PTSFilePath.text()
        selected = self.ui.buttonGroup.checkedButton().text()
        if is_valid_filepath(ImgPath,platform="Windows"):
            mode = self.module_map[f"{selected}"]
            height = self.PTSHeightLine.text()
            width = self.PTSWidthLine.text()
            steganographier = SSTVThread(self, "encode",ImgPath, mode, height, width, self.ui.PTSBtn,self.ui.STPBtn)
            steganographier.updateUISignal.connect(self.onStegUpdate)
            steganographier.start()
        
    def onSTPBtnClick(self):
        """
        从SSTV中提取图片
        """
        self.ui.STPBtn.setEnabled(False)
        self.ui.PTSBtn.setEnabled(False)
        WavPath = self.ui.STPFilePath.text()
        if is_valid_filepath(WavPath,platform="Windows"):
            height = self.STPHeightLine.text()
            width = self.STPWidthLine.text()
            steganographier = SSTVThread(self, "decode", WavPath, height, width,self.ui.STPBtn,self.ui.PTSBtn)
            steganographier.updateUISignal.connect(self.onStegUpdate)
            steganographier.start()
    
    def onStegUpdate(self, data):
        '''
        處理SSTVThread傳來的更新UI/處理完成信號

        Args: 
            data(dict): 該字典有以下屬性
                - type(str): "UI_UPDATE" | "DONE"
                - objectName(str): 定位ui控件的objectName
                - text(str): 要設置的text值
        '''
        if data["type"] == "PROGRESSING":
            getattr(self.ui, data["objectName"]).setText(data["text"])
        if data["type"] == "DONE":
            getattr(self.ui, data["objectName"]).setText(data["text"])
            info = QMessageBox()  # 创建QMessageBox()对象
            info.setIcon(QMessageBox.Information)  # 设置弹窗的QMessageBox.Icon类型
            info.setWindowTitle('提示')  # 设置弹窗标题
            info.setText("操作成功")  # 设置弹窗提示信息
            quit = info.addButton('关闭', QMessageBox.RejectRole)
            info.setDefaultButton(quit)    # 设置默认按钮
            info.exec_()  # 指定退出键；返回选中按钮的值
        elif data["type"] == "ERROR":
            getattr(self.ui, data["objectName"]).setText(data["text"])
            warning = QMessageBox()  # 创建QMessageBox()对象
            warning.setIcon(QMessageBox.Waring)  # 设置弹窗的QMessageBox.Icon类型
            warning.setWindowTitle('警告')  # 设置弹窗标题
            warning.setText("转换出错")  # 设置弹窗提示信息
            quit = warning.addButton('关闭', QMessageBox.RejectRole)
            warning.setDefaultButton(quit)    # 设置默认按钮
            warning.exec_()  # 指定退出键；返回选中按钮的值


class SSTVThread(QThread):
    updateUISignal = pyqtSignal(dict)

    def __init__(self, parent, func, *args):
        super(SSTVThread, self).__init__(parent)

        self.func = func
        self.args = args

    def run(self):
        if self.func == "encode":
            self.SSTVEncode(*self.args)
        elif self.func == "decode":
            self.SSTVDecode(*self.args)
    
    def setProgressState(self, state):
        if state == "encode":
            types = "PROGRESSING"
            stateText = "正在执行图片转SSTV的操作......"
        elif state == "decode":
            types = "PROGRESSING"
            stateText = "正在执行SSTV转图片的操作......"
        elif state == "idle":
            types = "DONE"
            stateText = "等待操作......"
        elif state == "error":
            types = "ERROR"
            stateText = "转换出错（"
            
        self.updateUISignal.emit({
            "type": types,
            "objectName": "progressState",
            "text": stateText
        })
    
    def SSTVDecode(self,WavPath, height, width,Btn1,Btn2):
        self.setProgressState("decode")
        f = open(WavPath,'rb')
        with sstv_decode.SSTVDecoder(f) as sstv:
            # 可以指定大小
            if height != "" and width !="":
                img = sstv.decode(width=int(width),height=int(height))
            else:
                img = sstv.decode()
            if img is None:  # No SSTV signal found
                self.setProgressState("error")
            else:
                img.save("result.png")
                self.setProgressState("idle")
            Btn1.setEnabled(True)
            Btn2.setEnabled(True)
                


    def SSTVEncode(self,ImgPath,mode,height,width,Btn1,Btn2):
        self.setProgressState("encode")
        image = Image.open(ImgPath) 
        if height != "" and width !="":
                # 可以指定大小
                mode.HEIGHT = int(height)
                mode.WIDTH = int(width)
        # 进行缩放操作
        resample = getattr(Image, "BICUBIC")
        orig_ratio = image.width / image.height
        mode_ratio = mode.WIDTH / mode.HEIGHT
        # crop = orig_ratio != mode_ratio
        t = orig_ratio > mode_ratio
        if t:
            w = mode.WIDTH
            h = int(w / orig_ratio)
        else:
            h = mode.HEIGHT
            w = int(orig_ratio * h)
        image = image.resize((w, h), resample)
        newbg = Image.new('RGB', (mode.WIDTH, mode.HEIGHT))
        if t:
            newbg.paste(image, (0, int((mode.HEIGHT/2)-(h/2))))
        else:
            newbg.paste(image, (int((mode.WIDTH/2)-(w/2)), 0))
        image = newbg.copy()
        # 开始转换
        s = mode(image, 48000, 16)
        s.vox_enabled = False
        try:
            s.write_wav("output.wav")
            self.setProgressState("idle")
        except:
            self.setProgressState("error")
        Btn1.setEnabled(True)
        Btn2.setEnabled(True)
        
        
# if __name__ == '__main__':

#     app = QtWidgets.QApplication(sys.argv)
#     window = Ui()
#     window.show()
#     sys.exit(app.exec_())