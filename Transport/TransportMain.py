import numpy as np
import DFS
from Solver import northwestMethods, potentialMethods, update

def main(sumA, sumB, cost, size):
    ## Step-1:
    adj, X = northwestMethods(sumA, sumB, size=(n, m))
    # print(adj, X)

    _dfs = DFS.DFS(adj, size=(n, m), origin_point=(0, 0))
    cnt = 0
    while True:
        cnt += 1

        ## Step-2:
        w, v, discri_matrix, check_point = potentialMethods(adj, cost, size=(n, m))
        # print(w, '\n', v, '\n', discri_matrix,'\n' , check_point)
        print(w, v)
        # print(adj,'\n', X,'\n', cost)

        if check_point == (-1, -1):
            print('Transport algorithm end!')
            break

        _dfs.adj = adj
        _dfs.origin_point = check_point
        _dfs.path = [check_point]

        for i in range(4):
            F = _dfs.dfs(begin=(_dfs.origin_point[0] + _dfs.direct[i][0], _dfs.origin_point[1] + _dfs.direct[i][1]),
                         direct_idx=i, depth=1)
            # print(i)
            if F: print(_dfs.path); break

        path = _dfs.path

        # update: adj(basic<->non-basic) / X
        adj, X = update(adj, X, path)
        # print(adj, '\n', X)
        print('*************')
    return adj, X

if __name__ == '__main__':
    n, m = 3, 4
    # cost = np.asarray([[6, 4, 5, 9],[8, 3, 6, 4],[5, 8, 7, 8]])
    # sumA = np.asarray([10, 12, 8]) # n
    # sumB = np.asarray([5, 9, 6, 10]) # m
    cost = np.asarray([[5, 8, 3, 4], [6, 7, 4, 8], [7, 6, 8, 5]])
    sumA = np.asarray([10, 12, 9])
    sumB = np.asarray([5, 5, 11, 10])
    adj, X = main(sumA, sumB, cost, size=(n, m))
    print(adj, '\n', X)



