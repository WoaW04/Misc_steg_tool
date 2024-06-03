import os
import sys
import numpy as np
from hashlib import md5
from PyQt5.QtGui import *
from PyQt5 import QtCore
import PIL.Image as Image
from PyQt5.QtWidgets import *
from cv2 import imread, imwrite
from PyQt5 import QtWidgets, uic
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet

class Ui(QtWidgets.QMainWindow):
    #显示消息/错误
    def displayMsg(self,title,msg,ico_type=None):
        MsgBox = QtWidgets.QMessageBox()
        MsgBox.setText(msg)
        MsgBox.setWindowTitle(title)
        if ico_type == 'err':
            ico = QtWidgets.QMessageBox.Critical
        else:
            ico = QtWidgets.QMessageBox.Information
        MsgBox.setIcon(ico)
        MsgBox.exec()

    #输入图像文件
    def getFile(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(None, '打开文件','',"图像文件 (*.jpg *.png *.bmp)")[0]
        if file_path != '':
            self.lineEdit.setText(file_path)

    #保存隐写的图像文件
    def saveFile(self):
        output_path = QtWidgets.QFileDialog.getSaveFileName(None, '保存编码后的文件','',"PNG文件(*.png)")[0]
        return output_path

    #图像隐写文本数据
    def encode(self):
        input_path = self.lineEdit.text()
        text = self.plainTextEdit.toPlainText()
        password = self.lineEdit_2.text()
        if input_path == '':
            self.displayMsg('错误','请选择输入的图像文件！','err')
        elif text == '':
            self.displayMsg('错误','请输入隐写文本！','err')
        elif password == '':
            self.displayMsg('错误','请输入加密密码！','err')
        else:
            output_path = self.saveFile()
            if output_path == '':
                self.displayMsg('取消操作','用户取消了操作！')
            else:
                try:
                    loss = encode(input_path,text,output_path,password,self.progressBar)
                except FileError as fe:
                    self.displayMsg('错误',str(fe),'err')
                except DataError as de:
                    self.displayMsg('错误',str(de),'err')
                else:
                    self.displayMsg('成功','编码成功！\n\n图像数据损失 = {:.5f} %'.format(loss))
                    self.progressBar.setValue(0)

    #提取图像隐写的文本数据
    def decode(self):
        input_path = self.lineEdit.text()
        password = self.lineEdit_3.text()
        if input_path == '':
            self.displayMsg('错误','请选择输入的图像文件！','err')
        elif password == '':
            self.displayMsg('错误','请输入解密密码！','err')
        else:
            try:
                data = decode(input_path,password,self.progressBar_2)
            except FileError as fe:
                self.displayMsg('错误',str(fe),'err')
            except PasswordError as pe:
                self.displayMsg('错误',str(pe),'err')
                self.progressBar_2.setValue(0)
            else:
                self.displayMsg('成功','提取成功！')
                self.plainTextEdit_2.document().setPlainText(data)
                self.progressBar_2.setValue(0)
        
    #输入隐写文件
    def getFile_1(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(None, '打开文件','',"全部文件 (*)")[0]
        if file_path != '':
            self.lineEdit_4.setText(file_path)

    #提取隐写的文件
    def saveFile_1(self):
        output_path = QtWidgets.QFileDialog.getSaveFileName(None, '保存提取的文件','',"全部文件(*)")[0]
        return output_path

    #图像隐写文件数据
    def encodefile(self):
        input_path = self.lineEdit.text()
        secret_filepath = self.lineEdit_4.text()
        password = self.lineEdit_5.text()
        if input_path == '':
            self.displayMsg('错误','请选择输入的图像文件！','err')
        elif secret_filepath == '':
            self.displayMsg('错误','请输入隐写文件！')
        elif password == '':
            self.displayMsg('错误','请输入加密密码！','err')
        else:
            output_path = self.saveFile()
            if output_path == '':
                self.displayMsg('取消操作','用户取消了操作！')
            else:
                try:
                    loss = encodefile(input_path,secret_filepath,output_path,password,self.progressBar_3)
                except FileError as fe:
                    self.displayMsg('错误',str(fe),'err')
                except DataError as de:
                    self.displayMsg('错误',str(de),'err')
                else:
                    self.displayMsg('成功','编码成功！\n\n图像数据损失 = {:.5f} %'.format(loss))
                    self.progressBar_3.setValue(0)

    #提取图像隐写的文件数据
    def decodefile(self):
        input_path = self.lineEdit.text()
        password = self.lineEdit_6.text()
        if input_path == '':
            self.displayMsg('错误','请选择输入的图像文件！','err')
        elif password == '':
            self.displayMsg('错误','请输入解密密码！','err')
        else:
            try:
                output_path = self.saveFile_1()
                data = decodefile(input_path,output_path,password,self.progressBar_4)
            except FileError as fe:
                self.displayMsg('错误',str(fe),'err')
            except PasswordError as pe:
                self.displayMsg('错误',str(pe),'err')
                self.progressBar_2.setValue(0)
            else:
                self.displayMsg('成功','提取成功！')
                self.plainTextEdit_3.document().setPlainText(data)
                self.progressBar_4.setValue(0)
        
    # 显示在主程序Tab中的标题
    NAME = "LSB隐写模块"
    UI_PATH = os.path.dirname(__file__) + '/' + "LSBWindow.ui"

    def __init__(self):
        super().__init__()
        self.mainLayout = None
        self.ui = uic.loadUi(self.UI_PATH, self)  # 加载UI

    def InitUI(self):
        # LSB文本隐写
        self.pushButton.clicked.connect(self.getFile)
        self.pushButton_2.clicked.connect(self.encode)
        self.pushButton_3.clicked.connect(self.decode)
        self.checkBox.stateChanged.connect(lambda: self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal) if self.checkBox.isChecked() else self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password))
        self.checkBox_2.stateChanged.connect(lambda: self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Normal) if self.checkBox_2.isChecked() else self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password))
        # LSB文件隐写
        self.pushButton_4.clicked.connect(self.getFile_1)
        self.pushButton_5.clicked.connect(self.encodefile)
        self.pushButton_6.clicked.connect(self.decodefile)
        self.checkBox_3.stateChanged.connect(lambda: self.lineEdit_5.setEchoMode(QtWidgets.QLineEdit.Normal) if self.checkBox_3.isChecked() else self.lineEdit_5.setEchoMode(QtWidgets.QLineEdit.Password))
        self.checkBox_4.stateChanged.connect(lambda: self.lineEdit_6.setEchoMode(QtWidgets.QLineEdit.Normal) if self.checkBox_4.isChecked() else self.lineEdit_6.setEchoMode(QtWidgets.QLineEdit.Password))

