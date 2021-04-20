"""Check duplicate image within same folder.

There are 2 approachs.
1. exact match:     Using Cryptographic hashing algorithms in 'hashlib'
2. similar match:   Using Perceptual hashing algorithms in 'imagehash' 
                    and use Hamming distance for finding differrence.
"""

import os
import PIL
import hashlib
import imagehash
import numpy as np
import matplotlib.pyplot as plt

class ImageDuplicate():
    def __init__(self, image_folder_path: str):
        try: # For development phase only
            get_ipython
            self.current_path = os.getcwd()
        except: # For production
            self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.current_path = os.path.join(self.current_path, image_folder_path)

        self.image_in_folder_list = [file for file in os.listdir(self.current_path) if (file.endswith('.png')) | (file.endswith('.jpg'))]
        self.image_path_list = [os.path.join(self.current_path,image) for image in self.image_in_folder_list]
        self.hash_value_list = []

        self.similar_group_dict = {} # Group of image separate by hash value
        self.non_duplicate_list = [] # Select 1 image in each group
        self.duplicate_list = [] # The rest that not be selected in non_duplicate_list

    def find_exact(self):
        print(f'Using method: Exact Match (MD5)')

        for image_file in self.image_in_folder_list:
            image_fullpath = os.path.join(self.current_path,image_file)
            with open(image_fullpath, 'rb') as f:
                hash_value = hashlib.md5(f.read()).hexdigest()
            self.hash_value_list.append(hash_value)

        fast_check_duplicate = len(set(self.hash_value_list)) - len(self.hash_value_list)
        if fast_check_duplicate == 0:
            print('There is no duplicate image here.')
            return
        else:
            for image_name, hash_value in zip(self.image_in_folder_list,self.hash_value_list):
                if hash_value not in self.similar_group_dict:
                    self.similar_group_dict[hash_value] = [image_name]
                    self.non_duplicate_list.append(image_name)
                else:
                    self.similar_group_dict[hash_value] += [image_name]
                    self.duplicate_list.append(image_name)
                
            temp_similar_group_dict = self.similar_group_dict.copy()
            for (key,value) in temp_similar_group_dict.items():
                if len(value) == 1:
                    self.similar_group_dict.pop(key)

        group_key = list(np.arange(len(self.similar_group_dict)))
        self.similar_group_dict = dict(zip(group_key,list(self.similar_group_dict.values())))

        num_duplicate = len(self.duplicate_list)
        num_all = len(self.image_in_folder_list)
        percentage = np.round(num_duplicate/num_all * 100, 2)
        print(f'There are {num_duplicate} duplicated images out of {num_all} which is around {percentage} %.')

        return self.similar_group_dict, self.duplicate_list, self.non_duplicate_list

    def find_similar(self, hash_method:str='phash', distance:int=2, hash_size:int=16):
        print(f'Using method: {hash_method}\nAn accepted distance: {distance}\nHashing size: {hash_size}')

        for image_file in self.image_in_folder_list:
            image_fullpath = os.path.join(self.current_path,image_file)
            image = PIL.Image.open(image_fullpath)
            if hash_method == 'phash':
                hash_value = imagehash.phash(image, hash_size)
            elif hash_method == 'ahash':
                hash_value = imagehash.average_hash(image, hash_size)
            elif hash_method == 'dhash':
                hash_value = imagehash.dhash(image, hash_size)
            elif hash_method == 'whash':
                hash_value = imagehash.whash(image, hash_size)
            elif hash_method == 'crop_resistant_hash':
                """
                - No hashing size
                - Take too much time!! (as another hash algorithm use 250 ms but this one take 1 min for test dataset)
                """
                hash_value = imagehash.crop_resistant_hash(image)
            else:
                print('There are 4 methods here which is phash, ahash, dhash, whash')
            self.hash_value_list.append(hash_value)

        # It is recommend to use distance = 0 for time reduction.

        if distance == 0:
            fast_check_duplicate = len(set(self.hash_value_list)) - len(self.hash_value_list)
            if fast_check_duplicate == 0:
                print('There is no duplicate image here.')
                return
            else:
                for image_name, hash_value in zip(self.image_in_folder_list,self.hash_value_list):
                    if hash_value not in self.similar_group_dict:
                        self.similar_group_dict[hash_value] = [image_name]
                        self.non_duplicate_list.append(image_name)
                    else:
                        self.similar_group_dict[hash_value] += [image_name]
                        self.duplicate_list.append(image_name)
        else:
            temp_filename_list = []
            num = 0
            filename_hash_dict = dict(zip(self.image_in_folder_list,self.hash_value_list))
            temp_filename_hash_dict = dict(zip(self.image_in_folder_list,self.hash_value_list))
            sort_filename_hash_dict = sorted(filename_hash_dict)
            
            for file_first in sort_filename_hash_dict:
                if file_first in temp_filename_hash_dict:
                
                    temp_similar_list = []
                    temp_similar_list.append(file_first)
                    temp_filename_list.append(file_first)
                    temp_filename_hash_dict.pop(file_first)

                    image_first = filename_hash_dict[file_first]
                
                for file_second in sort_filename_hash_dict:
                    if file_second not in temp_filename_list:
                        image_second = filename_hash_dict[file_second]
                        hamming_distance = image_first - image_second
                        
                        if hamming_distance <= distance:
                            temp_similar_list.append(file_second)
                            temp_filename_list.append(file_second)

                if len(temp_similar_list) > 1:
                    self.similar_group_dict[num] = temp_similar_list

                    for _item in temp_similar_list[1:]:
                        self.duplicate_list.append(_item)

                    num = num + 1

            self.non_duplicate_list = [image for image in self.image_in_folder_list if image not in self.duplicate_list]

        return self.similar_group_dict, self.duplicate_list, self.non_duplicate_list

        num_duplicate = len(self.duplicate_list)
        num_all = len(self.image_in_folder_list)
        percentage = np.round(num_duplicate/num_all * 100, 2)

        print(f'There are {num_duplicate} duplicated images out of {num_all} which is around {percentage} %.')


