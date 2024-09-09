import torch
from tqdm import tqdm


def torch_dbscan(X, eps, min_samples):
    """
    https://www.geeksforgeeks.org/pytorch-for-unsupervised-clustering/#dbscan-clustering
    with some modification

    # DBSCAN parameters
    # eps = 0.1
    # min_samples = 5

    # Perform clustering
    # labels = torch_dbscan(features, eps, min_samples)
    """
    n_samples = X.shape[0]
    labels = torch.full((n_samples,), -1, dtype=torch.int)

    # Initialize cluster label and visited flags
    cluster_label = -1
    visited = torch.zeros(n_samples, dtype=torch.bool)

    # Iterate over each point
    for i in tqdm(range(n_samples)):
        if visited[i]:
            continue
        visited[i] = True

        # Find neighbors
        neighbors_cond = torch.nonzero(euclidean_distance(X[i], X) < eps)

        if neighbors_cond.shape[0] < 2:
            continue

        neighbors = neighbors_cond.squeeze()

        # import pdb; pdb.set_trace()

        if neighbors.shape[0] < min_samples:
            # Label as noise
            labels[i] = -1
        else:
            # Expand cluster
            cluster_label += 1
            labels[i] = cluster_label
            expand_cluster(
                X, labels, visited, neighbors, cluster_label, eps, min_samples
            )

    return labels


def expand_cluster(X, labels, visited, neighbors, cluster_label, eps, min_samples):
    i = 0
    while i < neighbors.shape[0]:
        neighbor_index = neighbors[i].item()
        if not visited[neighbor_index]:
            visited[neighbor_index] = True
            neighbor_neighbors = torch.nonzero(
                euclidean_distance(X[neighbor_index], X) < eps
            ).squeeze()
            if neighbor_neighbors.shape[0] >= min_samples:
                neighbors = torch.cat((neighbors, neighbor_neighbors))
        if labels[neighbor_index] == -1:
            labels[neighbor_index] = cluster_label
        i += 1


def euclidean_distance(x1, x2):
    return torch.sqrt(torch.sum((x1 - x2) ** 2, dim=1))
