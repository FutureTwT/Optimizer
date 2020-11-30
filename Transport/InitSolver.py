import numpy as np
import copy

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
        if _B[j] == 0:
            j += 1
        else:
            i += 1

    return adj, X

if __name__ == '__main__':
    northwestMethods()