class ShowImageDuplicate():
    def __init__(self, image_folder_path, group_of_duplicate_dict:dict):
        self.image_folder_path = image_folder_path
        self.group_of_duplicate_dict = group_of_duplicate_dict

        self.number_of_group = len(self.group_of_duplicate_dict)
        print(f'There are {self.number_of_group} of duplicate image.\nUse .show_group(group_number) or .show_all() for all group.')
    def show_all(self):
        """
        Show only first 5 images in each group
        """
        fig, axes = plt.subplots(nrows=self.number_of_group, ncols=5, figsize=(24, 24))
        for axis in axes.ravel():
            axis.set_axis_off()
        for group_number in np.arange(self.number_of_group):
            image_list = self.group_of_duplicate_dict[group_number]
            if len(image_list) > 5:
                image_list = image_list[:5]
            for image_number in np.arange(len(image_list)):
                image_path = os.path.join(self.image_folder_path,image_list[image_number])
                image = PIL.Image.open(image_path)
                axes[group_number,image_number].imshow(image)
        plt.tight_layout()

    def show_group(self, group_number):
        image_list = self.group_of_duplicate_dict[group_number]
        if len(image_list) < 5:
            num_col = len(image_list)
        else:
            num_col = 5
        num_row = int(len(image_list)/num_col)
        mod = len(image_list)%num_col
        if mod != 0:
            num_row = num_row + 1
        fig, axes = plt.subplots(nrows=num_row, ncols=num_col, figsize=(24, 10))
        for axis in axes.ravel():
            axis.set_axis_off()
        for index, image_name in enumerate(image_list):
            image_path = os.path.join(self.image_folder_path,image_name)
            image = PIL.Image.open(image_path)
            axes.ravel()[index].imshow(image)
        plt.tight_layout()