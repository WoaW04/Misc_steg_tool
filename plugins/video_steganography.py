import os
from PyQt5.QtCore import QObject
import pyzipper
import subprocess
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

def getCurrentPath():
    if hasattr(sys, 'frozen'):  # 可执行文件走这里
        return os.path.dirname(sys.executable) + "/plugins/"
    return os.path.dirname(__file__)  # 源码走这里

class Ui(QtWidgets.QMainWindow):
    # 顯示在主程序Tab中的標題
    NAME = "Video隱寫模塊"
    UI_PATH = os.path.join(getCurrentPath(), "VideoStegWindow.ui")
    signal = None

    def __init__(self):
        super().__init__()
        self.mainLayout = None
        self.ui = uic.loadUi(self.UI_PATH, self)

        self.initUi()

    def initUi(self):
        self.ui.outputPathSelBtn.clicked.connect(self.onOutputPathSelBtnClick)
        self.ui.coverVideoSelBtn.clicked.connect(self.onCoverVideoSelBtnClick)
        self.ui.injectPathSelBtn.clicked.connect(self.onInjectPathSelBtnClick)
        self.ui.extractVideoSelBtn.clicked.connect(self.onExtractVideoSelBtnClick)
        self.ui.startStegBtn.clicked.connect(self.onStartStegBtnClick)
        self.ui.extractBtn.clicked.connect(self.onExtractBtnClick)
        self.ui.videoTypeCbx.currentIndexChanged.connect(self.onVideoTypeChanged)
        self.ui.injectTypeCbx.currentIndexChanged.connect(self.onInjectTypeChanged)

        self.ui.progressBar.setValue(0)

    def onVideoTypeChanged(self, index):

        self.ui.coverVideoPathEdit.setText("")
    def onInjectTypeChanged(self, index):

        self.ui.injectPathEdit.setText("")

    def check(self, *args):
        for arg in args:
            if arg == '':
                return False
        return True

    def onOutputPathSelBtnClick(self):
        folderPath = QFileDialog.getExistingDirectory(self, "Select Folder")
        
        self.ui.outputPathEdit.setText(folderPath)

    def onCoverVideoSelBtnClick(self):
        videoType = self.ui.videoTypeCbx.currentText()
        filePath, _ = QFileDialog.getOpenFileName(self, "Select File", filter = f"*.{videoType}")
        
        self.ui.coverVideoPathEdit.setText(filePath)

    def onInjectPathSelBtnClick(self):
        injectType = self.ui.injectTypeCbx.currentText()
        if injectType == "File":
            path, _ = QFileDialog.getOpenFileName(self, "Select File")
        else:
            path = QFileDialog.getExistingDirectory(self, "Select Folder")
        

        
        self.ui.injectPathEdit.setText(path)

    def onExtractVideoSelBtnClick(self):
        videoType = self.ui.videoTypeCbx.currentText()
        filePath, _ = QFileDialog.getOpenFileName(self, "Select File", filter = f"*.{videoType}")
        
        self.ui.extractVideoPathEdit.setText(filePath)

    def onStartStegBtnClick(self):
        videoType = self.ui.videoTypeCbx.currentText()
        inputFilePath = self.ui.injectPathEdit.text()
        coverVideoPath = self.ui.coverVideoPathEdit.text()
        password = None if self.ui.pwdEdit.text() == '' else self.ui.pwdEdit.text()
        outputPath = self.ui.outputPathEdit.text()

        if(not self.check(inputFilePath, coverVideoPath, outputPath)):
            QMessageBox.warning(self, "警告", "請檢查是否已選擇所有必選的路徑!!!")
            return
        
        self.ui.progressBar.setValue(0)

        steganographier = VideoStegThread(self, "inject", inputFilePath, coverVideoPath, password, outputPath, videoType)
        # self.workThread = WorkThread(steganographier.inject, inputFilePath, coverVideoPath, password, outputPath, videoType)
        steganographier.progressBarSignal.connect(self.onProgressBarUpdate)
        steganographier.updateUISignal.connect(self.onStegUpdate)
        # steganographier.inject(inputFilePath=inputFilePath, coverVideoPath=coverVideoPath, password=password, outputPath=outputPath, videoType=videoType)

        steganographier.start()

        

        # QMessageBox.information(self, "提示", "視頻隱寫成功!!!")

    def onStegUpdate(self, data):
        '''
        處理VideoSteg傳來的更新UI/處理完成信號

        Args: 
            data(dict): 該字典有以下屬性
                - type(str): "UI_UPDATE" | "DONE"
                - objectName(str): 定位ui控件的objectName
                - text(str): 要設置的text值
        '''
        if data["type"] == "UI_UPDATE":
            getattr(self.ui, data["objectName"]).setText(data["text"])
        elif data["type"] == "DONE":
            QMessageBox.information(self, "提示", data["text"])
        
    def onExtractBtnClick(self):
        inputFilePath = self.ui.extractVideoPathEdit.text()
        password = None if self.ui.pwdEdit.text() == '' else self.ui.pwdEdit.text()
        videoType = self.ui.videoTypeCbx.currentText()
        outputPath = self.ui.outputPathEdit.text()

        if(not self.check(inputFilePath, outputPath)):
            QMessageBox.warning(self, "警告", "請檢查是否已選擇所有必選的路徑!!!")
            return
        
        steganographier = VideoStegThread(self, "extract", inputFilePath, outputPath, password, videoType)
        steganographier.updateUISignal.connect(self.onStegUpdate)
        steganographier.start()

    

    def onProgressBarUpdate(self, num):
        self.ui.progressBar.setValue(num)


