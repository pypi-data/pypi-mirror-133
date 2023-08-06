import os

import numpy as np
from numpy.linalg import inv

os.add_dll_directory(os.path.join(os.environ['CUDA_PATH'], 'bin'))
"""tk = [x for x in range(1, 100)]
dt = 0.5
thick_x = 1.5e-4
t_k = 273.15
v = 7/6
dx = 1e-6
size_x = round(thick_x/dx + 1)
tkx = [x + t_k for x in range(1, 100)]
Emin = np.inf
E_data = []
"""


class solve(object):
    def __init__(self, step=None):
        self.step = step

    @staticmethod
    def CrankNicholsonSingle_GPU(func, T, m, n, a, phi_x, alpha_tk, beta_tk, step=None):
        """
                (见书P65)
                :param T:
                :param func 要求的函数
                :param m: m个时间点
                :param n: n个空间点
                :param step:步数
                :param a:主方程系数
                :param phi_x
                :param alpha_tk
                :param beta_tk        边界条件
                :return:
                """
        ...

    @staticmethod
    def CrankNicholsonSingle_CPU(func, T, m, n, a, phi_x, alpha_tk, beta_tk, step=None):

        """
        (见书P65)
        :param T:
        :param func 要求的函数
        :param m: m个时间点
        :param n: n个空间点
        :param step:步数
        :param a:主方程系数
        :param phi_x
        :param alpha_tk
        :param beta_tk        边界条件
        :return:
        """
        aa = 0
        res = []
        if step is None:
            step = n - 1
        h = 1 / m
        tau = T / n
        r = a * tau / h ** 2
        u = np.zeros((m + 1, n + 1))
        x = [i * h for i in range(m + 1)]
        t = [i * tau for i in range(n + 1)]
        left_mat = np.zeros((m - 1, m - 1))  # 迭代的三对角左右矩阵初始化
        right_mat = np.zeros((m - 1, m - 1))
        for i in range(m + 1):  # 迭代的三对角矩阵赋值
            u[i][0] = phi_x(x[i])
        for k in range(n + 1):
            u[0][k] = alpha_tk(t[k])
            u[m][k] = beta_tk(t[k])
        for xxx in range(0, m - 1):
            left_mat[xxx][xxx] = 1 + r
            right_mat[xxx][xxx] = 1 - r
        for qx in range(0, m - 2):
            left_mat[qx + 1][qx] = -(r / 2)
            right_mat[qx + 1][qx] = r / 2
        for xd in range(0, m - 2):
            left_mat[xd][xd + 1] = -(r / 2)
            right_mat[xd][xd + 1] = r / 2
        lmi = inv(left_mat)
        for k in range(n):  # 开始迭代n次
            tkmid = 0.5 * (t[k] + t[k + 1])  # t（1/2）
            tmp_add_mat = [tau * func(x[1], tkmid) + 0.5 * r * (u[0][k + 1] + u[0][k])] + [tau * func(x[i], tkmid) for i
                                                                                           in range(2, m - 1)] + [
                              tau * func(x[m - 1], tkmid) + r * 0.5 * (u[m][k + 1] + u[m][k])]  # 每次迭代时增加的矩阵
            add_mat = np.array([tmp_add_mat]).transpose()  # 进行新的向量迭代生成
            left = np.dot(right_mat, np.array([u[1:m][:][:, k]]).transpose()) + add_mat
            res_vec = np.dot(lmi, left)
            #  print(res_vec.reshape((m - 1,)))
            u[1:m][:][:, k + 1] = res_vec.reshape((m - 1,))  # 更新u矩阵
            res.append(res_vec)  # 返回值
        return np.array(res)

    @staticmethod
    def FrontEulaSingle_CPU(func, T, m, n, a, phi_x, alpha_tk, beta_tk, step=None):
        """
        显式差分
        :param func: 见上面
        :param T:
        :param m:
        :param n:
        :param step:
        :param a:
        :param phi_x:
        :param alpha_tk:
        :param beta_tk:
        :return:
        """
        res = []
        if step is None:
            step = n
        h = 1 / m
        tau = T / n
        r = a * tau / h ** 2
        if r > 0.5:
            raise SyntaxWarning("不稳定")  # 根据网格比确定稳定条件r<0.5
        vec_front = np.array([[phi_x(x / m) for x in range(m - 1)]]).transpose()
        mat = np.zeros((m - 1, m - 1))
        xx = np.array([y * 1 / m for y in range(m - 1)])
        t = np.array([y * T / n for y in range(n)])

        for x in range(1, m - 2):
            mat[x][x] = 1 - 2 * r
            mat[x][x + 1] = r
            mat[x + 1][x] = r
        mat[0][0] = 1 - 2 * r
        mat[m - 2][m - 2] = 1 - 2 * r
        mat[0][1] = r
        mat[1][0] = r
        mat[m - 2][m - 3] = r
        mat[m - 3][m - 2] = r
        for j in range(step):
            res_s = [tau * func(xx[0], t[j]) + r * alpha_tk(t[j])] + [tau * func(xx[i], t[j]) for i in
                                                                      range(1, m - 2)] + [
                        tau * func(xx[m - 2], t[j]) + r * beta_tk(t[j])]
            res_s = np.array([res_s]).transpose()
            vec_rear = np.dot(mat, vec_front) + res_s
            res.append(vec_rear)
            vec_front, vec_rear = vec_rear, np.zeros((1, m)).transpose()
        return np.array(res)

    @staticmethod
    def FrontEulaSingle_GPU(func, T, m, n, a, phi_x, alpha_tk, beta_tk, step=None):
        """
                显式差分
                :param func: 见上面
                :param T:
                :param m:
                :param n:
                :param step:
                :param a:
                :param phi_x:
                :param alpha_tk:
                :param beta_tk:
                :return:
                """
        res = []
        if step is None:
            step = n
        h = 1 / m
        tau = T / n
        r = a * tau / h ** 2
        if r > 0.5:
            raise SyntaxWarning("不稳定")
        vec_front = np.array([[phi_x(x / m) for x in range(m - 1)]]).transpose()
        mat = np.zeros((m - 1, m - 1))  # 迭代的三对角矩阵初始化
        xx = np.array([y * 1 / m for y in range(m - 1)])  # 空间序列（M）初始化
        t = np.array([y * T / n for y in range(n)])  # 空间序列（N）初始化

        def _get_add_vec(k):  # 生成每次迭代时等式右边的增加向量
            k = k - 1
            res_s = [tau * func(xx[0], t[k]) + r * alpha_tk(t[k])] + [tau * func(xx[i], t[k]) for i in
                                                                      range(1, m - 2)] + [
                        tau * func(xx[m - 2], t[k]) + r * beta_tk(t[k])]
            return np.array([res_s]).transpose()

        for x in range(1, m - 2):
            mat[x][x] = 1 - 2 * r
            mat[x][x + 1] = r
            mat[x + 1][x] = r
        mat[0][0] = 1 - 2 * r
        mat[m - 2][m - 2] = 1 - 2 * r
        mat[0][1] = r
        mat[1][0] = r
        mat[m - 2][m - 3] = r
        mat[m - 3][m - 2] = r
        for j in range(step):
            vec_rear = np.dot(mat, vec_front) + _get_add_vec(step)
            res.append(vec_rear)
            vec_front, vec_rear = vec_rear, np.zeros((1, m)).transpose()
        return np.array(res)

    @staticmethod
    def RK_Solve_CPU(func, a, b, h, y_0_value, step=None):
        """
        常微分方程数值解
        :param func: (a, b)
        :param h:划分的x点数
        :param y_0_value:
        :param step:
        :param a
        :param b:
        :return:
        """
        if step is None:
            step = h
            print(step)
        x = [(b - a) / step * y for y in range(step)]
        y = [0 for _ in range(step)]
        y[0] = y_0_value
        for i in range(step - 1):
            k1 = func(x[i], y[i])
            k2 = func(x[i] + h / 2, y[i] + h / 2 * k1)
            k3 = func(x[i] + h / 2, y[i] + h / 2 * k2)
            k4 = func(x[i] + h, y[i] + h * k3)
            y[i + 1] = y[i] + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        return y

    @staticmethod
    def RK_Solve_GPU(func, a, b, h, y_0_value, step=None):
        ...

    @staticmethod
    def CrankNicholsonComplex_GPU(func, T, m, n, a, para_lambda, para_miu, lambda_phi_x, lambda_alpha_tk,
                                  lambda_beta_tk,
                                  step=None):
        """
                混合边界条件下的求解(见书P80)
                :param func:
                :param T:
                :param m:
                :param n:
                :param step:
                :param a:
                :param para_lambda:
                :param lambda_phi_x:
                :param para_miu:
                :param lambda_alpha_tk:
                :param lambda_beta_tk:
                :return:
                """
        res = []
        if step is None:
            step = n
        h = 1 / m
        tau = T / n
        r = a * tau / h ** 2
        vec_front = np.array([[lambda_phi_x(x / m) for x in range(m + 1)]]).transpose()
        left_mat = np.zeros((m + 1, m + 1))
        right_mat = np.zeros((m + 1, m + 1))
        left_mat[0][0] = 1 + r + r * para_lambda * h
        left_mat[m][m] = 1 + r + r * para_miu * h
        left_mat[0][1] = -r
        left_mat[m][m - 1] = -r
        right_mat[0][1] = r
        right_mat[m][m - 1] = r
        right_mat[0][0] = 1 - r - r * para_lambda * h
        right_mat[m][m] = 1 - r - r * para_miu * h
        xx = np.array([y * 1 / m for y in range(m + 1)])
        t = np.array([y * T / n for y in range(n + 1)])

        def _get_add_vec_(_k):
            tk_half = (t[_k] + t[1 + _k]) / 2
            temp = np.array([[-r * h * lambda_alpha_tk(t[_k]) - r * h * lambda_alpha_tk(t[_k + 1]) + tau * func(xx[0],
                                                                                                                tk_half)] + [
                                 tau * func(xx[ii], tk_half) for ii in range(1, m)] + [
                                 r * h * lambda_beta_tk(_k) + r * h * lambda_beta_tk(_k + 1) * tau * func(xx[m],
                                                                                                          tk_half)]]).transpose()

            return temp

        for x in range(1, m):
            left_mat[x][x] = 1 + r
            right_mat[x][x] = 1 - r
            left_mat[x][x + 1] = -r / 2
            left_mat[x][x - 1] = -r / 2
            right_mat[x][x + 1] = r / 2
            right_mat[x][x - 1] = r / 2
        lmi = inv(left_mat)
        for i in range(step):
            vec_rear = np.dot(lmi, (np.dot(right_mat, vec_front) + _get_add_vec_(i)))
            res.append(vec_rear)
            vec_rear, vec_front = np.zeros((1, m)).transpose(), vec_rear
        return np.array(res)

    @staticmethod
    def CrankNicholsonComplex_CPU(func, T, m, n, a, para_lambda, para_miu, lambda_phi_x, lambda_alpha_tk,
                                  lambda_beta_tk,
                                  step=None):
        """
        混合边界条件下的求解(见书P80)
        :param func:
        :param T:
        :param m:
        :param n:
        :param step:
        :param a:
        :param para_lambda:
        :param lambda_phi_x:
        :param para_miu:
        :param lambda_alpha_tk:
        :param lambda_beta_tk:
        :return:
        """
        res = []
        if step is None:
            step = n
        h = 1 / m
        tau = T / n
        r = a * tau / h ** 2
        vec_front = np.array([[lambda_phi_x(x / m) for x in range(m + 1)]]).transpose()
        left_mat = np.zeros((m + 1, m + 1))
        right_mat = np.zeros((m + 1, m + 1))
        left_mat[0][0] = 1 + r + r * para_lambda * h
        left_mat[m][m] = 1 + r + r * para_miu * h
        left_mat[0][1] = -r
        left_mat[m][m - 1] = -r
        right_mat[0][1] = r
        right_mat[m][m - 1] = r
        right_mat[0][0] = 1 - r - r * para_lambda * h
        right_mat[m][m] = 1 - r - r * para_miu * h
        xx = np.array([y * 1 / m for y in range(m + 1)])
        t = np.array([y * T / n for y in range(n + 1)])

        def _get_add_vec_(_k):
            tk_half = (t[_k] + t[1 + _k]) / 2
            temp = np.array([[-r * h * lambda_alpha_tk(t[_k]) - r * h * lambda_alpha_tk(t[_k + 1]) + tau * func(xx[0],
                                                                                                                tk_half)] + [
                                 tau * func(xx[ii], tk_half) for ii in range(1, m)] + [
                                 r * h * lambda_beta_tk(_k) + r * h * lambda_beta_tk(_k + 1) * tau * func(xx[m],
                                                                                                          tk_half)]]).transpose()

            return temp

        for x in range(1, m):
            left_mat[x][x] = 1 + r
            right_mat[x][x] = 1 - r
            left_mat[x][x + 1] = -r / 2
            left_mat[x][x - 1] = -r / 2
            right_mat[x][x + 1] = r / 2
            right_mat[x][x - 1] = r / 2
        lmi = inv(left_mat)
        for i in range(step):
            vec_rear = np.dot(lmi, (np.dot(right_mat, vec_front) + _get_add_vec_(i)))
            res.append(vec_rear)
            vec_rear, vec_front = np.zeros((1, m)).transpose(), vec_rear
        return np.array(res)

    @staticmethod
    def LaxWenderoff(a, lambda_phi_x):
        ...


#if __name__ == "__main__":
   # a = solve.CrankNicholsonComplex_CPU(func=lambda x, t: 1, T=1, m=10, n=10, a=1, para_lambda=1,
                              #          para_miu=1, lambda_phi_x=lambda x: 1, lambda_alpha_tk=lambda x: 1,
                                    #    lambda_beta_tk=lambda x: 1,
                                     #   step=None)
   # print(a)
