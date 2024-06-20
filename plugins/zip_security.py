import os
from struct import unpack
from cryptography.fernet import Fernet
import PIL.Image as Image
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Eocd:
    def __init__(self):
        self.elDirectoryOffset = 0
        # self.elDirectorySize = 0


class ZipSteganography:
    '''Zip隱寫'''

    def __init__(self) -> None:
        pass

    def getEocdPosition(self, file):
        '''返回file(zip文件名)裡的eocd索引'''
        with open(file, mode = "rb") as f:
            data = bytearray(f.read())
            return data.find(b'\x50\x4b\x05\x06') # eocd區域起始特徵 '\x50\x4b\x05\x06'


    def eocdParse(self, file, pos):
        '''
        解析eocd裡指定的屬性

        Args:
            file(str): zip文件路徑

        Returns:
            解析好的Eocd對象
        '''
        with open(file, mode = 'rb') as f:
            # f.seek(pos + 12)
            f.seek(pos + 16)
            eocd = Eocd()
            # eocd.elDirectorySize = unpack('<I', f.read(4))[0]
            eocd.elDirectoryOffset = unpack('<I', f.read(4))[0]
            return eocd


    def checkInjectDataSize(self, injectFile):
        '''檢查注入的數據大小, 上限是2^32-1'''
        maxSize = (2**32) - 1
        injectSize = os.path.getsize(injectFile)
        return (injectSize + 4) - maxSize # 4是用來保存注入數據的大小


    def inject(self, origZipPath, injectFilePath, outputDir):
        '''
        檢查注入的數據大小, 上限是2^32-1

        Args:
            origZipPath(str): 原zip文件路徑
            injectFilePath(str): 目標文件路徑
            outputDir(str): 輸出目錄
        '''
        outputFilePath = outputDir + '/' + origZipPath.split('/')[-1].split('.')[0] + "_zipsteg.zip"

        # 獲取 zip文件的 End of central directory record (eocd)
        eocdPos = self.getEocdPosition(origZipPath)
        eocd = self.eocdParse(origZipPath, eocdPos)


        if self.checkInjectDataSize(injectFilePath) > 0:
            raise Exception(f"`{injectFilePath}` is too big")

        with open(outputFilePath, mode="wb") as f:
            origZipFile = open(origZipPath, mode = 'rb')
            injectFile = open(injectFilePath, mode = "rb")
            
            injectSize = os.path.getsize(injectFilePath)


            # 原zip的"壓縮源文件數據區"
            recordData = origZipFile.read(eocd.elDirectoryOffset)
            # 要注入的數據
            injectData = injectFile.read()

            # 原zip剩餘部分 ( cdh + eocd )
            lastOrigData = bytearray(origZipFile.read())
            eocdIndex = lastOrigData.find(b'\x50\x4b\x05\x06')
            newSize = injectSize + eocd.elDirectoryOffset + 4 # 頭4字節用來保存注入數據的大小

            lastOrigData[eocdIndex + 16 : eocdIndex + 16 + 4] = newSize.to_bytes(4, "little")

            f.write(recordData)
            f.write(injectData)
            f.write(injectSize.to_bytes(4, 'little')) # 保存injectSize, 方便提取注入後的數據
            f.write(lastOrigData)


            origZipFile.close()
            injectFile.close()


    def extract(self, filePath, outputDir):
        '''
        提取隱藏數據

        Args:
            filePath(str): 待提取的文件路徑
            outputDir(str): 輸出目錄
        '''
        outputFilePath = outputDir + '/' + filePath.split('/')[-1].split('.')[0] + "_extract"

        eocdPos = self.getEocdPosition(filePath)
        eocd = self.eocdParse(filePath, eocdPos)


        with open(filePath, mode="rb") as f:
            # 先移到eocd.elDirectoryOffset - 4的地方, 獲取injectSize
            f.seek(eocd.elDirectoryOffset - 4)
            size = unpack('I', f.read(4))[0]

            # 移到injectData起始位置, -4是因為size不包含保存大小的那4個字節
            f.seek(eocd.elDirectoryOffset - size - 4)

            # 提取injectData
            fileData = bytearray(f.read(size))
            print("file size: ", size)
        
        with open(outputFilePath, mode = "wb") as f:
            f.write(fileData)


