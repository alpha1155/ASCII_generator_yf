"""
@author: Viet Nguyen <nhviet1009@gmail.com>
python .\img2img_color_api.py --input .\data\jinx.png --background white  --num_cols 1100 --language chinese --output .\data\jinx_Ascii.jpg
"""
import argparse
from ast import Param

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from utils import get_data


def getImg(imgParam):
    if imgParam['background'] == "white":
        bg_code = (255, 255, 255)
    else:
        bg_code = (0, 0, 0)
    char_list, font, sample_character, scale = get_data(
        imgParam['language'], imgParam['mode'])
    num_chars = len(char_list)
    num_cols = imgParam['num_cols']
    image = cv2.imread(imgParam['input'], cv2.IMREAD_COLOR)
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
    out_image.save(imgParam['output'])


if __name__ == '__main__':
    imgParam = {"input": ".\\data\\jinx.png",
                "output": ".\\data\\jinx_Ascii.jpg",
                'language': 'chinese',
                "mode": "standard",
                "background": "white",
                "num_cols": 1100,
                "scale": 2}

    print(imgParam)
    getImg(imgParam)
