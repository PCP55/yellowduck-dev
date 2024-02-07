import numpy as np
from sklearn.cluster import DBSCAN
from strsimpy.levenshtein import Levenshtein


class TextGrouping:
    def __init__(
        self, list_of_text: list = [], distance: int = 1, minimum_members: int = 2
    ):
        self.list_of_text = list_of_text
        self.distance = distance
        self.minimum_members = minimum_members

    def _dbscan_levenshtein(self, x, y):
        """
        Implement DBScan to find similarity
        """
        i, j = int(x[0]), int(y[0])
        return Levenshtein().distance(self.list_of_text[i], self.list_of_text[j])

    def _get_result(self):
        return DBSCAN(
            metric=self._dbscan_levenshtein,
            eps=self.distance,
            min_samples=self.minimum_members,
        ).fit(np.arange(len(self.list_of_text)).reshape(-1, 1))

    def get_group(self):
        array_of_text = np.array(self.list_of_text)
        db_scan_result = self._get_result().labels_
        group = {}
        number_of_group = len(set(db_scan_result)) - 1
        number_of_individual = sum(db_scan_result == -1)

        if number_of_group > 0:
            print(
                f"There are {number_of_group} text groups having similar characters and {number_of_individual} individuals text."
            )
            for group_id in set(db_scan_result):
                group[group_id] = array_of_text[db_scan_result == group_id]
                # print(group_id)
                # print(array_of_text[db_scan_result==group_id])
        else:
            print("Cannot group text. Please reduce distance or minimum_members")

        return group