class ZipFake:
    """
    偽加密原理: 
    當zip的dirEntry後面的全局方式位標記為奇數時, zip文件打開會要求輸入密碼, 以此實現偽加密
    """
    @staticmethod
    def modify(zipPath, outputPath, modifyByte:bytes):
        zipName = zipPath.split("/")[-1].split(".")[0]
        with open(zipPath, mode = 'rb') as f:
            data = f.read()
            data = bytearray(data)

            current = 0
            # dirEntry 可能不至一個 (zip內是folder的情況), 因此要循環遍歷, 直到dirEntryIndex == -1
            while True:
                dirEntryIndex = data.find(b'\x50\x4B\x01\x02', current)
                if dirEntryIndex == -1:
                    break

                data[dirEntryIndex + 8 : dirEntryIndex + 9] = modifyByte
                current = dirEntryIndex + 1

        if modifyByte == b'\x05':
            output = f"{outputPath}/{zipName}_enc.zip"
        else:
            output = f"{outputPath}/{zipName}_dec.zip"


        with open(output, mode = 'wb') as f:
            f.write(data)
    
    @staticmethod
    def encrypt(zipPath, outputPath):
        ZipFake.modify(zipPath, outputPath, b'\x05')
    @staticmethod
    def decrypt(zipPath, outputPath):
        ZipFake.modify(zipPath, outputPath, b'\x00')


import sys
def getCurrentPath():
    if hasattr(sys, 'frozen'):  # 可执行文件走这里
        return os.path.dirname(sys.executable) + "/plugins/"
    return os.path.dirname(__file__)  # 源码走这里

