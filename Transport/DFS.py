import numpy as np
import sys
sys.setrecursionlimit(1000)

class DFS(object):
    def __init__(self, adj, size, origin_point):
        super(DFS, self).__init__()
        self.adj = adj
        self.n = size[0]
        self.m = size[1]
        self.path = []
        self.done_path = False
        self.origin_point = origin_point
        # down/right/up/left/
        self.direct = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def dfs(self, begin: tuple, direct_idx, depth):
        '''

        :param adj: [0, 1] Graph adjacent matrix, 1 is basic var and 0 is non-basic var
        :param begin: (x, y) is begin point and min-value is 1
        :param size: (n, m) shows that the matrix is n * m
        :return:
        '''
        if begin[0] >= self.n or begin[1] >= self.m or begin[0] < 0 or begin[1] < 0:
            return False
        if begin[0] ==  self.origin_point[0] and begin[1] == self.origin_point[1] and depth != 1:
            return True

        # corner true or not!
        flag = False
        if self.adj[begin[0], begin[1]] == 1:
            flag = True

        f = self.dfs(begin=(begin[0] + self.direct[direct_idx][0], begin[1] + self.direct[direct_idx][1]), direct_idx=direct_idx, depth=depth+1)
        if f: return True # cut dfs tree
        if flag:
            for i in range(4):
                if direct_idx == i:
                    continue
                if self.direct[i][0] + self.direct[direct_idx][0] == 0 and self.direct[i][1] + self.direct[direct_idx][1] == 0:
                    continue
                f = self.dfs(begin=(begin[0] + self.direct[i][0], begin[1] + self.direct[i][1]), direct_idx=i, depth=depth+1)
                if f and not self.done_path:
                    self.path.append(begin)
                    self.done_path == True if len(self.path) == 4 else False
                    return True

        return False

if __name__ == '__main__':
    A = np.asarray([[0,0,0,0],[1,1,0,1],[0,0,1,1]])
    begin = (2, 0)
    dfs = DFS(A, (3, 4), begin)
    dfs.path.append(begin)
    for i in range(4):
        F = dfs.dfs(begin=(begin[0] + dfs.direct[i][0], begin[1] + dfs.direct[i][1]), direct_idx=i, depth=1)
        if F: print(dfs.path); break

