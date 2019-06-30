import numpy as np


def shape_detect(pic_json):
    # Getting list of image file names
    imageURL_list = pic_json.get("image_locations")

    return imageURL_list
