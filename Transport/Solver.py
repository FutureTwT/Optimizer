import numpy as np
import copy
import scipy.sparse as sp

def northwestMethods(A, B, size):
    X = np.zeros(shape=size)
    adj = np.zeros_like(X) # init all non-basic param
    sumA = np.sum(A)
    sumB = np.sum(B)
    _A = copy.deepcopy(A)
    _B = copy.deepcopy(B)

    i, j = 0, 0
    while True:
        if i >= size[0] or j >= size[1]:
            break
        adj[i, j] = 1
        X[i, j] = min(_A[i], _B[j])
        _A[i] -= X[i, j]
        _B[j] -= X[i, j]
        if _B[j] == 0 and _A[i] != 0:
            j += 1
        elif _B[j] != 0 and _A[i] == 0:
            i += 1
        else:
            i += 1

    return adj, X

def potentialMethods(adj, cost, size):
    w = np.zeros(shape=(size[0],))
    w_flag = np.zeros_like(w)

    v = np.zeros(shape=(size[1],))
    v_flag = np.zeros_like(v)

    i, j = 0, 0
    w_flag[0] = 1
    sum_w, sum_v = 1, 0

    _adj = sp.csr_matrix(adj).tocoo()
    while sum_w < size[0] and sum_v < size[1]:
        for (i, j) in zip(_adj.row, _adj.col):
            if w_flag[i] == 1 and v_flag[j] == 1:
                continue
            elif w_flag[i] == 1:
                v[j] = cost[i, j] - w[i]
                v_flag[j], sum_v = 1, sum_v + 1
            elif v_flag[j] == 1:
                w[i] = cost[i, j] - v[j]
                w_flag[i], sum_w = 1, sum_w + 1
            else:
                continue

    discri_matrix = w.reshape((size[0], 1)) + v.reshape((1, size[1])) - cost
    discri_matrix[adj==1] = 0

    check_point = np.unravel_index(np.argmax(discri_matrix, axis=None), discri_matrix.shape)
    if discri_matrix[check_point] <= 0:
        check_point = (-1, -1)
    return w, v, discri_matrix, check_point

def update(adj, X, path):
    min_value = np.Inf
    min_value_idx = (-1, -1)
    for i in range(len(path)):
        if i % 2 == 1 and X[path[i][0], path[i][1]] < min_value:
            min_value = X[path[i][0], path[i][1]]
            min_value_idx = path[i]

    adj[path[0][0], path[0][1]], adj[min_value_idx[0], min_value_idx[1]] = 1, 0
    for i in range(len(path)):
        X[path[i][0], path[i][1]] = X[path[i][0], path[i][1]] + min_value if i % 2 == 0 \
            else X[path[i][0], path[i][1]] - min_value

    return adj, X

if __name__ == '__main__':
    # northwestMethods()
    potentialMethods(0, 0, size=(3, 3))