from blind_watermark import WaterMark

# 文檔: https://github.com/guofei9987/blind_watermark/blob/master/README_cn.md

# 嵌入盲水印


def embedBlindWatermark(originImgPath: str, outputPath: str, embedMsg: str):

    bwm1 = WaterMark(password_img=1, password_wm=1)
    bwm1.read_img(originImgPath)
    bwm1.read_wm(embedMsg, mode='str')
    bwm1.embed(outputPath)
    len_wm = len(bwm1.wm_bit)
    print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))
    return len_wm

# 提取盲水印


def extractBlindWatermark(imgPath: str, len_wm: int):
    bwm1 = WaterMark(password_img=1, password_wm=1)
    wm_extract = bwm1.extract(imgPath, wm_shape=len_wm, mode='str')
    print(f"從{imgPath}提取的盲水印信息: {wm_extract}")
    return wm_extract


len_wm = embedBlindWatermark("./test.jpg",
                             "./test_embed.png", "@guofei9987 开源万岁！")
extractBlindWatermark("./test_embed.png", len_wm)
