from cv2 import imread,imwrite
import numpy as np
from base64 import urlsafe_b64encode
from hashlib import md5
from cryptography.fernet import Fernet

class FileError(Exception):
    pass

class DataError(Exception):
    pass

class PasswordError(Exception):
    pass

#返回字符串的二进制表示形式（字符串转二进制）
def str2bin(string):
    return ''.join((bin(ord(i))[2:]).zfill(7) for i in string)

#返回二进制的字符串表示形式（二进制转字符串）
def bin2str(string):
    return ''.join(chr(int(string[i:i+7],2)) for i in range(len(string))[::7])

#根据输入的密码返回字符串的加密/解密形式
def encrypt_decrypt(string,password,mode='enc'):
    _hash = md5(password.encode()).hexdigest()
    cipher_key = urlsafe_b64encode(_hash.encode())
    cipher = Fernet(cipher_key)
    if mode == 'enc':
        return cipher.encrypt(string.encode()).decode()
    else:
        return cipher.decrypt(string.encode()).decode()

#对图像中的秘密数据进行编码
def encode(input_filepath,text,output_filepath,password=None,progressBar=None):
    if password != None:
        data = encrypt_decrypt(text,password,'enc') #如果输入了密码，则使用给定的密码加密数据
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

#对图像中的秘密数据进行解码
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

if __name__ == "__main__":

    ch = int(input('你要想进行什么操作？\n\n1.加密\n2.解密\n\n请输入(1或2)：'))
    if ch == 1:
        ip_file = input('\n输入图片名称(路径)(带扩展名)：')
        text = input('输入需要隐藏的数据：')
        pwd = input('输入加密密码：')
        op_file = input('输入隐写后的图片名称(路径)(带扩展名)：')
        try:
            loss = encode(ip_file,text,op_file,pwd)
        except FileError as fe:
            print("错误：{}".format(fe))
        except DataError as de:
            print("错误：{}".format(de))
        else:
            print('加密成功!\n图像数据损失 = {:.5f}%'.format(loss))
    elif ch == 2:
        ip_file = input('输入图片名称(路径)(带扩展名)：')
        pwd = input('输入解密密码：')
        try:
            data = decode(ip_file,pwd)
        except FileError as fe:
            print("错误：{}".format(fe))
        except PasswordError as pe:
            print('错误：{}'.format(pe))
        else:
            print('解密的数据:',data)
    else:
        print('错误选项！')