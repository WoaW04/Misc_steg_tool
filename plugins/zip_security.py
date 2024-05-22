
class ZipFakeEncrypt:
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
        # 奇數, 打開時會要求輸入密碼, 以此實現偽加密
        ZipFakeEncrypt.modify(zipPath, outputPath, b'\x05')
    @staticmethod
    def decrypt(zipPath, outputPath):
        ZipFakeEncrypt.modify(zipPath, outputPath, b'\x00')

if __name__ == "__main__":
    inputPath = r"C:\Users\user\Desktop\todoooo.zip"
    outputPath = r"C:\Users\user\Desktop\A\github\Img_steg_tool"
    ZipFakeEncrypt.encrypt(inputPath, outputPath)
    ZipFakeEncrypt.decrypt(outputPath + '\\' + 'todoooo_enc.zip', outputPath)
    