class VideoStegThread(QThread):
    progressBarSignal = pyqtSignal(int)
    updateUISignal = pyqtSignal(dict)

    def __init__(self, parent, func, *args):
        super(VideoStegThread, self).__init__(parent)
        print("func: ", func)
        self.mkvmergeExe = os.path.join(getCurrentPath(),'tools','mkvmerge.exe')
        self.mkvextractExe = os.path.join(getCurrentPath(),'tools','mkvextract.exe')
        self.mkvinfoExe = os.path.join(getCurrentPath(),'tools','mkvinfo.exe')

        self.totalFileSize = None
        self.func = func
        self.args = args


    
    def run(self):
        if self.func == "inject":
            self.inject(*self.args)
        elif self.func == "extract":
            self.extract(*self.args)

    def updateProgressBar(self, num):
        self.progressBarSignal.emit(num)

    def readInChunks(self, file_object, chunk_size = 1024*1024):
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data


    def compressFiles(self, zipFilePath, inputFilePath, processedSize=0, password=None):
        '''
        壓縮指定文件

        Args:
            zipFilePath(str): zip文件的路徑
            inputFilePath(str): 待隱寫的文件
            processedSize(int): 表示處理進度, 默認為0
            password(int): zip文件的密碼, 默認為None
        '''
        # 若password不為None, 則為zip設置指定密碼
        if password:
            zipFile = pyzipper.AESZipFile(zipFilePath, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES)
            zipFile.setpassword(password.encode())
        else:
            zipFile = pyzipper.ZipFile(zipFilePath, 'w', compression=pyzipper.ZIP_DEFLATED)
        

        with zipFile:
            print(f"Compressing file: {inputFilePath}")
            
            # 當被隱寫的是文件夾時
            if os.path.isdir(inputFilePath):
                rootFolder = os.path.basename(inputFilePath)
                # 隱寫目錄下所有文件
                for root, dirs, files in os.walk(inputFilePath):
                    for file in files:
                        fileFullPath = os.path.join(root, file)
                        arcname = os.path.join(rootFolder, os.path.relpath(fileFullPath, start=inputFilePath))
                        zipFile.write(fileFullPath, arcname)
                        
                        # 更新進度條
                        processedSize += os.path.getsize(fileFullPath)

                        self.updateProgressBar(int(100* (processedSize / self.totalFileSize)))
                        
            # 表示只有單一文件
            else: 
                
                zipFile.write(inputFilePath, os.path.basename(inputFilePath))
                # 更新進度條
                processedSize = os.path.getsize(inputFilePath)

                self.updateProgressBar(int(100* (processedSize / self.totalFileSize)))

    def setProgressState(self, state):
        if state == "compress":
            stateText = "正在對待注入文件進行壓縮......"
        elif state == "inject":
            stateText = "壓縮完成，正在合並中......"

        elif state == "complete":
            stateText = "無"

        elif state == "extract":
            stateText = "隱寫附件提取中......"

        self.updateUISignal.emit({
            "type": "UI_UPDATE",
            "objectName": "progressStateLabel",
            "text": stateText
        })
    
    def sendDoneSignal(self, text):
        self.updateUISignal.emit({
            "type": "DONE",
            "objectName": None,
            "text": text
        })

    def inject(self, inputFilePath, 
                  coverVideoPath=None, 
                  password=None, 
                  outputPath=None, 
                  videoType=None):
        '''
        隱寫的具體邏輯

        Args:
            inputFilePath(str): 待隱寫的文件/文件夾路徑
            coverVideoPath(str): 作為載體的視頻的路徑
            password(str): zip文件的密碼
            outputPath(str): 輸出目錄
            videoType(str): 視頻類型, 只支援mp4/mkv
        '''

        # 臨時zip文件名
        zipFilePath = os.path.join(os.path.splitext(inputFilePath)[0] + "_hidden_tmp.zip")
        
        # 計算要隱寫的文件的總大小, 分文件夾/文件兩種情況
        self.totalFileSize = 0
        if os.path.isdir(inputFilePath):
            for root, dirs, files in os.walk(inputFilePath):
                for file in files:
                    fileFullPath = os.path.join(root, file)
                    self.totalFileSize += os.path.getsize(fileFullPath)
        else:
            self.totalFileSize = os.path.getsize(inputFilePath)
        
        print("totalFileSize: ", self.totalFileSize)

        # processedSize表示處理進度
        processedSize = 0

        # 設置顯示在UI上的進度狀態
        self.setProgressState("compress")

        # 創建隱寫的臨時zip文件 (最終注入到coverVideo的是zip文件)
        self.compressFiles(zipFilePath, inputFilePath, processedSize=processedSize, password=password)

        self.updateProgressBar(0)
        self.setProgressState("inject")

        try:        
            # mp4的隱寫邏輯
            if videoType == 'mp4':
                # 輸出文件名
                outputFile = outputPath + '/' + coverVideoPath.split('/')[-1].split('.')[0] + "_hidden.mp4"
            
                try:
                    totalSizeHidden = os.path.getsize(coverVideoPath) + os.path.getsize(zipFilePath)
                    print("totalSizeHidden: ", totalSizeHidden)
                    processedSize = 0
                    with open(coverVideoPath, "rb") as file1:
                        with open(zipFilePath, "rb") as file2:
                            with open(outputFile, "wb") as output:
                                print(f"Hiding file: {inputFilePath}")

                                # 載體mp4
                                for chunk in self.readInChunks(file1):
                                    output.write(chunk)
                                    processedSize += len(chunk)

                                    self.updateProgressBar(int(100* (processedSize / totalSizeHidden)))

                                # zip
                                for chunk in self.readInChunks(file2):
                                    output.write(chunk)
                                    processedSize += len(chunk)
                                    self.updateProgressBar(int(100* (processedSize / totalSizeHidden)))
                
                except Exception as e:
                    print(f"MP4文件寫入錯誤: {str(e)}")
                    raise

            # mkv的隱寫邏輯
            elif videoType == 'mkv':
                outputFile = outputPath + '/' + coverVideoPath.split('/')[-1].split('.')[0] + "_hidden.mkv"
 
                try:
                    # 通過cmd調用 mkvmergeExe 來合並目標
                    cmd = [
                        self.mkvmergeExe, '-o',
                        outputFile, coverVideoPath,
                        '--attach-file', zipFilePath,
                    ]

                    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

                    if result.returncode != 0:
                        raise subprocess.CalledProcessError(result.returncode, cmd, output=result.stdout, stderr=result.stderr)

                except subprocess.CalledProcessError as cpe:
                    print(f"隱寫時發生錯誤: {str(cpe)}")
                    print(f'CalledProcessError output：{cpe.output}') if cpe.output else None
                    print(f'CalledProcessError stderr：{cpe.stderr}') if cpe.stderr else None
                    raise

                except Exception as e:
                    print(f"執行mkvmerge發生錯誤: {str(e)}")
                    raise

            self.setProgressState("complete")
            self.sendDoneSignal("視頻隱寫成功!!!")
        except Exception as e:
            print(f"隱寫時發生錯誤: {str(e)}")
            raise
        finally:
            # 刪除臨時的zip文件
            os.remove(zipFilePath)

    
    def extract(self, inputFilePath, outputPath, password=None, videoType=None):
        '''
        提取隱寫文件/文件夾
        
        Args:
            inputFilePath(str): 待提取的視頻路徑
            password(str): zip密碼, 需與inject時相同
            videoType(str): 視頻類型, 只支援mp4/mkv
        '''
        self.setProgressState("extract")
        if videoType == 'mp4':
            try:
                with open(inputFilePath, "rb") as file:
                    zipData = file.read()

                outputFile = outputPath + '/' + inputFilePath.split('/')[-1].split('.')[0] + "_extracted.zip"
                # 創建臨時zip文件
                zipPath = outputFile
                with open(zipPath, "wb") as file:
                    file.write(zipData)

                # 解壓臨時zip文件
                if password:
                    with pyzipper.AESZipFile(zipPath) as zipFile:
                        zipFile.setpassword(password.encode())
                        zipFile.extractall(os.path.dirname(zipPath))
                else:
                    with pyzipper.ZipFile(zipPath, 'r') as zipFile:
                        zipFile.extractall(os.path.dirname(zipPath))

                # 刪除臨時zip文件
                os.remove(zipPath)

            except Exception as e:
                if os.path.exists(zipPath):
                    os.remove(zipPath)
        
        elif videoType == 'mkv':
            # 獲取mkv附件id的函數
            def getAttachmentName(inputFilePath):
                cmd = [self.mkvinfoExe, inputFilePath]
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
                    lines = result.stdout.splitlines()
                    # 只取第一個附件的實際名稱
                    for idx, line in enumerate(lines):
                        if "MIME" in line:
                            parts = lines[idx-1].split(':')
                            attachmentsName = parts[1].strip().split()[-1]
                            break
                except Exception as e:
                    print(f"獲取附件名稱失敗: {e}")
                
                return attachmentsName
            
            # 提取mkv附件
            def extractAttachment(inputFilePath, outputPath):
                cmd = [
                    self.mkvextractExe, 'attachments',
                    inputFilePath,
                    f'1:{outputPath}'
                ]
                try:
                    subprocess.run(cmd, check=True)
                except subprocess.CalledProcessError as e:
                    raise Exception(f"提取附件失敗: {e}")   
                    

            attachmentsName = getAttachmentName(inputFilePath)
            if attachmentsName:
                outputPath = os.path.join(os.path.dirname(inputFilePath), attachmentsName)

                try:
                    extractAttachment(inputFilePath, outputPath)

                    if attachmentsName.endswith('.zip'):
                        try:
                            zipPath = outputPath
                            print(f"Extracting ZIP file: {zipPath}")
                            with pyzipper.AESZipFile(zipPath, 'r', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zipFile:
                                zipFile.extractall(os.path.dirname(inputFilePath), pwd=password.encode())
                            
                            os.remove(zipPath)
                    
                        except RuntimeError as e:
                            print(e)
                except subprocess.CalledProcessError as e:
                    print(e)

            else:
                print("該mkv文件沒有可提取的附件")

        self.setProgressState("complete")
        self.sendDoneSignal("隱寫附件提取成功!!!")



