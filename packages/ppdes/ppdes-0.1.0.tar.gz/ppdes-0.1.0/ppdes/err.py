class err_manager:

    def diff_mode(self, ideal_data, real_data, min_err):
        ...

    def abs_mode(self, ideal_data, real_data, min_err):
        ...

    def d_mode(self, ideal_data, real_data, min_err):
        ...

    def get_err(self, ideal_data, real_data, min_err, mode="diff"):
        """
        根据各种方法确定误差（默认为距离）
        :param ideal_data:
        :param real_data:
        :param min_err:
        :param mode:
        diff:欧氏距离
        dk :k阶中心距
        abs：绝对值

        :return:
        """
        ...