class Ui(QtWidgets.QMainWindow):
    # 顯示在主程序Tab中的標題
    NAME = "Zip模塊"
    UI_PATH = os.path.join(getCurrentPath(), "ZipWindow.ui")
    signal = None

    def __init__(self):
        super().__init__()
        self.mainLayout = None
        self.ui = uic.loadUi(self.UI_PATH, self)

        self.initUi()

    def initUi(self):
        self.ui.zipPseSelBtn.clicked.connect(self.onZipPseSelBtnClick)
        self.ui.zipPseSelOutputBtn.clicked.connect(self.onZipPseSelOutputBtn)
        self.ui.pseEncBtn.clicked.connect(self.onPseEncBtnClick)
        self.ui.pseDecBtn.clicked.connect(self.onPseDecBtnClick)
        self.ui.zipStegPathSelBtn.clicked.connect(self.onZipStegPathSelBtnClick)
        self.ui.zipStegInjectPathSelBtn.clicked.connect(self.onZipStegInjectPathSelBtnClick)
        self.ui.zipStegOutputPathSelBtn.clicked.connect(self.onZipStegOutputPathSelBtnClick)
        self.ui.zipInjectBtn.clicked.connect(self.onZipInjectBtnClick)
        self.ui.zipToExtractPathSelBtn.clicked.connect(self.onZipToExtractPathSelBtnClick)
        self.ui.zipExtractBtn.clicked.connect(self.onZipExtractBtnClick)
        self.ui.zipExtractOutputPathSelBtn.clicked.connect(self.onZipExtractOutputPathSelBtnClick)
    
    def onZipPseSelBtnClick(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Select File", filter = "Zip Files (*.zip)")
        
        self.ui.zipPsePathEdit.setText(filePath)
        
    def onZipPseSelOutputBtn(self):
        folderPath = QFileDialog.getExistingDirectory(self, "Select Folder")
        
        self.ui.zipPseOutputPathEdit.setText(folderPath)
    def onPseEncBtnClick(self):
        filePath = self.ui.zipPsePathEdit.text()
        outputPath = self.ui.zipPseOutputPathEdit.text()
        if filePath == '' or outputPath == '':
            QMessageBox.warning(self, "警告", "Zip文件/輸出路徑為空，請先選擇")
            return
        ZipFake.encrypt(filePath, outputPath)
        QMessageBox.information(self, "提示", "加密成功")

    def onPseDecBtnClick(self):
        filePath = self.ui.zipPsePathEdit.text()
        outputPath = self.ui.zipPseOutputPathEdit.text()
        if filePath == '' or outputPath == '':
            QMessageBox.warning(self, "警告", "Zip文件/輸出路徑為空，請先選擇")
            return
        ZipFake.decrypt(filePath, outputPath)
        QMessageBox.information(self, "提示", "解密成功")
    
    def onZipStegPathSelBtnClick(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Select File", filter = "Zip Files (*.zip)")
        
        self.ui.zipStegPathEdit.setText(filePath)

    def onZipStegInjectPathSelBtnClick(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Select File")
        
        self.ui.zipStegInjectPathEdit.setText(filePath)

    def onZipStegOutputPathSelBtnClick(self):
        folderPath = QFileDialog.getExistingDirectory(self, "Select Folder")
        
        self.ui.zipStegOutputPathEdit.setText(folderPath)


    def onZipInjectBtnClick(self):
        zipFilePath = self.ui.zipStegPathEdit.text()
        injectFilePath = self.ui.zipStegInjectPathEdit.text()
        outputPath = self.ui.zipStegOutputPathEdit.text()
        if zipFilePath == '' or outputPath == '' or injectFilePath == '':
            QMessageBox.warning(self, "警告", "Zip文件/注入文件/輸出路徑為空，請先選擇")
            return
        
        zipSteg = ZipSteganography()
        zipSteg.inject(zipFilePath, injectFilePath, outputPath)
        QMessageBox.information(self, "提示", "注入成功")
        

    def onZipExtractBtnClick(self):
        zipFilePath = self.ui.zipToExtractPathEdit.text()
        outputPath = self.ui.zipExtractOutputPathEdit.text()
        if zipFilePath == '' or outputPath == '':
            QMessageBox.warning(self, "警告", "Zip文件/輸出路徑為空，請先選擇")
            return
        
        zipSteg = ZipSteganography()
        zipSteg.extract(zipFilePath, outputPath)
        QMessageBox.information(self, "提示", "提取成功")

    def onZipToExtractPathSelBtnClick(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Select File", filter = "Zip Files (*.zip)")
        
        self.ui.zipToExtractPathEdit.setText(filePath)
    
    def onZipExtractOutputPathSelBtnClick(self):
        folderPath = QFileDialog.getExistingDirectory(self, "Select Folder")
        
        self.ui.zipExtractOutputPathEdit.setText(folderPath)

def test2():
    origZipPath = r"C:\Users\user\Desktop\todoooo.zip"
    injectFilePath = "C:/Users/user/Desktop/A/github/Img_steg_tool/test.png"
    outputFilePath = r"C:\Users\user\Desktop\A\github\Img_steg_tool"
    zipSteg = ZipSteganography()
    zipSteg.inject(origZipPath, injectFilePath, outputFilePath)

    zipSteg.extract(r"C:\Users\user\Desktop\A\github\Img_steg_tool\todoooo_zipsteg.zip", outputFilePath)

def test1():
    inputPath = r"C:\Users\user\Desktop\todoooo.zip"
    outputPath = r"C:\Users\user\Desktop\A\github\Img_steg_tool"
    ZipFake.encrypt(inputPath, outputPath)
    ZipFake.decrypt(outputPath + '\\' + 'todoooo_enc.zip', outputPath)




if __name__ == "__main__":
    # test1()
    test2()
    