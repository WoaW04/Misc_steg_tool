import os
from struct import pack, unpack

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
        outputFilePath = outputDir + '\\' + origZipPath.split('\\')[-1].split('.')[0] + "_zipsteg.zip"

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
        outputFilePath = outputDir + '\\' + filePath.split('\\')[-1].split('.')[0] + "_extract"

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
        zipName = zipPath.split("\\")[-1].split(".")[0]
        with open(zipPath, mode = 'rb') as f:
            data = f.read()
            data = bytearray(data)

            dirEntryIndex = data.find(b'\x50\x4B\x01\x02')
            if dirEntryIndex == -1:
                raise IndexError("[zip偽加密失敗] 指定zip文件可能有問題")

            data[dirEntryIndex + 8 : dirEntryIndex + 9] = modifyByte

        if modifyByte == b'\x05':
            output = f"{outputPath}/{zipName}_enc.zip"
        else:
            output = f"{outputPath}/{zipName}_dec.zip"


        with open(output, mode = 'wb') as f:
            f.write(data)
    
    @staticmethod
    def encrypt(zipPath, outputPath):
        ZipFakeEncrypt.modify(zipPath, outputPath, b'\x05')
    @staticmethod
    def decrypt(zipPath, outputPath):
        ZipFakeEncrypt.modify(zipPath, outputPath, b'\x00')



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
    