class FileError(Exception):
    pass

class DataError(Exception):
    pass

class PasswordError(Exception):
    pass

#字符串转二进制
def str2bin(string):
    return ''.join((bin(ord(i))[2:]).zfill(7) for i in string)

#二进制转字符串
def bin2str(string):
    return ''.join(chr(int(string[i:i+7],2)) for i in range(len(string))[::7])

#根据输入的密码返回字符串的加密/解密形式
def encrypt_decrypt(string,password,mode='dec'):
    _hash = md5(password.encode()).hexdigest()
    cipher_key = urlsafe_b64encode(_hash.encode())
    cipher = Fernet(cipher_key)
    if mode == 'enc':
        return cipher.encrypt(string.encode()).decode()
    else:
        return cipher.decrypt(string.encode()).decode()

#图像隐写文本数据
def encode(input_filepath,text,output_filepath,password=None,progressBar=None):
    if password != None:
        data = encrypt_decrypt(text,password,'enc')
    else:
        data = text
    data_length = bin(len(data))[2:].zfill(32)
    bin_data = iter(data_length + str2bin(data))
    img = imread(input_filepath,1)
    if img is None:
        raise FileError("无法访问图像文件{}".format(input_filepath))
    height,width = img.shape[0],img.shape[1]
    encoding_capacity = height*width*3
    total_bits = 32+len(data)*7
    if total_bits > encoding_capacity:
        raise DataError("隐写数据大小太大，图像无法容纳！")
    completed = False
    modified_bits = 0
    progress = 0
    progress_fraction = 1/total_bits
        
    for i in range(height):
        for j in range(width):
            pixel = img[i,j]
            for k in range(3):
                try:
                    x = next(bin_data)
                except StopIteration:
                    completed = True
                    break
                if x == '0' and pixel[k]%2==1:
                    pixel[k] -= 1
                    modified_bits += 1
                elif x=='1' and pixel[k]%2==0:
                    pixel[k] += 1
                    modified_bits += 1
                if progressBar != None: #如果进度条对象被传递
                    progress += progress_fraction
                    progressBar.setValue(int(progress*100))
            if completed:
                break
        if completed:
            break

    written = imwrite(output_filepath,img)
    if not written:
        raise FileError("隐写数据写入图像{}失败".format(output_filepath))
    loss_percentage = (modified_bits/encoding_capacity)*100
    return loss_percentage

