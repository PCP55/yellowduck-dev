# Check Duplicate Picture in Directory

# mode = 'same'
# Use Cryptographic hashing algorithms in 'hashlib'
# Editing image won't be count as the duplicated image.

# mode = 'similar'
# Use Perceptual hashing algorithms
# Hash value of editing image will be close to the original image.

import os
import hashlib
from PIL import Image
import imagehash
import numpy as np

class duplicate():
    #################################################################
    # init
    def __init__(self, image_folder_path):
        

        try:
            get_ipython
            self.current_path = os.getcwd() # For test function in .ipynb
        except:
            self.current_path = os.path.dirname(os.path.realpath(__file__)) # For .py
            
        self.current_path = os.path.join(self.current_path, image_folder_path)

        self.remove_filename_list = [] # List of similar image except original one
        self.similar_group_dict = {} # Group of similar image including original one

    def from_directory():

    def from_image():

    #################################################################
    # Find    
    def find(self, mode = 'same', distance = 0, phash_size = 16):
        
        num = 0
        filename_hash = dict()
        image_list = os.listdir(self.current_path)
        
        ###########################

        if mode == 'same':

            hash_keys = dict()
            duplicate_group = dict()
            self.remove_filename_list = []

            for index, filename in enumerate(image_list):

                file_path = os.path.join(self.current_path, filename)

                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as f:
                        filehash = hashlib.md5(f.read()).hexdigest()

                    filename_hash[filename] = filehash

                    if filehash not in hash_keys:
                        hash_keys[filehash] = index
                        
                    else:
                        self.remove_filename_list.append(filename)

            set_hash = set(filename_hash.values())

            for h in set_hash:
                duplicate_group[h] = [k for k in filename_hash.keys() if filename_hash[k] == h]

            for val in duplicate_group.values():
                if len(val) > 1:
                    self.similar_group_dict[num] = val
                    num = num + 1

            ############
            # print

            num_duplicate = len(self.remove_filename_list)
            num_all = len(filename_hash)
            percentage = np.round(num_duplicate/num_all * 100, 2)

            print('There are {} duplicated images from {} images which is around {} %.'.format(num_duplicate, num_all,percentage))

            return self.remove_filename_list, self.similar_group_dict

        ###########################

        if mode == 'similar':
            
            temp_filename_hash = dict()
            temp_filename_list = []
            self.remove_filename_list = []

            print('The accepted distance is {}'.format(distance))
            
            ############
            # Find phash
            for filename in image_list:

                file_path = os.path.join(self.current_path, filename)
                
                if os.path.isfile(file_path):
                    image_file = Image.open(file_path)                        
                    phash = imagehash.phash(image_file, hash_size = phash_size)
                    filename_hash[filename] = phash
                    temp_filename_hash[filename] = phash
            
            ############        
            # Find similarity between image using hamming distance (of phash)
            
            sort_filename_hash = sorted(filename_hash)
            
            for file_first in sort_filename_hash:
                
                if file_first in temp_filename_hash:
                
                    temp_similar_list = []
                    temp_similar_list.append(file_first)
                    temp_filename_list.append(file_first)
                    temp_filename_hash.pop(file_first)

                    image_first = filename_hash[file_first]
                
                for file_second in sort_filename_hash:
                    
                    if file_second not in temp_filename_list:
                        
                        image_second = filename_hash[file_second]
                        
                        hamming_distance = image_first - image_second
                        
                        if hamming_distance <= distance:
                            temp_similar_list.append(file_second)
                            temp_filename_list.append(file_second)

                if len(temp_similar_list) > 1:
                    self.similar_group_dict[num] = temp_similar_list

                    for _item in temp_similar_list[1:]:
                        self.remove_filename_list.append(_item)

                    num = num + 1
            
            ############
            # print

            num_duplicate = len(self.remove_filename_list)
            num_all = len(filename_hash)
            percentage = np.round(num_duplicate/num_all * 100, 2)

            print('There are {} similar images in distance from {} images which is around {} %.'.format(num_duplicate, num_all,percentage))

            return self.remove_filename_list, self.similar_group_dict

    #################################################################
    # Get           
    def get(self):
            
        return self.similar_group_dict, self.remove_filename_list
            
                   
    #################################################################
    # Show    
    def show(self, max_sample_case = 1, max_sample_each_case = 1, size = 1):
        
        try:
            get_ipython
#             matplotlib show duplicate or similar picture
            print(self.similar_group_dict)
        except:
            print('Please run it in iPython Notebook')

    #################################################################
    # Move 
    def move_to_folder(self):
        pass

    #################################################################
    # Remove    
    def remove_in_folder(self):
        for filename in self.remove_filename_list:
            file_path = os.path.join(self.current_path, filename)
            os.remove(file_path)

# Credit: https://medium.com/@urvisoni/removing-duplicate-images-through-python-23c5fdc7479e