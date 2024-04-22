import numpy as np
import PIL.Image as Image
from utils.watermark import *


def ReadImg(src, path):
    src = np.array(Image.open(path))

    print("图像信息：")
    print(f"长：{src.shape[1]}\t宽：{src.shape[0]}\t通道数：{src.shape[2]}")


if __name__ == '__main__':
    jpeg_test_path = "./test.jpg"
    png_test_path = "./test.png"
    src = np.array(0)
    ReadImg(src, jpeg_test_path)
    ReadImg(src, png_test_path)

    len_wm1 = embedBlindWatermark(jpeg_test_path, "jpg_embed_test.jpg", "Hello World1")
    extractBlindWatermark("jpg_embed_test.jpg", len_wm1)

    len_wm2 = embedBlindWatermark(png_test_path, "png_embed_test.jpg", "Hello World2")
    extractBlindWatermark("png_embed_test.jpg", len_wm2)

