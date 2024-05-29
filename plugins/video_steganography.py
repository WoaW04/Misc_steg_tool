import os
import sys
# import shutil
import random
import pyzipper
import subprocess
import string
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import struct
from datetime import datetime, timedelta
import argparse


def generate_random_filename(length=16):
    """生成指定长度的随机文件名, 不带扩展名"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def format_duration(seconds):
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}m:{seconds:02d}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours}h:{minutes:02d}m:{seconds:02d}s"

def get_video_duration(filepath):
    parser = createParser(filepath)
    if not parser:
        return None
    try:
        metadata = extractMetadata(parser)
        if not metadata:
            return None
        duration = metadata.get('duration')
        return int(duration.seconds) if duration else None
    finally:
        parser.stream._input.close()

def get_video_files_info(folder_path):
    videos = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp4"):
            filepath = os.path.join(folder_path, filename)
            duration_seconds = get_video_duration(filepath)
            if duration_seconds is None:
                formatted_duration = "Unknown"
            else:
                formatted_duration = format_duration(duration_seconds)
            size = os.path.getsize(filepath) / (1024 * 1024)  # Convert bytes to MB
            videos.append({
                "filename": filename,
                "duration": formatted_duration,
                "duration_seconds": duration_seconds or 0,  # Use 0 for unknown durations for sorting
                "size": size
            })
    # Sort the videos by duration in descending order
    videos.sort(key=lambda x: x['duration_seconds'], reverse=True)
    
    # Format for display
    formatted_videos = [f"{video['filename']} - {video['duration']} - {video['size']:.2f}MB" for video in videos]
    return formatted_videos

class Steganographier:
    '''隐写的具体功能由此类实现'''
    def __init__(self, video_folder_path=None):
        # nglog
        # self.mkvmerge_exe   = os.path.join(application_path,'tools','mkvmerge.exe')
        # self.mkvextract_exe = os.path.join(application_path,'tools','mkvextract.exe')
        # self.mkvinfo_exe    = os.path.join(application_path,'tools','mkvinfo.exe')
        # if video_folder_path:
        #     self.video_folder_path = video_folder_path
        # else:
        #     self.video_folder_path = os.path.join(application_path, "cover_video")  # 默认路径
        # print(f"外壳文件夹路径：{self.video_folder_path}")
        self.total_file_size = None
        self.password = None
        self.remaining_video_files = []
        self.progress_callback = None

    def initialize_video_files(self):
        """初始化剩余可用的外壳文件列表"""
        video_files = [f for f in os.listdir(self.video_folder_path) if f.endswith(".mp4")]
        random.shuffle(video_files)  # 随机排序
        self.remaining_video_files = video_files

    def set_progress_callback(self, callback): # GUI进度条回调
        self.progress_callback = callback

    def log(self, message): # CLI模式专属log方法
        print(message)

    def read_in_chunks(self, file_object, chunk_size=1024*1024):
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data

    def choose_cover_video_file(self, cover_video=None, processed_files=None, output_video_name_mode=None):
        # 外壳文件选择
        if cover_video:  # 如果指定了外壳文件名就使用之（CLI模式）绝对路径
            return cover_video

        # 1. 检查cover_video中是否存在用来作为外壳的MP4文件（比如海绵宝宝之类，数量任意，每次随机选择）
        video_files = [f for f in os.listdir(self.video_folder_path) if f.endswith(".mp4")]  # 按默认排序选择
        if not video_files:
            raise Exception(f"{self.video_folder_path} 文件夹下没有文件，请添加文件后继续.")

        # 2. 否则在cover_video中选择
        if output_video_name_mode == '===============随机选择模式===============':
            # 2-a. 随机选择一个外壳MP4文件用来隐写，尽量不重复
            if not self.remaining_video_files:
                self.initialize_video_files()
            video_file = self.remaining_video_files.pop()

        elif output_video_name_mode == '===============时长顺序模式===============':
            # 2-b. 按时长顺序选择一个外壳MP4文件用来隐写
            video_files = get_video_files_info(self.video_folder_path)  # 按时长顺序选择
            video_file = video_files[processed_files % len(video_files)]

        elif output_video_name_mode == '===============名称顺序模式===============':
            # 2-c. 按名称顺序选择一个外壳MP4文件用来隐写
            video_file = video_files[processed_files % len(video_files)]

        else:
            # 2-d. 根据下拉菜单选择外壳MP4文件
            video_file = output_video_name_mode

        self.cover_video_file = video_file[:video_file.rfind('.mp4')] + '.mp4'  # 按最后一个.mp4切分
        cover_video_path = os.path.join(self.video_folder_path, self.cover_video_file)
        return cover_video_path
    
    def compress_files(self, zip_file_path, input_file_path, processed_size=0, password=None):
        # 6.1 选择是否使用加密
        if password:
            # 使用密码加密
            zip_file = pyzipper.AESZipFile(zip_file_path, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES)
            zip_file.setpassword(password.encode())
        else:
            # 不使用加密
            zip_file = pyzipper.ZipFile(zip_file_path, 'w', compression=pyzipper.ZIP_DEFLATED)
        
        # 6.2 压缩zip文件
        with zip_file:
            self.log(f"Compressing file 6.2: {input_file_path}")
            
            # 假如被隐写的文件是一个文件夹
            if os.path.isdir(input_file_path):
                # 定义总的顶层文件夹名为原文件夹的名字
                root_folder = os.path.basename(input_file_path)
                # 然后隐写其下所有文件
                for root, dirs, files in os.walk(input_file_path):
                    for file in files:
                        file_full_path = os.path.join(root, file)
                        # 在原有的相对路径前加上顶层文件夹名
                        arcname = os.path.join(root_folder, os.path.relpath(file_full_path, start=input_file_path))
                        zip_file.write(file_full_path, arcname)
                        
                        # 更新已处理的大小并更新进度条
                        processed_size += os.path.getsize(file_full_path)
                        if self.progress_callback:
                            self.progress_callback(processed_size, self.total_file_size)
            else:
                # 否则只隐写该文件
                zip_file.write(input_file_path, os.path.basename(input_file_path))
                # 更新已处理的大小并更新进度条
                processed_size = os.path.getsize(input_file_path)
                if self.progress_callback:
                    self.progress_callback(processed_size, self.total_file_size)

    def get_output_file_path(self, input_file_path=None, output_file_path=None, processed_files=0, output_option=None, output_video_name_mode=None):

        # 输出文件名指定
        if output_file_path:
            return output_file_path # 如果指定了输出文件名就用输出文件名（CLI模式）

        print(f'type option: {self.type_option}')
        if self.type_option == 'mp4':

            # 输出文件名选择
            if self.output_option == '原文件名':
                output_file_path = os.path.splitext(input_file_path)[0] + f"_hidden_{processed_files+1}.mp4"
            elif self.output_option == '外壳文件名':
                output_file_path = os.path.join(os.path.split(input_file_path)[0], 
                                        os.path.splitext(self.cover_video_file)[0] + f'_{processed_files+1}.mp4')
            elif self.output_option == '随机文件名':
                output_file_path = os.path.join(os.path.split(input_file_path)[0], 
                                        generate_random_filename(length=16) + f'_{processed_files+1}.mp4')
            print(f"output_file_path: {output_file_path}")    
        elif self.type_option == 'mkv':

            # 输出文件名选择
            if self.output_option == '原文件名':
                output_file_path = os.path.splitext(input_file_path)[0] + f"_hidden_{processed_files+1}.mkv"
            elif self.output_option == '外壳文件名':
                output_file_path = os.path.join(os.path.split(input_file_path)[0], 
                                        os.path.splitext(self.cover_video_file)[0] + f'_{processed_files+1}.mkv')          
            elif self.output_option == '随机文件名':
                output_file_path = os.path.join(os.path.split(input_file_path)[0], 
                                        generate_random_filename(length=16) + f'_{processed_files+1}.mkv')    
        
        return output_file_path

    # 隐写方法实现部分
    def hide_file(self, input_file_path, 
                  coverVideoPath=None, 
                  password=None, 
                  processed_files=0, 
                  output_file_path=None, 
                  output_option=None, 
                  output_video_name_mode=None,
                  type_option=None):

        self.type_option                = type_option
        self.output_option              = output_option
        self.output_video_name_mode     = output_video_name_mode
        self.password                   = password

        # 1~2. 隐写外壳文件选择
        # cover_video_path = self.choose_cover_video_file(cover_video=cover_video, processed_files=processed_files, output_video_name_mode=output_video_name_mode)
        # print(f"实际隐写外壳文件：{cover_video_path}")
                
        # 3. 隐写的临时zip文件名
        zip_file_path = os.path.join(os.path.splitext(input_file_path)[0] + f"_hidden_{processed_files}.zip")
        
        # 4. 计算要压缩的文件总大小
        # nglog
        # self.total_file_size = 0
        # if os.path.isdir(input_file_path):
        #     for root, dirs, files in os.walk(input_file_path):
        #         for file in files:
        #             file_full_path = os.path.join(root, file)
        #             self.total_file_size += os.path.getsize(file_full_path)
        # else:
        self.total_file_size = os.path.getsize(input_file_path)
            
        processed_size = 0 # 初始化已处理的大小为0
        self.compress_files(zip_file_path, input_file_path, processed_size=processed_size, password=password)    # 创建隐写的临时zip文件

        try:        
            # 7.1. 隐写MP4文件的逻辑
            if type_option == 'mp4':
                output_file = output_file_path + '/' + input_file_path.split('/')[-1].split('.')[0] + "_hidden.mp4"
                # output_file = self.get_output_file_path(input_file_path, output_file_path, processed_files, self.output_option, self.output_video_name_mode)

                self.log(f"Output file: {output_file}")
            
                try:
                    total_size_hidden = os.path.getsize(coverVideoPath) + os.path.getsize(zip_file_path)
                    processed_size = 0
                    with open(coverVideoPath, "rb") as file1:
                        with open(zip_file_path, "rb") as file2:
                            with open(output_file, "wb") as output:
                                self.log(f"Hiding file: {input_file_path}")

                                # 外壳 MP4 文件
                                for chunk in self.read_in_chunks(file1):
                                    output.write(chunk)
                                    processed_size += len(chunk)
                                    if self.progress_callback:
                                        self.progress_callback(processed_size, total_size_hidden)

                                # 压缩包 zip 文件
                                for chunk in self.read_in_chunks(file2):
                                    output.write(chunk)
                                    processed_size += len(chunk)
                                    if self.progress_callback:
                                        self.progress_callback(processed_size, total_size_hidden)

                                # nglog
                                # # 随机写入 2 种压缩文件特征码，用来混淆网盘的检测系统
                                # head_signatures = {
                                #     "RAR4": b'\x52\x61\x72\x21\x1A\x07\x00',
                                #     "RAR5": b'\x52\x61\x72\x21\x1A\x07\x01\x00',
                                #     "7Z": b'\x37\x7A\xBC\xAF\x27\x1C',
                                #     "ZIP": b'\x50\x4B\x03\x04',
                                #     "GZIP": b'\x1F\x8B',
                                #     "BZIP2": b'\x42\x5A\x68',
                                #     "XZ": b'\xFD\x37\x7A\x58\x5A\x00',
                                # }

                                # # 添加随机压缩文件特征码
                                # random_bytes = os.urandom(1024 * random.randint(20, 25))  # 10KB - 25KB 的随机字节
                                # output.write(random.choice(list(head_signatures.values())))  # 随机压缩文件特征码
                                # output.write(random_bytes)

                                # output.write(random.choice(list(head_signatures.values())))  # 第二个压缩文件特征码
                                # random_bytes = os.urandom(1024 * random.randint(20, 25))  # 10KB - 25KB 的随机字节
                                # output.write(random_bytes)

                                # 构造一个随机的 moov box
                                def construct_random_moov_box():
                                    # 生成随机的 32 位整数。
                                    def generate_random_uint32():
                                        return random.randint(0, 0xFFFFFFFF)

                                    # 随机生成时间戳（1970 年后）
                                    def generate_random_timestamp():
                                        epoch = datetime(1970, 1, 1)
                                        random_date = epoch + timedelta(seconds=random.randint(0, int((datetime.now() - epoch).total_seconds())))
                                        return int(random_date.timestamp())

                                    # 随机生成矩阵（3x3 矩阵）
                                    def generate_random_matrix():
                                        return struct.pack(">9I",
                                                        0x00010000, 0, 0,  # 第一行
                                                        0, 0x00010000, 0,  # 第二行
                                                        0, 0, 0x40000000)  # 第三行
                                    moov_box_header = b'\x00\x00\x00\x6C\x6D\x6F\x6F\x76'  # moov header
                                    mvhd_box_header = b'\x00\x00\x00\x6C\x6D\x76\x68\x64'  # mvhd header

                                    mvhd_box = (
                                        mvhd_box_header +  # mvhd header
                                        b'\x00\x00\x00\x00' +  # version and flags
                                        struct.pack(">I", generate_random_timestamp()) +  # creation time
                                        struct.pack(">I", generate_random_timestamp()) +  # modification time
                                        struct.pack(">I", 1000) +  # timescale
                                        struct.pack(">I", random.randint(10000, 60000)) +  # duration
                                        struct.pack(">I", 0x00010000) +  # rate (1.0)
                                        struct.pack(">H", 0x0100) +  # volume (1.0)
                                        b'\x00\x00' +  # reserved
                                        struct.pack(">Q", generate_random_uint32()) +  # reserved
                                        generate_random_matrix() +  # matrix
                                        b'\x00\x00\x00\x00\x00\x00\x00\x00' +  # pre-defined
                                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' +  # pre-defined
                                        struct.pack(">I", generate_random_uint32())  # next track ID
                                    )

                                    moov_box = moov_box_header + mvhd_box
                                    return moov_box

                                # 将随机的 moov box 附加到文件末尾
                                moov_box = construct_random_moov_box()
                                output.write(moov_box)
                
                except Exception as e:
                    self.log(f"在写入MP4文件时发生未预料的错误: {str(e)}")
                    raise

            # 7.2. 隐写mkv文件的逻辑
            elif type_option == 'mkv':
                output_file = self.get_output_file_path(input_file_path, output_file_path, processed_files, self.output_option, self.output_video_name_mode)
                
                # 生成末尾随机字节
                random_data_path = f"temp_{generate_random_filename(length=16)}"
                try:
                    with open(random_data_path, "wb") as f:
                        random_bytes = os.urandom(1024*8)  # 8kb
                        f.write(random_bytes)

                    self.log(f"Output file: {output_file}")
                    cmd = [
                        self.mkvmerge_exe, '-o',
                        output_file, cover_video_path,
                        '--attach-file', zip_file_path,
                        '--attach-file', random_data_path,
                    ]
                    self.log(f"Hiding file: {input_file_path}")
                    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
                    
                    # 删除临时随机字节
                    os.remove(random_data_path)

                    if result.returncode != 0:
                        raise subprocess.CalledProcessError(result.returncode, cmd, output=result.stdout, stderr=result.stderr)

                except subprocess.CalledProcessError as cpe:
                    self.log(f"隐写时发生错误: {str(cpe)}")
                    self.log(f'CalledProcessError output：{cpe.output}') if cpe.output else None
                    self.log(f'CalledProcessError stderr：{cpe.stderr}') if cpe.stderr else None
                    raise

                except Exception as e:
                    self.log(f"在执行mkvmerge时发生未预料的错误: {str(e)}")
                    raise

        except Exception as e:
            self.log(f"隐写时发生未预料的错误: {str(e)}")
            raise
        finally:
            # 8. 删除临时zip文件
            os.remove(zip_file_path)

        self.log(f"Output file created: {os.path.exists(output_file)}")
    
    
    # 解除隐写的方法     
    def reveal_file(self, input_file_path, password=None, type_option=None):

        self.type_option = type_option
        
        # 解除MP4隐写的逻辑
        if self.type_option == 'mp4':
            try:
                # 读取文件数据
                self.log(f"Revealing file: {input_file_path}")
                with open(input_file_path, "rb") as file:
                    file_data = file.read()

                # 计算ZIP数据起始位置
                zip_start_pos = len(file_data) - os.path.getsize(input_file_path)
                zip_data = file_data[zip_start_pos:]

                # 将ZIP文件写入硬盘
                zip_path = os.path.splitext(input_file_path)[0] + "_extracted.zip"
                with open(zip_path, "wb") as file:
                    file.write(zip_data)

                self.log(f"Extracted ZIP file: {zip_path}")

                # 根据是否有密码选择解压方式
                if password:
                    # 使用密码解压ZIP文件
                    with pyzipper.AESZipFile(zip_path) as zip_file:
                        zip_file.setpassword(password.encode())
                        zip_file.extractall(os.path.dirname(zip_path))
                else:
                    # 无密码解压ZIP文件
                    with pyzipper.ZipFile(zip_path, 'r') as zip_file:
                        zip_file.extractall(os.path.dirname(zip_path))

                # 删除ZIP文件
                os.remove(zip_path)

                self.log(f"File extracted successfully: {not os.path.exists(zip_path)}")

            except (pyzipper.BadZipFile, ValueError) as e:
                # 处理ZIP文件损坏或密码错误的情况
                if os.path.exists(zip_path):
                    os.remove(zip_path)
                self.log(f"无法解压文件 {input_file_path}，可能是密码错误或文件损坏: {str(e)}")
            except Exception as e:
                # 处理其他异常
                if os.path.exists(zip_path):
                    os.remove(zip_path)
                self.log(f"解压时发生错误: {str(e)}")
        
        # 解除mkv文件隐写的逻辑
        elif self.type_option == 'mkv':
            # 获取mkv附件id函数
            def get_attachment_name(input_file_path):
                cmd = [self.mkvinfo_exe, input_file_path]
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
                    lines = result.stdout.splitlines()
                    for idx, line in enumerate(lines):
                        if "MIME" in line:
                            parts = lines[idx-1].split(':')
                            attachments_name = parts[1].strip().split()[-1] # 附件的实际名称
                            break                                           # 只要第一个附件
                except Exception as e:
                    self.log(f"获取附件时出错: {e}")
                
                return attachments_name
            
            # 提取mkv附件
            def extract_attachment(input_file_path, output_path):
                cmd = [
                    self.mkvextract_exe, 'attachments',
                    input_file_path,
                    f'1:{output_path}'
                ]
                try:
                    subprocess.run(cmd, check=True)
                except subprocess.CalledProcessError as e:
                    raise Exception(f"提取附件时出错: {e}")   
                    
            # 获取附件文件名
            attachments_name = get_attachment_name(input_file_path)
            if attachments_name:
                output_path = os.path.join(os.path.dirname(input_file_path), attachments_name)
                self.log(f"Mkvextracting attachment file: {output_path}")
                # 提取附件
                try:
                    extract_attachment(input_file_path, output_path)

                    # 使用密码解压ZIP文件
                    if attachments_name.endswith('.zip'):
                        try:
                            zip_path = output_path
                            self.log(f"Extracting ZIP file: {zip_path}")
                            with pyzipper.AESZipFile(zip_path, 'r', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zip_file:
                                zip_file.extractall(os.path.dirname(input_file_path), pwd=password.encode())
                            
                            # 解压后删除ZIP文件
                            os.remove(zip_path)
                    
                        except RuntimeError as e:
                            # 这里处理密码错误的情况
                            self.log(f"解压失败，错误信息: {e}")

                    # 解压后删除隐写MP4文件
                    os.remove(input_file_path)
                    
                    self.log(f"提取附件 {attachments_name} 成功")
                except subprocess.CalledProcessError as e:
                    self.log(f"提取附件 {attachments_name} 时出错: {e}")

            else:
                self.log("该 MKV 文件中没有可提取的附件。")

    def run_cli(self, args):
        # self.type_option_var = argparse.Namespace()
        # self.type_option_var.get = lambda: args.type # 模拟.get() 方法

        print(f"输入文件/文件夹路径: {args.input}")
        print(f"输出文件/文件夹路径: {args.output}")
        print(f"密码: {args.password}")
        print(f"输出文件类型: {args.type}")
        print(f"设定外壳MP4视频路径: {args.cover}")
        print(f"执行解除隐写: {args.reveal}")

        self.type_option = args.type
        
        if not args.reveal:
            if args.output:
                output_file = args.output
            else:
                input_file_name = os.path.splitext(os.path.basename(args.input))[0]
                output_file = f"{input_file_name}_hidden.{args.type}"
            
            self.hide_file(input_file_path=args.input, cover_video=args.cover, password=args.password, output_file_path=output_file, type_option=self.type_option)  # 调用hide_file方法
        else:
            self.reveal_file(input_file_path=args.input, password=args.password, type_option=self.type_option)  # 调用reveal_file方法


def testReveal():
    inputFilePath = "C:/Users/user/Desktop/testt/video_steg_test/test_hidden.mp4"
    password = "1234" 
    typeOption = "mp4"
    steganographier = Steganographier()

    steganographier.reveal_file(input_file_path=inputFilePath, password=password, type_option=typeOption)

def testHide():
    inputFilePath = "C:/Users/user/Desktop/testt/video_steg_test/test.js"
    coverVideoPath = "C:/Users/user/Desktop/testt/video_steg_test/cover.mp4"
    password = "1234" 
    outputPath = "C:/Users/user/Desktop/testt/video_steg_test"
    typeOption = "mp4"


    steganographier = Steganographier()
    steganographier.hide_file(input_file_path=inputFilePath, coverVideoPath=coverVideoPath, password=password, output_file_path=outputPath, type_option=typeOption)

if __name__ == "__main__":
    # testHide()
    testReveal()

    exit()
    # 关于程序执行路径的问题
    if getattr(sys, 'frozen', False):  # 打包成exe的情况
        application_path = os.path.dirname(sys.executable)
    else:  # 在开发环境中运行
        application_path = os.path.dirname(__file__)

    parser = argparse.ArgumentParser(description='隐写者 Ver.1.1.1 CLI 作者: 层林尽染')
    parser.add_argument('-i', '--input', default=None, help='指定输入文件或文件夹的路径')
    parser.add_argument('-o', '--output', default=None, help='1.指定输出文件名(包含后缀名) [或] 2.输出文件夹路径(默认为原文件名+"hidden")')
    parser.add_argument('-p', '--password', default='', help='设置密码 (默认无密码)')
    parser.add_argument('-t', '--type', default='mp4', choices=['mp4', 'mkv'], help='设置输出文件类型 (默认为mp4)')
    parser.add_argument('-c', '--cover', default=None, help='指定外壳MP4视频（默认在程序同路径下搜索）')
    parser.add_argument('-r', '--reveal', action='store_true', help='执行解除隐写')

    args, unknown = parser.parse_known_args()

    if unknown: # 假如没有指定参数标签，那么默认第一个传入为 -i 参数
        args.input = unknown[0]

    if args.input:
        print('CLI')
        # 首先调整传入的参数
        # 1. 处理输出路径
        if args.output is None:
            # 1.1 如果没有指定输出文件路径, 则默认和输入文件同路径, 使用原文件名+"_hidden.mp4/mkv"
            input_dir = os.path.dirname(os.path.abspath(args.input))
            args.output = os.path.join(input_dir, f"{os.path.splitext(os.path.basename(args.input))[0]}_hidden.{args.type}")
        else:
            # 1.2. 如果指定了输出路径但不包含文件名, 仍使用原文件名+"_hidden.mp4/mkv"
            if os.path.splitext(args.output)[1] == '':
                input_filename = os.path.splitext(os.path.basename(args.input))[0]
                args.output = f"{os.path.join(args.output, input_filename)}_hidden.{args.type}"
            # 1.3. 其余情况则使用指定的输出文件名
            else:
                args.output = args.output

        # 2. 处理外壳MP4文件
        if args.cover is None:
            mp4list = []
            # 2.1 如果没有指定外壳视频路径, 则自动在程序同路径下的 cover_video 文件夹中寻找第一个文件
            cover_video_path = os.path.join(application_path, 'cover_video')
            if os.path.exists(cover_video_path):
                mp4list = [os.path.join(cover_video_path, item) for item in os.listdir(cover_video_path) if item.endswith('.mp4')]
            
            # 2.2 否则使用程序所在目录中的第一个mp4文件
            mp4list += [os.path.join(application_path, item) for item in os.listdir(application_path) if item.endswith('.mp4')]  # 程序所在目录
            
            # 2.3 假如以上都没找到,那么就在输入文件/目录所在目录下寻找
            if not mp4list:
                input_dir = os.path.dirname(os.path.abspath(args.input)) # 获取输入文件/文件夹的父目录
                mp4list += [os.path.join(input_dir, item) for item in os.listdir(input_dir) if item.endswith('.mp4')]  # 输入文件/目录所在目录

            if mp4list:
                args.cover = mp4list[0]
            else:
                print('请指定外壳MP4文件')
                exit(1)  # 退出程序

        steganographier = Steganographier()
        steganographier.run_cli(args)

