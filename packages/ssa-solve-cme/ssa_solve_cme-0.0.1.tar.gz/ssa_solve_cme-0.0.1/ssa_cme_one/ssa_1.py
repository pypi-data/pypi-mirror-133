import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mul
import pandas as pd

k = [60, 25, 1, 0.1, 0.25]
t_max = 6
def ssa_trend(self):
    t = 0
    n_on = 1
    n_off = 0
    n_p = 0
    m = 1
    num_p = []
    while t<= t_max:
        s = [[0, 0, 0, -1, 1],   #G_on
             [1, 1, -1, 0, 0],   #P
             [0, 0, 0, 1, -1]]   #G_off
        fr = [60*n_on, 25*n_off, n_p, 0.1*n_on, 0.25*n_off]
        u = np.random.rand(2,1)
        r = 0
        lam = np.sum(fr)
        tao = (-np.log(u[0]))/lam
        add = np.cumsum(fr)
        while add[r] <= u[1] * lam:
            r = r + 1
        n_p = n_p + s[1][r]
        n_on = n_on + s[0][r]
        n_off = n_off + s[2][r]
        if t < m :
            if num_p == []:
                pass

        elif t >= m :
            num_p.append(n_p)
            m = m + 1
        t = t + tao

    return num_p
if __name__ == '__main__':
    N = 2
    pool = mul.Pool()
    res = pool.map(ssa_trend, range(N))
    X = range(0, 100)
    for i in range(0,5):
        nlist=[]
        for j in range(0,N):
            nlist.append(res[j][i])
        n, bins, patches = plt.hist(nlist, 100, (0, 100), density = True, alpha = 0.5)
        path = 'E:/deep_learning/PycharmProjects/pythonProject/telegraph.csv'
        data = pd.read_csv(path)

        y = data[['%d' % (i + 1)]]
        plt.plot(X, y)

        if i == 5:
            plt.title('steady state')
        else:
            plt.title('t=%d' % (i + 1))
        plt.show()
