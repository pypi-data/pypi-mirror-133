import os
from warnings import warn

import pandas as pd


class file_base(object):  # 数据导入导出基类
    def __init__(self, path, res):
        self.path = path
        self.res = res
        self.pd_res = pd.DataFrame(self.res)  # 用pandas处理运行结果，便于导出

    def to_csv(self, csv_name):
        """
        导出为CSV格式
        :param csv_name:
        :return:
        """
        res = []
        if self.res is None:
            warn(Warning("没有进行运算，导出结果为空"))
        if ".csv" not in csv_name:  # 没有后缀名则加上
            csv_name += ".csv"
        for x in self.res:
            res.append(x.transpose()[0])
        self.pd_res = pd.DataFrame(res)

        with open(csv_name, "w+") as csv:
            self.pd_res.to_csv(csv)
            print("导出成功， 路径为{}".format(os.getcwd()) + csv_name)  # 提示导出成功

    def to_xls(self, xls_name, xls_path, xls_sheet):
        ...

    def to_dict(self):
        self.pd_res = pd.DataFrame(self.res)
        self.pd_res.to_dict()


class plot_base(object):

    @staticmethod
    def plot(*args, **kwargs):
        import matplotlib.pyplot as plt
        plt.plot(*args, **kwargs)
        plt.show()
