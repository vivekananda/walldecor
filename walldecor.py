#!/usr/bin/env python3
import os
import sys
import math
import papersize

from PIL import Image


class WallDecor:
    max_horizontal_sheets = 10

    def __init__(self, file_path, min_sheets):
        self.file_path = file_path
        self.min_sheets = int(min_sheets)

    def make_files(self):
        if not os.path.isfile(self.file_path):
            print("please check the file path and try again")
            return

        (a4_height, a4_width) = papersize.parse_papersize("A4", "mm")
        zoom_factor = 1
        no_of_horizontal_sheets = 1
        no_of_vertical_sheets = 1

        with Image.open(self.file_path) as im:
            for no_of_horizontal_sheets in range(1, self.max_horizontal_sheets):
                zoom_factor = float(a4_width * no_of_horizontal_sheets) / float(im.width)
                no_of_vertical_sheets = int(math.ceil(im.height * zoom_factor / float(a4_height)))
                if no_of_horizontal_sheets * no_of_vertical_sheets >= self.min_sheets:
                    break
            new_img = self.__scale_image(im, zoom_factor)

            # make sheets
            (prefix, extension) = self.file_path.split(".")
            for i in range(no_of_horizontal_sheets):
                for j in range(no_of_vertical_sheets):
                    self.__save_a4_image(new_img, i, j, prefix, extension)
        print(f"Created {no_of_horizontal_sheets * no_of_vertical_sheets} files in same directory as {self.file_path}")

    @staticmethod
    def __scale_image(im, zoom_factor):
        new_size = [int(math.ceil(im.width * zoom_factor)), int(math.ceil(im.height * zoom_factor))]
        return im.resize(new_size)

    @staticmethod
    def __save_a4_image(new_img, i, j, prefix, extension):
        (a4_height, a4_width) = papersize.parse_papersize("A4", "mm")
        box = [i * a4_width, j * a4_height, (i + 1) * a4_width, (j + 1) * a4_height]
        region = new_img.crop(box)
        new_file_name = "%s_%d_%d.%s" % (prefix, j, i, extension)
        region.convert('RGB').save(new_file_name)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        wd = WallDecor(sys.argv[1], sys.argv[2])
        wd.make_files()

    else:
        print("Syntax: python walldecor.py <file path> <min number of a4 sheets>")
