import cv2
import numpy as np
import glob
import os

class ProcessImage():
    def __init__(self):
        pass

    def remove_padding(self, data_path, ext):
        img_lst = glob.glob(os.path.join(data_path, "*." + ext))
        for img_file in img_lst:
            image = cv2.imread(img_file).astype(np.float32)
            dummy = np.argwhere(image > 50) # assume blackground is zero
            max_y = dummy[:, 0].max()
            min_y = dummy[:, 0].min()
            min_x = dummy[:, 1].min()
            max_x = dummy[:, 1].max()
            crop_image = image[min_y:max_y, min_x:max_x]
            cv2.imwrite(img_file, crop_image)