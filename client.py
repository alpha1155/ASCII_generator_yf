# import requests

# res = requests.get(
#     "https://gchat.qpic.cn/gchatpic_new/2931470156/736599314-3070512006-9975D3B5EEF8B2F067D27D6340D2F77D/0?term=3,subType=0")
# print(dir(res))
# print(res.content)

import os
import cv2
import datetime
import numpy as np
from utils import get_data
from urllib import request
from PIL import Image, ImageDraw, ImageOps


def getImg(imgParam):
    if imgParam['background'] == "white":
        bg_code = (255, 255, 255)
    else:
        bg_code = (0, 0, 0)
    char_list, font, sample_character, scale = get_data(
        imgParam['language'], imgParam['mode'])
    num_chars = len(char_list)
    num_cols = imgParam['num_cols']
    # image = cv2.imread(imgParam['input'], cv2.IMREAD_COLOR)
    url = imgParam['img_url']
    resp = request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width, _ = image.shape
    cell_width = width / imgParam['num_cols']
    cell_height = scale * cell_width
    num_rows = int(height / cell_height)
    if num_cols > width or num_rows > height:
        print("Too many columns or rows. Use default setting")
        cell_width = 6
        cell_height = 12
        num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)
    char_width, char_height = font.getsize(sample_character)
    out_width = char_width * num_cols
    out_height = scale * char_height * num_rows
    out_image = Image.new("RGB", (out_width, out_height), bg_code)
    draw = ImageDraw.Draw(out_image)
    for i in range(num_rows):
        for j in range(num_cols):
            partial_image = image[int(i * cell_height):min(int((i + 1) * cell_height), height),
                                  int(j * cell_width):min(int((j + 1) * cell_width), width), :]
            partial_avg_color = np.sum(
                np.sum(partial_image, axis=0), axis=0) / (cell_height * cell_width)
            partial_avg_color = tuple(
                partial_avg_color.astype(np.int32).tolist())
            char = char_list[min(
                int(np.mean(partial_image) * num_chars / 255), num_chars - 1)]
            draw.text((j * char_width, i * char_height),
                      char, fill=partial_avg_color, font=font)

    if imgParam['background'] == "white":
        cropped_image = ImageOps.invert(out_image).getbbox()
    else:
        cropped_image = out_image.getbbox()
    out_image = out_image.crop(cropped_image)
    out_image.save(os.path.split(os.path.realpath(__file__))
                   [0]+'\\data\\' + imgParam['output'])


if __name__ == '__main__':
    imgParam = {
        "img_url": 'https://c2cpicdw.qpic.cn/offpic_new/0/2931470156-1644525957-E9DC8C8A20E03758A1A37C5830C6625B/0?term=3',
        "output": "testRemote0.jpg",
        'language': 'chinese',
        "mode": "standard",
        "background": "white",
        "num_cols": 300,
        "scale": 2}

    # print(os.path.realpath(__file__))
    # print(os.path.split(os.path.realpath(__file__))[0])
    # print(imgParam)
    # print(os.path.split(os.path.realpath(__file__))[0])
    getImg(imgParam)
# now_time = datetime.datetime.now()
# print(now_time)
