import collections
import json
from enum import Enum

import numpy as np
import pandas as pd
from preda.deployment.airflow.utils import kube_pod_xcom_push
from preda.logger import logger
from sklearn.metrics import classification_report
from snorkel_lab.config import config as package_config


def logger_info_dataframe(dataframe: pd.DataFrame):
    logger.info(f"\n{dataframe.to_markdown()}")


def logger_info_classification_report(y_true, y_pred, target_names):
    report_dict = classification_report(
        y_true, y_pred, target_names=target_names, output_dict=True, digits=2
    )
    report_df = pd.DataFrame(report_dict).round(2)
    logger.info(f"\n{report_df.transpose().to_markdown()}")
    return report_dict


def pass_information_to_the_next_task(informations: dict) -> None:
    logger.info("----- pass_information_to_the_next_task -----")
    xcom_return = json.dumps(informations)
    kube_pod_xcom_push({"xcom_return": xcom_return})


def get_xcom_from_the_previous_task(xcom_return: str) -> dict:
    logger.info("----- get_xcom_from_the_previous_task -----")
    xcom_return = json.loads(xcom_return)
    logger.info(f"xcom_return: {xcom_return}")
    return xcom_return


###


# TODO: Fix and add this into training and prediction pipeline
class PredictionStats:
    def __init__(self, prediction_array: np.ndarray):
        self.prediction_array = prediction_array

    @property
    def value(self) -> np.ndarray:
        return self.prediction_array

    @property
    def abstain_value(self) -> int:
        return package_config.snorkel.abstain_value

    @property
    def total_labeled_datapoint(self) -> int:
        return np.count_nonzero(
            self.prediction_array != package_config.snorkel.abstain_value
        )

    @property
    def total_unlabeled_datapoint(self) -> int:
        return np.count_nonzero(
            self.prediction_array == package_config.snorkel.abstain_value
        )

    @property
    def total_datapoint(self) -> int:
        return len(self.prediction_array)

    @property
    def total_coverage_percent(self) -> float:
        return round(self.total_labeled_datapoint / self.total_datapoint, 4) * 100

    @property
    def individual_coverage(self) -> dict:
        return collections.Counter(self.prediction_array)

    @property
    def unique_class(self) -> list:
        return list(np.unique(self.prediction_array))

    @property
    def unique_class_without_abstain(self) -> list:
        unique_class = list(np.unique(self.prediction_array))
        if package_config.snorkel.abstain_value in unique_class:
            unique_class.remove(package_config.snorkel.abstain_value)
        return unique_class

    def get_least_support_class(self, Label: Enum) -> dict:
        class_counter = self.individual_coverage.copy()
        del class_counter[package_config.snorkel.abstain_value]
        key_least_support_class = min(class_counter, key=class_counter.get)
        key_name_least_support_class = Label(key_least_support_class).name
        value_least_support_class = min(class_counter.values())
        return {key_name_least_support_class: value_least_support_class}

    def get_class_balance(self) -> float:
        """
        Using Shannon Entropy to findout class balance
        0 for an unbalanced data set
        1 for a balanced data set
        Ref: https://stats.stackexchange.com/questions/239973/a-general-measure-of-data-set-imbalance
        """
        counts = np.array(
            [
                count_label
                for label, count_label in collections.Counter(
                    self.prediction_array
                ).items()
                if label != package_config.snorkel.abstain_value
            ]
        )
        probabilities = counts / self.total_labeled_datapoint
        shannon_entropy = -(probabilities * np.log(probabilities)).sum()
        return round(
            shannon_entropy / np.log(len(self.unique_class_without_abstain)), 2
        )
