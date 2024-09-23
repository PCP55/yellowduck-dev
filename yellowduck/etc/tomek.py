# Get it from https://github.com/scikit-learn-contrib/imbalanced-learn/blob/master/imblearn/under_sampling/_prototype_selection/_tomek_links.py
# But return the third argument, removed_indices.

"""Class to perform under-sampling by removing Tomek's links."""

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
#          Fernando Nogueira
#          Christos Aridas
# License: MIT

import numbers
from typing import Union

import numpy as np
from imblearn.under_sampling.base import BaseCleaningSampler
from imblearn.utils import _safe_indexing
from sklearn.neighbors import NearestNeighbors


class TomekLinks(BaseCleaningSampler):
    """Under-sampling by removing Tomek's links."""

    _parameter_constraints: dict = {
        **BaseCleaningSampler._parameter_constraints,
        "n_jobs": [numbers.Integral, None],
    }

    def __init__(self, *, sampling_strategy="auto", n_jobs=None):
        super().__init__(sampling_strategy=sampling_strategy)
        self.n_jobs = n_jobs

    @staticmethod
    def is_tomek(
        y: np.ndarray, nn_index: np.ndarray, class_type: Union[int, str]
    ) -> np.ndarray:
        """Detect if samples are Tomek's link using vectorized operations.

        Parameters
        ----------
        y : np.ndarray
            Target vector of the data set.
        nn_index : np.ndarray
            Index of the closest nearest neighbour for each sample.
        class_type : int or str
            Label of the minority class.

        Returns
        -------
        np.ndarray
            Boolean array indicating Tomek links (True for Tomek link).
        """
        links = np.zeros(len(y), dtype=bool)

        # Get mask for excluded classes (majority class)
        excluded_mask = np.isin(y, class_type, invert=True)

        # Find Tomek links: nearest neighbors of each other and different classes
        different_class_mask = y[nn_index] != y
        reverse_neighbor_mask = nn_index[nn_index] == np.arange(len(y))

        # Combine conditions to identify Tomek links
        links = np.logical_and(different_class_mask, reverse_neighbor_mask)
        links[excluded_mask] = False  # Exclude classes not in the class_type

        return links

    def _fit_resample(self, X: np.ndarray, y: np.ndarray):
        """Apply Tomek links under-sampling."""
        # Find the nearest neighbour of every point
        nn = NearestNeighbors(n_neighbors=2, n_jobs=self.n_jobs)
        nn.fit(X)
        nns = nn.kneighbors(X, return_distance=False)[:, 1]

        # Identify Tomek links
        links = self.is_tomek(y, nns, self.sampling_strategy_)

        # Store indices of retained and removed samples
        self.sample_indices_ = np.flatnonzero(~links)
        removed_indices = np.flatnonzero(links)

        # Return the resampled dataset
        return (
            _safe_indexing(X, self.sample_indices_),
            _safe_indexing(y, self.sample_indices_),
            removed_indices,
        )

    def _more_tags(self):
        return {"sample_indices": True}
