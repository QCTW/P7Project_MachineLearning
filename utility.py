import scipy.sparse as sp
import numpy as np

def create_csr_matrix(double_array):
    shape = (len(double_array), len(double_array[0]))
    row_index = []
    col_index = []
    flat_array = []
    for i in range(len(double_array)):
        arr = double_array[i]
        for j in range(len(arr)):
            if(arr[j]!=0):
                flat_array.append(arr[j])
                row_index.append(i)
                col_index.append(j)

    rows = np.array(row_index)
    cols = np.array(col_index)
    np_array = np.array(flat_array)
    return sp.csr_matrix( (np_array, (rows, cols)),  shape)


def merge_csr_matrix_by_col(csr_m1, csr_m2):
    return sp.hstack((csr_m1, csr_m2))

def merge_csr_matrix_by_row(csr_m1, csr_m2):
    return sp.vstack((csr_m1, csr_m2))