from PIL import Image
import os
import json


def crack(filenamee):

    image = Image.open(filenamee).convert('L')
    pixel_matrix = image.load()

    for col in range(0, image.height):
        for row in range(0, image.width):
            if pixel_matrix[row, col] > 135:
                pixel_matrix[row, col] = 255


    for column in range(1, image.height - 1):
        for row in range(1, image.width - 1):
            if pixel_matrix[row, column] >= 0 and pixel_matrix[row, column - 1] == 255 and pixel_matrix[row, column + 1] == 255:
                pixel_matrix[row, column] = 255
            if pixel_matrix[row, column] >= 0 and pixel_matrix[row - 1, column] == 255 and pixel_matrix[row + 1, column] == 255:
                pixel_matrix[row, column] = 255

    for col in range(0, image.height):
        for row in range(0, image.width):
            if pixel_matrix[row, col] != 255:
                pixel_matrix[row, col] = 0



    characters = "23456789abcdefghijkmnopqrstuvwxyz"
    captcha = ""
    with open("bitmaps.json", "r") as fin:
        bitmap = json.load(fin)

    for j in range(35, 151, 20):
        char_img = image.crop((j-20, 12, j, 44))
        char_matrix = char_img.load()
        matches = {}
        for char in characters:
            match = 0
            black = 0
            bitmap_matrix = bitmap[char]
            for col in range(0, 32):
                for row in range(0, 20):
                    if char_matrix[row, col] == bitmap_matrix[col][row] and bitmap_matrix[col][row] == 0:
                        match += 1
                    if bitmap_matrix[col][row] == 0:
                        black += 1
            perc = float(match) / float(black)
            matches.update({perc: char[0]})
        try:
            captcha += matches[max(matches.keys())]
        except ValueError:
            print("failed captcha")
            captcha += "0"
    return captcha

for root, dirs, files in os.walk("captcha_image"):
    for name in files:
        print(name + " : " + crack("captcha_image/" + str(name)))

