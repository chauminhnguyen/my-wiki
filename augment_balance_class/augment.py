import glob
import json
import os
import imgaug.augmenters as iaa
from tqdm import tqdm
import cv2
from shutil import copyfile
import math
import numpy as np

class Dataset:
    def __init__(self, data_path):
        self.data_path = data_path
        self.get_data_lst()

    def get_data_lst(self):
        img_lst = glob.glob(self.data_path + '\*.jpg')
        self.data_lst = []
        self.class_clust = {}
        for index, img_name in enumerate(img_lst):
            gt_name = img_name + '.json'
            class_name = json.load(fp=open(gt_name))['classId'][0]
            if class_name not in self.class_clust:
                self.class_clust[class_name] = []
            self.class_clust[class_name].append((img_name, gt_name))
            self.data_lst.append((img_name, gt_name))
    
    def get_class_count(self):
        class_count = {}
        for class_name in self.class_clust:
            class_count[class_name] = len(self.class_clust[class_name])
        return class_count
    
    def get_samples_by_cls(self, class_name):
        return self.class_clust[class_name]
    
    def add_sample(self, img_name, gt_name):
        class_name = json.load(fp=open(gt_name))['classId'][0]
        self.data_lst.append((img_name, gt_name))
        if class_name not in self.class_clust:
            self.class_clust[class_name] = []
        self.class_clust[class_name].append((img_name, gt_name))
        
    def __getitem__(self, index):
        img_name, gt_name, class_name = self.data_lst[index]
        img = cv2.imread(img_name)
        gt = json.load(fp=open(gt_name))
        return img_name, img, gt


class Augmentation:
    def __init__(self):
        self.basic_augment = self.load_basic_augment()
        self.noisy_augment = self.load_noisy_augment()
    
    def load_basic_augment(self):
        return \
        {
            'hor':  iaa.Flipud(1.0),
            'ver':  iaa.Fliplr(1.0),
            '90':   iaa.Rotate(90),
            '180':  iaa.Rotate(180)
        }

    def load_noisy_augment(self):
        return \
        {'noise':
                iaa.SomeOf(2,[
                iaa.GammaContrast((0.5, 2.0)),
                iaa.SigmoidContrast(gain=(3, 10), cutoff=(0.4, 0.6)),
                iaa.AverageBlur(k=((5, 11))),
                iaa.Add((-40, 40)),
                iaa.Multiply((0.5, 1.5))
            ])
        }
    
    def number_of_basic_aug(self):
        return len(self.basic_augment)
    
    def number_of_noisy_aug(self):
        return len(self.noisy_augment)
    
    def save_aug_image(self, img, img_path, aug_path, aug_type):
        it = 0
        img_name, ext = os.path.splitext(img_path)
        img_aug_path = os.path.join(aug_path, os.path.basename(img_name) + '_' + aug_type + ext)
        while os.path.exists(img_aug_path):
            it += 1
            img_aug_path = os.path.join(aug_path, os.path.basename(img_name) + '_' + aug_type + '_' + str(it) + ext)
        cv2.imwrite(img_aug_path, img)
        copyfile(img_path + '.json', img_aug_path + '.json')
        return img_aug_path
    
    def augment_noisy_data(self, data_lst, aug_path, aug_num):
        img_name_aug_arr = []

        idx_data_lst = np.arange(len(data_lst))
        idx_data_lst = np.random.choice(idx_data_lst, aug_num)
        for index in tqdm(idx_data_lst):
            it = 0
            img_path, _ = data_lst[index]
            img = cv2.imread(img_path)
            img_aug = self.noisy_augment['noise'].augment_image(img)
            img_aug_path = self.save_aug_image(img_aug, img_path, aug_path, "noise")
            img_name_aug_arr.append(img_aug_path)
        return img_name_aug_arr
    
    def augment_basic_data(self, data_lst, aug_path, aug_num):
        img_name_aug_arr = []
        
        aug_len = math.ceil(aug_num / len(data_lst))
        
        if aug_len == 0:
            raise ValueError('data_lst cannot be empty')
        if aug_len > self.number_of_basic_aug():
            print('WARNING: aug_num is too large')
            aug_lst = np.random.choice(list(self.basic_augment.keys()), aug_len)
        else:
            aug_lst = self.basic_augment.keys()
        aug_i = 0
        
        while (len(img_name_aug_arr) < aug_num):
            aug_method = list(aug_lst)[aug_i]
            for img_path, _ in tqdm(data_lst):
                img = cv2.imread(img_path)
                img_aug = self.basic_augment[aug_method].augment_image(img)
                img_aug_path = self.save_aug_image(img_aug, img_path, aug_path, aug_method)
                img_name_aug_arr.append(img_aug_path)
                if len(img_name_aug_arr) >= aug_num:
                    return img_name_aug_arr
            aug_i += 1
        return img_name_aug_arr


class Augment_Manager:
    def __init__(self, data):
        '''
        :param data: Dataset object
        '''
        self.data = data
        self.augmentation = Augmentation()
        self.class_count = self.data.get_class_count()
        self.max_class_count = max(self.class_count.values())
    
    def checkIf_augment(self, class_name):
        return self.class_count[class_name] < self.max_class_count

    def update_aug_data(self, img_name_aug_arr):
        for img_name_aug in img_name_aug_arr:
            self.data.add_sample(img_name_aug, img_name_aug + '.json')
        self.class_count = self.data.get_class_count()
        

    def augment(self, aug_path):
        '''
        :param aug_path: path to save augmented data
        :param aug_num: number of augmented data
        '''
        if not os.path.exists(aug_path):
            os.makedirs(aug_path)

        number_of_basic_aug = self.augmentation.number_of_basic_aug()
        
        for class_name in self.class_count:
            print('Augmenting class: ' + class_name)
            if self.checkIf_augment(class_name):
                data_lst = self.data.get_samples_by_cls(class_name)
                number_of_basic_aug_img = len(data_lst) * number_of_basic_aug
                remain = self.max_class_count - number_of_basic_aug_img
                # If use all the basic augmentation techniques makes 
                # the number of augmented data larger than the number of samples in the max class, 
                # then clamb tthe aug_num
                if remain < 0:
                    basic_aug_num = self.max_class_count - len(data_lst)
                    img_name_aug_arr = self.augmentation.augment_basic_data(data_lst, aug_path, basic_aug_num)
                    self.update_aug_data(img_name_aug_arr)
                
                # If the class is not balanced even though use all basic augmentation techniques, then use noisy augmentation
                elif remain > 0:
                    basic_aug_num = self.max_class_count - len(data_lst)
                    if basic_aug_num > self.class_count[class_name] * number_of_basic_aug:
                        basic_aug_num = self.class_count[class_name] * number_of_basic_aug
                    img_name_aug_arr = self.augmentation.augment_basic_data(data_lst, aug_path, basic_aug_num)
                    self.update_aug_data(img_name_aug_arr)
                    
                    data_lst = self.data.get_samples_by_cls(class_name)
                    noise_aug_num = self.max_class_count - self.class_count[class_name]
                    
                    img_name_aug_arr = self.augmentation.augment_noisy_data(data_lst, aug_path, noise_aug_num)
                    self.update_aug_data(img_name_aug_arr)


data = Dataset('GOOD DIES - Copy')
print(data.get_class_count())
aug = Augment_Manager(data)
aug.augment('GOOD DIES - Copy/augmented')