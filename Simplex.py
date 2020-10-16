import numpy as np

def init(A, b, c, rank, m):
    A_b = A[:, (m-rank):]
    A_n = A[:, :(m-rank)]

    c_b = c[:, (m-rank):]
    c_n = c[:, :(m-rank)]

    A_b_inv = np.linalg.pinv(A_b)
    b_ = A_b_inv @ b
    tmp = c_b @ A_b_inv
    ZC = tmp @ A_n - c_n

    F = tmp @ b

    # Get the Simplex Tabel
    T1 = np.vstack((A_b_inv @ A_n, ZC))
    T2 = np.vstack((A_b, np.zeros_like(ZC)))
    T3 = np.vstack((b_, F))
    T = np.hstack((T1, T2, T3))

    return T

def main(T, rank, m):
    '''

    :param T: left is non-basic and right is basic
    :param rank: the number of basic vector or variable
    :return:
    '''
    while True:
        F = T[-1, -1]
        ZC = T[-1, :(m - rank)]

        if np.max(ZC) <= 0:
            return F

        # Find the main column
        main_col = np.argmax(T[-1, :(m-rank)])
        # Find the main row
        tmp = T[:-1, -1] / T[:-1, main_col]
        index, min_v = -1, 1e10
        for i in range(tmp.shape[0]):
            if tmp[i] < min_v and tmp[i] > 0:
                index, min_v = i, tmp[i]
        main_row = index
        if main_row == -1:
            raise Exception('No solution!')
            return False

        # Update
        T[main_row, :] = T[main_row, :] / T[main_row, main_col]
        for i in range(T.shape[0]):
            if i == main_row:
                continue
            alpha = T[i, main_col] / T[main_row, main_col]
            T[i, :] = T[i, :] - alpha * T[main_row, :]
        turn = T[:, main_col]
        T[:, main_col] = T[:, (m-rank+main_row-1)]
        T[:, (m-rank+main_row-1)] = turn

    return 0


if __name__ == '__main__':
    data = np.loadtxt('data/data-1.txt')
    n, m = data.shape

    # C: row-vector
    c = data[0, :-1]
    c = c[np.newaxis, :]
    # B: col-vector
    b = data[1:n, -1]
    b = b[:, np.newaxis]
    # A: matrix
    A = data[1:n, :-1]

    rank = min(n-1, m-1)
    assert rank == n-1
    m = m-1
    T = init(A, b, c, rank, m)
    Final = main(T, rank, m)

    print('The min value of object function is ', Final)