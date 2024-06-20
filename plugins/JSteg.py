import io
import os
import sys
import magic
import numpy as np
import jpegio as jio
from hashlib import md5
from base64 import urlsafe_b64encode
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from cryptography.fernet import Fernet
from PyQt5.QtCore import pyqtSignal

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import sys
def getCurrentPath():
    if hasattr(sys, 'frozen'):  # 可执行文件走这里
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)  # 源码走这里

class Ui(QMainWindow):
    # 显示在主程序Tab中的标题
    NAME = "JSteg隐写模块"
    UI_PATH = os.path.join(getCurrentPath(), "JSteg.ui")
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.mainLayout = None
        self.ui = uic.loadUi(self.UI_PATH, self)  # 加载UI
        self.InitUI()

    def InitUI(self):

        self.setWindowTitle("JPEG图片水印工具")
        self.resize(800, 600)
        self.center()

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.inject_tab = QWidget()
        self.extract_tab = QWidget()

        self.tab_widget.addTab(self.inject_tab, "盲水印注入")
        self.tab_widget.addTab(self.extract_tab, "盲水印提取")

        self.init_steg_tab()
        self.init_extract_tab()
        self.create_menu()
        self.signal.connect(self.onMainMessage)

    def onMainMessage(self, message):
        # 接收來自主窗口的信息
        self.lineEdit.setText(message)

    def init_steg_tab(self):
        self.layout = QVBoxLayout()

        self.steg_image_label = QLabel("图片路径：")
        self.layout.addWidget(self.steg_image_label)

        self.steg_image_path_label = QLabel()
        self.layout.addWidget(self.steg_image_path_label)

        # 添加密码功能
        self.password_layout = QHBoxLayout()
        self.password_label = QLabel("密码：")
        self.password_layout.addWidget(self.password_label)
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText("可选择是否设置密码")
        self.password_layout.addWidget(self.password_edit)
        self.password_checkbox = QCheckBox("显示密码")
        self.password_checkbox.stateChanged.connect(self.toggle_password_visibility)
        self.password_layout.addWidget(self.password_checkbox)
        self.layout.addLayout(self.password_layout)

        # 添加水印内容
        self.watermark_type_layout = QHBoxLayout()
        self.watermark_type_label = QLabel("选择水印类型：")
        self.watermark_type_layout.addWidget(self.watermark_type_label)
        self.watermark_type_layout.addStretch(1)  # 添加伸缩空间使按钮靠右对齐
        self.text_watermark_button = QPushButton("文本水印")
        self.text_watermark_button.clicked.connect(self.show_text_watermark_dialog)
        self.text_watermark_button.clicked.connect(self.set_mode_text)
        self.watermark_type_layout.addWidget(self.text_watermark_button)
        self.file_watermark_button = QPushButton("文件水印")
        self.file_watermark_button.clicked.connect(self.load_watermark_file)
        self.file_watermark_button.clicked.connect(self.set_mode_file)
        self.watermark_type_layout.addWidget(self.file_watermark_button)
        self.layout.addLayout(self.watermark_type_layout)

        # 信号量，用于指示水印类型
        self.mode = "str"

        self.watermark_content_layout = QVBoxLayout()
        self.watermark_content_label = QLabel("水印内容：")
        self.watermark_content_layout.addWidget(self.watermark_content_label)
        self.watermark_content = QTextEdit()
        self.watermark_content.setReadOnly(True)
        self.watermark_content_layout.addWidget(self.watermark_content)
        self.layout.addLayout(self.watermark_content_layout)

        # 进度条
        self.steg_progress_layout = QHBoxLayout()
        self.steg_progress_label = QLabel("水印注入进度：")
        self.steg_progress_layout.addWidget(self.steg_progress_label)
        self.steg_progress_bar = QProgressBar()
        self.steg_progress_layout.addWidget(self.steg_progress_bar)
        self.layout.addLayout(self.steg_progress_layout)

        self.add_watermark_button = QPushButton("添加水印")
        self.add_watermark_button.clicked.connect(self.add_watermark)
        self.layout.addWidget(self.add_watermark_button)

        self.inject_tab.setLayout(self.layout)

        self.watermark_text_dialog = None

    def init_extract_tab(self):
        layout = QVBoxLayout()

        self.extract_image_label = QLabel("选择待提取的图像文件:")
        layout.addWidget(self.extract_image_label)

        self.extract_image_path_label = QLabel()
        layout.addWidget(self.extract_image_path_label)
        # 添加密码功能
        self.extract_password_layout = QHBoxLayout()
        self.extract_password_label = QLabel("密码：")
        self.extract_password_layout.addWidget(self.extract_password_label)
        self.extract_password_edit = QLineEdit()
        self.extract_password_edit.setEchoMode(QLineEdit.Password)
        self.extract_password_layout.addWidget(self.extract_password_edit)
        self.extract_password_checkbox = QCheckBox("显示密码")
        self.extract_password_checkbox.stateChanged.connect(
            self.toggle_password_visibility
        )
        self.extract_password_layout.addWidget(self.extract_password_checkbox)
        layout.addLayout(self.extract_password_layout)

        # 进度条
        self.extract_progress_layout = QHBoxLayout()
        self.extract_progress_label = QLabel("水印提取进度：")
        self.extract_progress_layout.addWidget(self.extract_progress_label)
        self.extract_progress_bar = QProgressBar()
        self.extract_progress_layout.addWidget(self.extract_progress_bar)
        layout.addLayout(self.extract_progress_layout)

        self.extract_button = QPushButton("提取水印")
        self.extract_button.clicked.connect(self.extract_watermark)
        layout.addWidget(self.extract_button)

        self.extract_output_label = QLabel("提取水印保存路径:")
        layout.addWidget(self.extract_output_label)

        self.extract_tab.setLayout(layout)

    # 显示消息/错误
    def displayMsg(self, title, msg, ico_type=None):
        MsgBox = QMessageBox()
        MsgBox.setText(msg)
        MsgBox.setWindowTitle(title)
        if ico_type == "err":
            ico = QMessageBox.Critical
        else:
            ico = QMessageBox.Information
        MsgBox.setIcon(ico)
        MsgBox.exec()

    def set_mode_text(self):
        self.mode = "str"

    def set_mode_file(self):
        self.mode = "file"

    def create_menu(self):
        open_image_action = QAction("&打开图片", self)
        open_image_action.setShortcut("Ctrl+O")
        open_image_action.triggered.connect(self.load_image)
        clear_image_action = QAction("&清除图片", self)
        clear_image_action.setShortcut("Ctrl+L")
        clear_image_action.triggered.connect(self.clear_all)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&文件")
        file_menu.addAction(open_image_action)
        file_menu.addAction(clear_image_action)

    def load_image(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("JPEG Files (*.jpg *.jpeg)")
        filename, _ = file_dialog.getOpenFileName(
            self, "选择图片", "", "JPEG Files (*.jpg *.jpeg)"
        )
        if filename:
            # 在注入页面显示
            self.steg_image_path_label.setText("图片路径：" + filename)
            pixmap = QPixmap(filename)
            self.steg_image_label.setPixmap(pixmap.scaledToWidth(300))
            # 在提取页面显示
            self.extract_image_path_label.setText("图片路径：" + filename)
            pixmap = QPixmap(filename)
            self.extract_image_label.setPixmap(pixmap.scaledToWidth(300))
            self.origin()

    def show_text_watermark_dialog(self):
        if not self.watermark_text_dialog:
            self.watermark_text_dialog = TextWatermarkDialog(self)

        if self.watermark_text_dialog.exec_() == QDialog.Accepted:
            text_watermark = self.watermark_text_dialog.get_watermark_text()
            if text_watermark:
                self.watermark_content.setText(text_watermark)

    def load_watermark_file(self):
        file_dialog = QFileDialog()
        # file_dialog.setNameFilter("PNG Files (*.png);;Text Files (*.txt)")
        filename, _ = file_dialog.getOpenFileName(self, "选择水印文件", "")
        if filename:
            self.watermark_content.setText(filename)
            self.extract_progress_bar.setValue(0)

    def add_watermark(self):
        self.extract_progress_bar.setValue(0)
        if (
            not hasattr(self, "steg_image_path_label")
            or not self.steg_image_path_label.text()
        ):
            QMessageBox.warning(self, "警告", "请先选择图片")
            return

        if (
            not hasattr(self, "watermark_content")
            or not self.watermark_content.toPlainText()
        ):
            QMessageBox.warning(self, "警告", "请选择水印内容")
            return

        if self.password_edit.text() == "":
            reply = QMessageBox.question(
                self,
                "警告",
                "设置加密密码会提高水印安全性，是否确认不设置加密密码？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.No:
                return

        input_path = self.steg_image_path_label.text().split("：")[1]
        secret_path = self.watermark_content.toPlainText()
        mode = self.mode
        password = (
            self.password_edit.text() if self.password_edit.text() != "" else None
        )

        # 选择保存路径，设置过滤器为JPEG文件
        output_path, _ = QFileDialog.getSaveFileName(
            self, "保存水印文件", "", "JPEG Files (*.jpg *.jpeg)"
        )
        if output_path:
            # 调用embed_message函数
            try:
                embed_message(
                    input_path,
                    secret_path,
                    output_path,
                    password=password,
                    mode=mode,
                    progressBar=self.steg_progress_bar,
                )
            except FileError as fe:
                self.displayMsg("错误", str(fe), "err")
            except ValueError as ve:
                self.displayMsg("错误", str(ve), "err")
            except Exception as e:
                self.displayMsg("错误", str(e), "err")
            else:
                QMessageBox.information(
                    None, "提示", "水印文件已保存至：" + output_path
                )
                self.steg_progress_bar.setValue(0)
                self.password_edit.clear()

    def extract_watermark(self):
        self.extract_progress_bar.setValue(0)
        if (
            not hasattr(self, "extract_image_path_label")
            or not self.extract_image_path_label.text()
        ):
            QMessageBox.warning(self, "警告", "请先选择图片")
            return

        if self.extract_password_edit.text() == "":
            reply = QMessageBox.question(
                self,
                "警告",
                "确定您加密时没有设置密码？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.No:
                return
        image_path = self.extract_image_path_label.text().split("：")[1]
        password = (
            self.extract_password_edit.text()
            if self.extract_password_edit.text() != ""
            else None
        )
        # output_path, _ = QFileDialog.getSaveFileName(self, "保存水印文件", "")
        if image_path:
            try:
                file_type, message = extract_file(
                    image_path,
                    password=password,
                    progressBar=self.extract_progress_bar,
                )
            except FileError as fe:
                self.displayMsg("错误", str(fe), "err")
                self.extract_progress_bar.setValue(0)
            except PasswordError as pe:
                self.displayMsg("错误", str(pe), "err")
                self.extract_progress_bar.setValue(0)
            except Exception as inner_e:
                QMessageBox.warning(None, "警告", f"提取出错: {inner_e}")
                self.extract_progress_bar.setValue(0)
            else:
                QMessageBox.information(
                    None,
                    "提示",
                    f"水印文件类型为{file_type}",
                )
                output_path, _ = QFileDialog.getSaveFileName(
                    self, "请选择保存水印地址：", ""
                )
                if output_path:
                    ex_path = write_binary_file(output_path, message)
                    QMessageBox.information(
                        None,
                        "提示",
                        f"水印文件已保存至：{ex_path}",
                    )
                    self.extract_output_label.setText(f"提取水印保存路径: {ex_path}")
                    self.extract_progress_bar.setValue(0)
                    self.extract_password_edit.clear()
                else:
                    self.origin()

    def center(self):
        # 将窗口移动到屏幕中央
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def toggle_password_visibility(self):
        if self.password_checkbox.isChecked():
            self.password_edit.setEchoMode(QLineEdit.Normal)
        else:
            self.password_edit.setEchoMode(QLineEdit.Password)
        if self.extract_password_checkbox.isChecked():
            self.extract_password_edit.setEchoMode(QLineEdit.Normal)
        else:
            self.extract_password_edit.setEchoMode(QLineEdit.Password)

    def origin(self):
        self.password_edit.clear()
        self.watermark_content.clear()
        self.steg_progress_bar.setValue(0)
        self.watermark_text_dialog = None

        self.extract_password_edit.clear()
        self.extract_progress_bar.setValue(0)
        self.extract_output_label.setText("提取水印保存路径:")

    def clear_all(self):
        # 在注入页面显示
        self.steg_image_path_label.setText("图片路径：")
        self.steg_image_label.clear()
        # 在提取页面显示
        self.extract_image_path_label.setText("选择待提取的图像文件:")
        self.extract_image_label.clear()
        self.origin()


class TextWatermarkDialog(QDialog):
    def __init__(self, parent=None):
        super(TextWatermarkDialog, self).__init__(parent)

        self.setWindowTitle("输入文本水印内容")

        layout = QVBoxLayout()

        self.watermark_text_edit = QTextEdit()
        self.watermark_text_edit.setPlaceholderText("输入文本水印内容")
        layout.addWidget(self.watermark_text_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_watermark_text(self):
        return self.watermark_text_edit.toPlainText()


class FileError(Exception):
    pass


class WriteError(Exception):
    pass


class DataError(Exception):
    pass


class FileWaterMarkError(Exception):
    pass


class PasswordError(Exception):
    pass


# 根据输入的密码返回字符串的加密/解密形式
def encrypt_decrypt(string, password, mode="dec"):
    password = str(password)
    _hash = md5(password.encode()).hexdigest()
    cipher_key = urlsafe_b64encode(_hash.encode())
    cipher = Fernet(cipher_key)
    if mode == "enc":
        return cipher.encrypt(string.encode()).decode()
    else:
        return cipher.decrypt(string.encode()).decode()


# 根据输入的密码返回字符串的加密/解密形式
def encrypt_decrypt_1(data, password, mode="enc"):
    _hash = md5(password.encode()).hexdigest()
    cipher_key = urlsafe_b64encode(_hash.encode())
    cipher = Fernet(cipher_key)
    if mode == "enc":
        return cipher.encrypt(data)
    else:
        return cipher.decrypt(data)


# 检测图片的最大容量
def get_embedding_capacity(dct_coeffs):
    check_dct = get_ac_coeffs(dct_coeffs)
    embedding_capacity = 0
    for i in range(dct_coeffs.shape[0]):
        for j in range(dct_coeffs.shape[1]):
            if check_dct[i, j]:
                if dct_coeffs[i, j] not in (-1, 0, 1):
                    embedding_capacity += 1
    return embedding_capacity


# 设置矩阵检测是否是AC系数
def get_ac_coeffs(dct_coeffs):
    check_dct = np.ones(dct_coeffs.shape, dtype=bool)
    for i in range(0, dct_coeffs.shape[0], 8):
        for j in range(0, dct_coeffs.shape[1], 8):
            check_dct[i, j] = 0
    return check_dct


# 将二进制数据转换为01二进制字符串
def binary_to_binary_str(binary_data):
    binary_str = "".join(format(byte, "08b") for byte in binary_data)
    return binary_str


# 将二进制字符串转换回字节数据
def bits_to_bytes(binary_str):
    byte_data = bytearray()
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i : i + 8]
        byte_str = "".join(map(str, byte))
        byte_data.append(int(byte_str, 2))
    return bytes(byte_data)


# 判断文件类型
def identify_file_type(binary_content):
    file_magic = magic.Magic(mime=True)
    file_type = file_magic.from_buffer(binary_content)
    return file_type


# 将二进制写回文件
def write_binary_file(output_path, binary_content):
    with open(output_path, "wb") as file:
        try:
            file.write(binary_content)
        except:
            raise WriteError("写入出错")
    return output_path


# 水印注入函数
def embed_message(
    image_path, message_path, output_path, password=None, mode="str", progressBar=None
):
    if mode == "file":
        with open(message_path, "rb") as file:
            message = file.read()
    elif mode == "str":
        message = str(message_path)

    if password is not None:
        if mode == "str":
            data = encrypt_decrypt(message, password, "enc")
            message_bits = "".join(format(ord(byte), "08b") for byte in data)
        else:
            data = encrypt_decrypt_1(message, password, "enc")
            message_bits = binary_to_binary_str(data)
    else:
        if mode == "str":
            data = message
            message_bits = "".join(format(ord(byte), "08b") for byte in data)
        else:
            data = message
            message_bits = binary_to_binary_str(data)

    # 水印头（32位）表示水印长度
    message_length = len(message_bits)
    header_bits = format(message_length, "032b")
    total_bits = header_bits + message_bits

    # 读取JPEG图像并加载其DCT系数
    jpeg = jio.read(image_path)

    if jpeg.coef_arrays is None:
        raise FileError("无法访问图像文件{}".format(image_path))
    dct_coeffs = jpeg.coef_arrays[0]

    # 计算可嵌入的最大位数
    embedding_capacity = get_embedding_capacity(dct_coeffs)
    print(f"图像{image_path}的最大嵌入量为{embedding_capacity}bits")
    # 检查消息是否可以嵌入
    if len(total_bits) > embedding_capacity:
        raise ValueError("水印大小过大，无法嵌入图像")

    # 设置DC不可嵌入，AC可以嵌入
    check_dct = get_ac_coeffs(dct_coeffs)
    # 嵌入消息
    bit_index = 0
    for i in range(dct_coeffs.shape[0]):
        for j in range(dct_coeffs.shape[1]):
            if check_dct[i, j]:
                if dct_coeffs[i, j] not in (-1, 1, 0) and bit_index < len(total_bits):
                    lower_bit = int(dct_coeffs[i, j] % 2)
                    bit = int(total_bits[bit_index])
                    if lower_bit != bit:
                        if dct_coeffs[i, j] > 0:
                            if dct_coeffs[i, j] % 2:
                                dct_coeffs[i, j] -= 1
                            else:
                                dct_coeffs[i, j] += 1
                        elif dct_coeffs[i, j] < 0:
                            if dct_coeffs[i, j] % 2:
                                dct_coeffs[i, j] += 1
                            else:
                                dct_coeffs[i, j] -= 1
                    bit_index += 1
                    if progressBar is not None:
                        progressBar.setValue(int((bit_index / len(total_bits)) * 100))

    # 保存带有嵌入消息的JPEG图像
    jpeg.coef_arrays[0] = dct_coeffs
    written = jio.write(jpeg, output_path)
    if not written:
        raise FileError("隐写数据写入图像{}失败".format(output_path))
    else:
        print("水印嵌入成功")


# 文本提取函数
def extract_message(image_path, password=None, progressBar=None):
    # 读取JPEG图像并加载其DCT系数
    jpeg = jio.read(image_path)
    if jpeg.coef_arrays is None:
        raise FileError("无法访问图像文件{}".format(image_path))
    dct_coeffs = jpeg.coef_arrays[0]

    # 提取AC系数
    check_dct = get_ac_coeffs(dct_coeffs)

    # 提取消息
    message_bits = []
    for i in range(dct_coeffs.shape[0]):
        for j in range(dct_coeffs.shape[1]):
            if check_dct[i, j]:
                if dct_coeffs[i, j] not in (-1, 1, 0):
                    message_bits.append(dct_coeffs[i, j] % 2)

    # 提取水印头（32位）
    header_bits = message_bits[:32]
    message_length = int("".join(map(str, header_bits)), 2)

    # 提取实际的水印内容
    message_bits = message_bits[32 : 32 + message_length]
    # message = ""
    # for i in range(0, len(message_bits), 8):
    #     byte = message_bits[i : i + 8]
    #     byte_str = "".join([str(bit) for bit in byte])
    #     message += chr(int(byte_str, 2))
    #     if progressBar is not None:
    #         for j in range(i, i + 8):
    #             progressBar.setValue(int(j / message_length * 100))
    message = bits_to_bytes(message_bits)

    message_type = identify_file_type(message)
    if message_type != "application/octet-stream":
        raise FileWaterMarkError

    if password is not None:
        try:
            return encrypt_decrypt(message, password, "dec")
        except:
            raise PasswordError("密码无效！")

    return message


# 文件提取函数
def extract_file(image_path, password=None, progressBar=None):
    # 读取JPEG图像并加载其DCT系数
    jpeg = jio.read(image_path)
    if jpeg.coef_arrays is None:
        raise FileError("无法访问图像文件{}".format(image_path))
    dct_coeffs = jpeg.coef_arrays[0]

    # 提取AC系数
    check_dct = get_ac_coeffs(dct_coeffs)

    # 提取消息
    message_bits = []
    for i in range(dct_coeffs.shape[0]):
        for j in range(dct_coeffs.shape[1]):
            if check_dct[i, j]:
                if dct_coeffs[i, j] not in (-1, 1, 0):
                    message_bits.append(dct_coeffs[i, j] % 2)

    # 提取水印头（32位）
    header_bits = message_bits[:32]
    message_length = int("".join(map(str, header_bits)), 2)

    # 提取实际的水印内容
    message_bits = message_bits[32 : 32 + message_length]
    for i in range(message_length):
        progressBar.setValue(int((i / message_length) * 100))

    message = bits_to_bytes(message_bits)
    if password is not None:
        try:
            message = encrypt_decrypt_1(message, password, "dec")
        except:
            raise PasswordError("密码无效！")
    # write_binary_file(output_path, message)
    message_type = identify_file_type(message)

    return message_type, message


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())
