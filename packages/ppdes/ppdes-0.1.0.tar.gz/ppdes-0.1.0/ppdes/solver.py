from ppdes.base import *
from ppdes.diffsolve import solve

NOW_PATH = os.getcwd()


class C_K_complex(solve, plot_base, object):
    """
    调用CK方法解决混合边界条件下的抛物线微分方程数值解
    """

    def __init__(self, func, T, m, n, a, para_lambda, para_miu, lambda_phi_x, lambda_alpha_tk, lambda_beta_tk,
                 step=None, cuda=False):
        """
        :param func:
        :param T:
        :param m:
        :param n:
        :param a:
        :param para_lambda:
        :param para_miu:
        :param lambda_phi_x:
        :param lambda_alpha_tk:
        :param lambda_beta_tk:
        以上参数见黄色书籍
        :param step: 是否运行到最大步长（时间为T，空间为x = 1）
        :param cuda: 是否启用cuda加速（2000*2000以下可能会降低效率）
        """
        super().__init__(step)
        assert callable(lambda_phi_x), "lambda_phi_x应输入lambda表达式"
        assert callable(lambda_alpha_tk), "lambda_alpha_tk应输入lambda表达式"
        assert callable(lambda_beta_tk), "lambda_beta_tk应输入lambda表达式"

        self.step = step if self is not None else 1000
        self.func = func
        self.T = T
        self.m = m
        self.n = n
        self.a = a
        self.lam = para_lambda
        self.miu = para_miu
        self.phi = lambda_phi_x
        self.alpha_tk = lambda_alpha_tk
        self.bet_tk = lambda_beta_tk
        self.res = None
        self.cuda = cuda
        self.file = file_base(path=None, res=self.res)
        self.plotter = plot_base()
        self.C_K_complex = True

    def __str__(self):  # 打印此时结果
        return self.res

    def __repr__(self):
        return self.__str__()

    def solve(self, step=None):  # 根据此时参数求解微分方程
        if self.cuda is False:
            self.res = self.CrankNicholsonComplex_CPU(func=self.func, T=self.T, m=self.m, n=self.n, a=self.a,
                                                      lambda_phi_x=self.phi, lambda_alpha_tk=self.alpha_tk,
                                                      lambda_beta_tk=self.bet_tk, para_lambda=self.lam,
                                                      para_miu=self.miu,
                                                      step=None)
        else:
            if self.m < 2000 or self.n < 2000:
                warn(Warning("小于2000*2000启用cuda加速的运算效率可能低于cpu运算"))
            self.res = self.CrankNicholsonComplex_GPU(func=self.func, T=self.T, m=self.m, n=self.n, a=self.a,
                                                      lambda_phi_x=self.phi, lambda_alpha_tk=self.alpha_tk,
                                                      lambda_beta_tk=self.bet_tk, para_lambda=self.lam,
                                                      para_miu=self.miu,
                                                      step=step)
        self.file.res = self.res
        return self.res

    def set_step(self, step):  # 设置步长
        self.step = step

    def to_csv(self, csv_name):  # 各种导出数据，利用file_base功能
        self.file.to_csv(csv_name)

    def to_xls(self, xls_path, xls_name, sheet):
        self.file.res = self.res
        self.file.to_xls(xls_name=xls_name, xls_path=xls_path, xls_sheet=sheet)

    def to_dict(self):
        self.file.res = self.res
        return self.file.to_dict()

    def plot(self, *args, **kwargs):
        self.plot(*args, **kwargs)


class C_K_single(solve, object):
    def __init__(self, func, T, m, n, a, phi_x, alpha_tk, beta_tk, step=None, cuda=False):
        """
        第一类边界条件
        :param func:
        :param T:
        :param m:
        :param n:
        :param a:
        :param phi_x:
        :param alpha_tk:
        :param beta_tk:
        :param step:
        :param cuda:
        """
        super().__init__(step)
        assert callable(phi_x), "phi_x必须是lambda表达式"
        assert callable(alpha_tk), "alpha_tk必须是lambda表达式"
        assert callable(beta_tk), "beta_tk必须是lambda表达式"
        self.func = func
        self.T = T
        self.m = m
        self.n = n
        self.a = a
        self.step = step
        self.cuda = cuda
        self.res = None
        self.phi_x = phi_x
        self.alpha_tk = alpha_tk
        self.beta_tk = beta_tk
        self.file = file_base(path=None, res=self.res)
        self.plotter = plot_base()
        self.C_K_single = True

    def solve(self):
        if self.cuda is False:
            self.res = self.CrankNicholsonSingle_CPU(self.func, self.T, self.m, self.n, self.a, phi_x=self.phi_x,
                                                     alpha_tk=self.alpha_tk,
                                                     beta_tk=self.beta_tk)
        else:
            if self.m < 2000 or self.n < 2000:
                warn(Warning("小于2000*2000启用cuda加速的运算效率可能低于cpu运算"))
            self.CrankNicholsonSingle_GPU(self.func, self.T, self.m, self.n, self.a, phi_x=self.phi_x,
                                          alpha_tk=self.alpha_tk,
                                          beta_tk=self.beta_tk)
        self.file.res = self.res
        return self.res

    def __str__(self):
        return self.res

    def __repr__(self):
        return self.__str__()

    def set_step(self, step):
        self.step = step

    def to_csv(self, csv_name):
        self.file.res = self.res
        self.file.to_csv(csv_name)

    def to_xls(self, xls_path, xls_name, sheet):
        self.file.res = self.res
        self.file.to_xls(xls_name=xls_name, xls_path=xls_path, xls_sheet=sheet)

    def to_dict(self):
        self.file.res = self.res
        return self.file.to_dict()

    def plot(self, *args, **kwargs):
        self.plot(*args, **kwargs)


