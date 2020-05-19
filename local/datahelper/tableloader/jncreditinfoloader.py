from datahelper.tableloader.tableloader import TableLoader


class JnCreditInfoLoader(TableLoader):
    """
    处理表中的信用等级，把等级转换为分数返回
    """

    def __init__(self):
        super().__init__()
        self.load_name = 'jn_credit_info'
        self.gradit_list = ['C', 'B-', 'A-', 'A', 'N', 'N+']  # 我不知道N到底是什么级别，这里把他排到最高级

    def load(self, table):
        credit_grade = table['credit_grade']

        for i, grade in enumerate(credit_grade):
            score = self.gradit_list.index(grade)
            credit_grade[i] = score

        table['credit_grade'] = credit_grade
        return table

    def solve_unaccept_value(self, value, key):
        if key == 'credit_grade':
            value = 2.5  # 平均等级
        return value

