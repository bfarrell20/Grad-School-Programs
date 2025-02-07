#!/usr/bin/env python3
import numpy as np
from scipy.sparse import coo_matrix
import requests
import io

def prepare_matrix():
    url = "https://raw.githubusercontent.com/singhj/big-data-repo/main/datasets/chicago-taxi-rides.csv"
    response = requests.get(url)  # get data from github link
    
    # Put csv into an array
    data = np.genfromtxt(io.StringIO(response.text), delimiter=',', skip_header=1, filling_values=0)

    # Extract rows, columns, and values from the data
    rows = data[:, 0].astype(int)
    cols = data[:, 1].astype(int)
    values = data[:, 2]

    # set matrix size to given value 77
    matrix_size = 77

     # Make sure all the indices are within the matrix size
    rows = np.clip(rows, 0, 76)
    cols = np.clip(cols, 0, 76)

    # Create the matrix
    matrix = coo_matrix((values, (rows, cols)), shape=(matrix_size, matrix_size))

    dense_matrix = matrix.toarray()

    # Normalize the matrix by dividing each row by its sum
    row_sums = dense_matrix.sum(axis=1, keepdims=True)
    normalized_matrix = dense_matrix / row_sums

    # Handle rows with zero sum
    normalized_matrix[row_sums.flatten() == 0] = 1 / matrix_size

    return normalized_matrix

def TrafficRank(iter):
    # Get the matrix from first function
    transition_matrix = prepare_matrix()

    # Number of nodes 
    num_nodes = transition_matrix.shape[0]

    # Initialize the rank vector 
    rank_vector = np.ones(num_nodes) / num_nodes

    # Damping factor
    damping_factor = 0.85

    # Iteratively update the rank vector
    for _ in range(iter):
        rank_vector = damping_factor * transition_matrix.T @ rank_vector + (1 - damping_factor) / num_nodes

    return rank_vector

prepare_matrix()
TrafficRank(1)