class front_eula_para(solve, object):

    def __init__(self, func, T, m, n, a, phi_x, alpha_tk, beta_tk, step=None, cuda=False):
        """
        使用向前欧拉法求解抛物线微分方程(具体参数见黄色书)
        :param func:
        :param T:
        :param m:
        :param n:
        :param a:
        :param phi_x:
        :param alpha_tk:
        :param beta_tk:
        :param step:
        :param cuda:
        """
        assert callable(phi_x), "phi_x必须是lambda表达式"
        assert callable(alpha_tk), "alpha_tk必须是lambda表达式"
        assert callable(beta_tk), "beta_tk必须是lambda表达式"
        super().__init__(step)
        self.func = func
        self.T = T
        self.m = m
        self.n = n
        self.a = a
        self.phi_x = phi_x
        self.alpha_tk = alpha_tk
        self.beta_tk = beta_tk
        self.step = step
        self.cuda = cuda
        self.res = None
        self.file = file_base(path=None, res=self.res)
        self.plotter = plot_base()
        self.front_eula_para = True

    def __str__(self):
        return self.res

    def __repr__(self):
        return self.__str__()

    def solve(self):
        if self.cuda is False:
            self.res = self.FrontEulaSingle_CPU(func=self.func, T=self.T, m=self.m, n=self.n, a=self.a,
                                                phi_x=self.phi_x, alpha_tk=self.alpha_tk, beta_tk=self.beta_tk,
                                                step=None)
        else:
            if self.m < 2000 or self.n < 2000:
                warn(Warning("小于2000*2000启用cuda加速的运算效率可能低于cpu运算"))
            self.res = self.FrontEulaSingle_GPU(func=self.func, T=self.T, m=self.m, n=self.n, a=self.a,
                                                phi_x=self.phi_x, alpha_tk=self.alpha_tk, beta_tk=self.beta_tk,
                                                step=None)
        self.file.res = self.res
        return self.res

    def set_step(self, step):
        self.step = step

    def to_csv(self, csv_name):
        self.file.to_csv(csv_name)

    def to_xls(self, xls_path, xls_name, sheet):
        self.file.to_xls(xls_name=xls_name, xls_path=xls_path, xls_sheet=sheet)

    def to_dict(self):
        return self.file.to_dict()

    def plot(self, *args, **kwargs):
        self.plot(*args, **kwargs)


class quad_R_k(solve, object):
    def __init__(self, func, a, b, h, y_0_value, step=None, cuda=False):
        super().__init__()
        self.func = func
        self.a = a
        self.b = b
        self.h = h
        self.y0_value = y_0_value
        self.step = step
        self.cuda = cuda
        self.res = None
        self.file = file_base(path=None, res=self.res)
        self.plotter = plot_base()

        self.front_eula_para = True

    def __str__(self):
        return self.res

    def __repr__(self):
        return self.__str__()

    def solve(self):
        if self.cuda is False:
            self.res = self.RK_Solve_CPU(func=self.func, a=self.a, b=self.b, h=self.h, y_0_value=self.y0_value,
                                         step=self.step)
        else:
            if self.h < 10000:
                warn(Warning("小于2000*2000启用cuda加速的运算效率可能低于cpu运算"))
            self.res = self.RK_Solve_GPU(func=self.func, a=self.a, b=self.b, h=self.h, y_0_value=self.y0_value,
                                         step=self.step)
        self.file.res = self.res
        return self.res

    def set_step(self, step):
        self.step = step

    def to_csv(self, csv_name):
        """
        导出CSV
        :param csv_name:
        :return:
        """

        self.file.res = self.res
        self.file.to_csv(csv_name)

    def to_xls(self, xls_path, xls_name, sheet):
        """
        导出 XLS
        :param xls_path:
        :param xls_name:
        :param sheet:
        :return:
        """
        self.file.res = self.res
        self.file.to_xls(xls_name=xls_name, xls_path=xls_path, xls_sheet=sheet)

    def to_dict(self):
        """
        导出dict
        :return:
        """
        self.file.res = self.res
        return self.file.to_dict()

    def plot(self, *args, **kwargs):
        self.plot(*args, **kwargs)
