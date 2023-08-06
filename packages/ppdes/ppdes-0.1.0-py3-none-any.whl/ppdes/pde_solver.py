from ppdes.err import *
from ppdes.solver import *


class Pde(err_manager, object):
    def __init__(self, pde_class):
        """

        :param pde_class: pde类型
        """
        self.pde_class = str(pde_class)
        self.pde_solver = None
        self.params = None
        self.res = None
        self.error = None
        self.min_err = None
        self.ideal_data = None

    def get_error(self, min_err, mode=None):  # 设定并获取拟合误差
        self.min_err = min_err
        if mode is None:  # 设置默认误差形式为欧氏距离
            mode = "diff"
        return self.get_err(self.ideal_data, self.res, self.min_err, mode)

    def load_data(self, path):  # 加载理想数据
        with open(path, "r") as data:
            self.ideal_data = pd.read_csv(data).to_numpy()

    def pde_solver_init(self, **kwargs):  # 根据选择初始化求解器
        self.params = kwargs
        if self.pde_solver is not None:  # 初始化过了则跳过
            return self.pde_solver
        try:
            kwargs.pop("plot")  # 导入求解参数
            kwargs.pop("plot")  # 导入求解参数
        except:
            pass
        if self.pde_class == "<class 'ppdes.solver.C_K_single'>":  # 分别遍历各种情况，选择求解器
            try:
                solver_type = "C_K_single"
                self.pde_solver = C_K_single(**kwargs)
            except:
                raise ValueError(
                    "请检查参数输入格式是否正确，必须为{}".format(
                        "func, T, m, n, a, phi_x, alpha_tk, beta_tk, step=None（可不选）, cuda=False（可不选）"))
        elif self.pde_class == "<class 'ppdes.solver.C_K_complex'>":
            try:
                solver_type = "C_K_complex"
                self.pde_solver = C_K_complex(**kwargs)
            except:
                raise ValueError(
                    "请检查参数输入格式是否正确，必须为{}".format(
                        "func, T, m, n, a, para_lambda, para_miu, lambda_phi_x, lambda_alpha_tk, lambda_beta_tk,step=None（可不选）, cuda=False（可不选）"))
        elif self.pde_class == "<class 'ppdes.solver.front_eula_para'>":
            try:
                solver_type = "front_eula_para"
                self.pde_solver = front_eula_para(**kwargs)
            except:
                raise ValueError(
                    "请检查参数输入格式是否正确，必须为{}".format(
                        "func, T, m, n, a, phi_x, alpha_tk, beta_tk, step=None, cuda=False"))
        elif self.pde_class == "<class 'ppdes.solver.quad_R_k'>":
            try:
                solver_type = "quad_R_k"
                self.pde_solver = quad_R_k(**kwargs)
            except:
                raise ValueError(
                    "请检查参数输入格式是否正确，必须为{}".format(
                        "func, a, b, h, y_0_value, step=None, cuda=False"))
        else:
            raise ValueError("输入有误")
        print("求解器已经设置为{}".format(solver_type))

    def solve(self):
        """
        单个参数求解
        :return:
        """
        self.res = self.pde_solver.solve()

    def set_paras(self, **kwargs):
        self.params.update(kwargs)
        self.pde_solver_init(**self.params)

    def to_csv(self, csv_name, **kwargs):  # 导出成CSV文件
        self.pde_solver.to_csv(csv_name, **kwargs)

    def __str__(self):
        if self.res is not None:
            return str(self.res)
        else:
            return str(self.params)

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, item):
        return self.res[item]

