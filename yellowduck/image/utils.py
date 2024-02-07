import matplotlib.pyplot as plt
import numpy as np
import os
import PIL


class ShowImageDuplicate:
    def __init__(self, image_folder_path, group_of_duplicate_dict: dict):
        self.image_folder_path = image_folder_path
        self.group_of_duplicate_dict = group_of_duplicate_dict

        self.number_of_group = len(self.group_of_duplicate_dict)
        print(
            f"There are {self.number_of_group} of duplicate image.\nUse .show_group(group_number) or .show_all() for all group."
        )

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
                image_path = os.path.join(
                    self.image_folder_path, image_list[image_number]
                )
                image = PIL.Image.open(image_path)
                axes[group_number, image_number].imshow(image)
        plt.tight_layout()

    def show_group(self, group_number):
        image_list = self.group_of_duplicate_dict[group_number]
        if len(image_list) < 5:
            num_col = len(image_list)
        else:
            num_col = 5
        num_row = int(len(image_list) / num_col)
        mod = len(image_list) % num_col
        if mod != 0:
            num_row = num_row + 1
        fig, axes = plt.subplots(nrows=num_row, ncols=num_col, figsize=(24, 10))
        for axis in axes.ravel():
            axis.set_axis_off()
        for index, image_name in enumerate(image_list):
            image_path = os.path.join(self.image_folder_path, image_name)
            image = PIL.Image.open(image_path)
            axes.ravel()[index].imshow(image)
        plt.tight_layout()
