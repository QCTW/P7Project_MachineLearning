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
    return sp.csr_matrix( (np_array, (rows, cols)), shape)

def expends(X_small, F_small, X_larger, F_larger):
    f_larger_set = set(F_larger)
    csr_new = sp.csr_matrix( (X_small.shape[0], X_larger.shape[1]))
    for i in range(X_small.shape[0]):
        for j in range(len(F_small)):
            f = F_small[j]
            if(f in f_larger_set):
                idx = F_larger.index(f)
                csr_new[i, idx] = X_small.getcol(j)

    return csr_new

def merge_csr_matrix_by_col(csr_m1, csr_m2):
    return sp.hstack((csr_m1, csr_m2))

def merge_csr_matrix_by_row(csr_m1, csr_m2):
    return sp.vstack((csr_m1, csr_m2))

def get_unique_value_in_list(np_arr): # Return a list, not np.array
    ret = []
    seen = set()
    for ele in np_arr.tolist():
        if ele not in seen:
            seen.add(ele) 
            ret.append(ele)
    return ret