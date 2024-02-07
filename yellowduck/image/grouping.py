from abc import ABC, abstractmethod
import hashlib
import imagehash
import numpy as np
import os
import PIL

from utils.similarity import get_similar


class ImageGroupingStrategy(ABC):
    @abstractmethod
    def get_similar_images_index(self, **kwargs) -> list:
        pass


class ExactGrouping(ImageGroupingStrategy):
    def get_similar_images_index(self, **kwargs) -> list:
        """
        Find similar images using MD5 hashing method
        """
        print(f"Using method: Exact Grouping")
        images_index = get_similar(self.images_list)
        return images_index


class SimilarGroupingPHash(ImageGroupingStrategy):
    def get_similar_images_index(self, **kwargs) -> list:
        """
        Find similar images using PHash hashing method
        """
        print(f"Using method: Similar Grouping using PHash")
        images_index = get_similar(self.images_list)
        return images_index


class ImageGrouping:
    def __init__(self):
        pass

    def get_group(self):
        pass


class ImageDuplicate:
    def __init__(self, image_folder_path: str):
        try:  # For development phase only
            get_ipython
            self.current_path = os.getcwd()
        except:  # For production
            self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.current_path = os.path.join(self.current_path, image_folder_path)

        self.image_in_folder_list = [
            file
            for file in os.listdir(self.current_path)
            if (file.endswith(".png")) | (file.endswith(".jpg"))
        ]
        self.image_path_list = [
            os.path.join(self.current_path, image)
            for image in self.image_in_folder_list
        ]
        self.hash_value_list = []

        self.similar_group_dict = {}  # Group of image separate by hash value
        self.non_duplicate_list = []  # Select 1 image in each group
        self.duplicate_list = []  # The rest that not be selected in non_duplicate_list

    def find_exact(self):
        print(f"Using method: Exact Match (MD5)")

        for image_file in self.image_in_folder_list:
            image_fullpath = os.path.join(self.current_path, image_file)
            with open(image_fullpath, "rb") as f:
                hash_value = hashlib.md5(f.read()).hexdigest()
            self.hash_value_list.append(hash_value)

        fast_check_duplicate = len(set(self.hash_value_list)) - len(
            self.hash_value_list
        )
        if fast_check_duplicate == 0:
            print("There is no duplicate image here.")
            return
        else:
            for image_name, hash_value in zip(
                self.image_in_folder_list, self.hash_value_list
            ):
                if hash_value not in self.similar_group_dict:
                    self.similar_group_dict[hash_value] = [image_name]
                    self.non_duplicate_list.append(image_name)
                else:
                    self.similar_group_dict[hash_value] += [image_name]
                    self.duplicate_list.append(image_name)

            temp_similar_group_dict = self.similar_group_dict.copy()
            for key, value in temp_similar_group_dict.items():
                if len(value) == 1:
                    self.similar_group_dict.pop(key)

        group_key = list(np.arange(len(self.similar_group_dict)))
        self.similar_group_dict = dict(
            zip(group_key, list(self.similar_group_dict.values()))
        )

        num_duplicate = len(self.duplicate_list)
        num_all = len(self.image_in_folder_list)
        percentage = np.round(num_duplicate / num_all * 100, 2)
        print(
            f"There are {num_duplicate} duplicated images out of {num_all} which is around {percentage} %."
        )

        return self.similar_group_dict, self.duplicate_list, self.non_duplicate_list

    def find_similar(
        self, hash_method: str = "phash", distance: int = 2, hash_size: int = 16
    ):
        print(
            f"Using method: {hash_method}\nAn accepted distance: {distance}\nHashing size: {hash_size}"
        )

        for image_file in self.image_in_folder_list:
            image_fullpath = os.path.join(self.current_path, image_file)
            image = PIL.Image.open(image_fullpath)
            if hash_method == "phash":
                hash_value = imagehash.phash(image, hash_size)
            elif hash_method == "ahash":
                hash_value = imagehash.average_hash(image, hash_size)
            elif hash_method == "dhash":
                hash_value = imagehash.dhash(image, hash_size)
            elif hash_method == "whash":
                hash_value = imagehash.whash(image, hash_size)
            elif hash_method == "crop_resistant_hash":
                """
                - No hashing size
                - Take too much time!! (as another hash algorithm use 250 ms but this one take 1 min for test dataset)
                """
                hash_value = imagehash.crop_resistant_hash(image)
            else:
                print("There are 4 methods here which is phash, ahash, dhash, whash")
            self.hash_value_list.append(hash_value)

        # It is recommend to use distance = 0 for time reduction.

        if distance == 0:
            fast_check_duplicate = len(set(self.hash_value_list)) - len(
                self.hash_value_list
            )
            if fast_check_duplicate == 0:
                print("There is no duplicate image here.")
                return
            else:
                for image_name, hash_value in zip(
                    self.image_in_folder_list, self.hash_value_list
                ):
                    if hash_value not in self.similar_group_dict:
                        self.similar_group_dict[hash_value] = [image_name]
                        self.non_duplicate_list.append(image_name)
                    else:
                        self.similar_group_dict[hash_value] += [image_name]
                        self.duplicate_list.append(image_name)
        else:
            temp_filename_list = []
            num = 0
            filename_hash_dict = dict(
                zip(self.image_in_folder_list, self.hash_value_list)
            )
            temp_filename_hash_dict = dict(
                zip(self.image_in_folder_list, self.hash_value_list)
            )
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

            self.non_duplicate_list = [
                image
                for image in self.image_in_folder_list
                if image not in self.duplicate_list
            ]

        num_duplicate = len(self.duplicate_list)
        num_all = len(self.image_in_folder_list)
        percentage = np.round(num_duplicate / num_all * 100, 2)

        print(
            f"There are {num_duplicate} duplicated images out of {num_all} which is around {percentage} %."
        )

        return self.similar_group_dict, self.duplicate_list, self.non_duplicate_list