#提取图像隐写的文本数据
def decode(input_filepath,password=None,progressBar=None):
    result,extracted_bits,completed,number_of_bits = '',0,False,None
    img = imread(input_filepath)
    if img is None:
        raise FileError("无法访问图像文件{}".format(input_filepath))
    height,width = img.shape[0],img.shape[1]
    for i in range(height):
        for j in range(width):
            for k in img[i,j]:
                result += str(k%2)
                extracted_bits += 1
                if progressBar != None and number_of_bits != None: #如果进度条对象被传递
                    progressBar.setValue(int(100*(extracted_bits/number_of_bits)))
                if extracted_bits == 32 and number_of_bits == None: #如果提取出前32位，它就是我们的数据大小，现在提取原始数据
                    number_of_bits = int(result,2)*7
                    result = ''
                    extracted_bits = 0
                elif extracted_bits == number_of_bits:
                    completed = True
                    break
            if completed:
                break
        if completed:
            break
    if password == None:
        return bin2str(result)
    else:
        try:
            return encrypt_decrypt(bin2str(result),password,'dec')
        except:
            raise PasswordError("密码无效！")

#根据输入的密码返回字符串的加密/解密形式
def encrypt_decrypt_1(data,password,mode='enc'):
    _hash = md5(password.encode()).hexdigest()
    cipher_key = urlsafe_b64encode(_hash.encode())
    cipher = Fernet(cipher_key)
    if mode == 'enc':
        return cipher.encrypt(data).decode()
    else:
        return cipher.decrypt(data).decode()

#图像隐写文件数据
def encodefile(input_filepath,secret_filepath,output_filepath,password=None,progressBar=None):
    with open(secret_filepath,'rb') as file:
        secret_data = file.read()
    if password != None:
        data = encrypt_decrypt_1(secret_data,password,'enc')
    else:
        data = secret_data
    data_length = bin(len(data))[2:].zfill(32)
    bin_data = iter(data_length + str2bin(data))
    img = imread(input_filepath,1)
    if img is None:
        raise FileError("无法访问图像文件{}".format(input_filepath))
    height,width = img.shape[0],img.shape[1]
    encoding_capacity = height*width*3
    total_bits = 32+len(data)*7
    if total_bits > encoding_capacity:
        raise DataError("隐写数据大小太大，图像无法容纳！")
    completed = False
    modified_bits = 0
    progress = 0
    progress_fraction = 1/total_bits
        
    for i in range(height):
        for j in range(width):
            pixel = img[i,j]
            for k in range(3):
                try:
                    x = next(bin_data)
                except StopIteration:
                    completed = True
                    break
                if x == '0' and pixel[k]%2==1:
                    pixel[k] -= 1
                    modified_bits += 1
                elif x=='1' and pixel[k]%2==0:
                    pixel[k] += 1
                    modified_bits += 1
                if progressBar != None: #如果进度条对象被传递
                    progress += progress_fraction
                    progressBar.setValue(int(progress*100))
            if completed:
                break
        if completed:
            break

    written = imwrite(output_filepath,img)
    if not written:
        raise FileError("隐写数据写入图像{}失败".format(output_filepath))
    loss_percentage = (modified_bits/encoding_capacity)*100
    return loss_percentage

#提取图像隐写的文件数据
def decodefile(input_filepath,output_filepath,password=None,progressBar=None):
    result,extracted_bits,completed,number_of_bits = '',0,False,None
    img = imread(input_filepath)
    if img is None:
        raise FileError("无法访问图像文件{}".format(input_filepath))
    height,width = img.shape[0],img.shape[1]
    for i in range(height):
        for j in range(width):
            for k in img[i,j]:
                result += str(k%2)
                extracted_bits += 1
                if progressBar != None and number_of_bits != None: #如果进度条对象被传递
                    progressBar.setValue(int(100*(extracted_bits/number_of_bits)))
                if extracted_bits == 32 and number_of_bits == None: #如果提取出前32位，它就是我们的数据大小，现在提取原始数据
                    number_of_bits = int(result,2)*7
                    result = ''
                    extracted_bits = 0
                elif extracted_bits == number_of_bits:
                    completed = True
                    break
            if completed:
                break
        if completed:
            break
    if password == None:
        return bin2str(result)
    else:
        try:
            original_data = encrypt_decrypt(bin2str(result),password,'dec').encode()
            with open(output_filepath, 'wb') as file:
                file.write(original_data)
            return "数据已成功解码并写入文件：{}".format(output_filepath)
        except:
            raise PasswordError("密码无效！")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.InitUI()
    window.show()
    sys.exit(app.exec_())