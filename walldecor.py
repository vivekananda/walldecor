#!/usr/bin/env python3
import os
import sys
import math
import papersize

from PIL import Image


class WallDecor:
    def __init__(self, file_path, min_sheets):
        self.file_path = file_path
        self.min_sheets = int(min_sheets)

    def make_files(self):
        if os.path.isfile(self.file_path):
            im = Image.open(self.file_path)

            (A4Width, A4Height) = papersize.parse_papersize("A4", "mm")
            (no_of_horizontal_sheets, no_of_vertical_sheets) = (1, 1)

            for no_of_horizontal_sheets in range(1, 10):
                zoom_factor = float(A4Width * no_of_horizontal_sheets) / float(im.width)
                no_of_vertical_sheets = int(math.ceil(im.height * zoom_factor / float(A4Height)))
                if no_of_horizontal_sheets * no_of_vertical_sheets >= self.min_sheets:
                    break
            new_size = [int(math.ceil(x * zoom_factor)) for x in (im.width, im.height)]
            new_img = im.resize(new_size)

            # import pdb;
            # pdb.set_trace()
            # make sheets
            tokens = self.file_path.split(".")
            for i in range(no_of_horizontal_sheets):
                for j in range(no_of_vertical_sheets):
                    box = [i * A4Width, j * A4Height, (i + 1) * A4Width, (j + 1) * A4Height]
                    region = new_img.crop(box)
                    new_file_name = "%s_%d_%d.%s" % (tokens[0],j, i,tokens[1])
                    region.convert('RGB').save(new_file_name)
                    pass

        else:
            print("file doesn't exist")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        wd = WallDecor(sys.argv[1], sys.argv[2])
        wd.make_files()

    else:
        print("Syntax: python walldecor.py <file path> <min number of a4 sheets>")
