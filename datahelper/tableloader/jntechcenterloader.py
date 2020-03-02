from datahelper.tableloader.tableloader import TableLoader


class JnTechCenterLoader(TableLoader):
    """
    这个类处理了level_rank关键字，因为大部分的企业的rank都是0，这个的权重应该要很高
    """
    def __init__(self):
        super().__init__()
        self.load_name = 'jn_tech_center'

    def load(self, table):
        level_rank = table['level_rank']

        for i, level in enumerate(level_rank):

            if level == '省级':
                level_rank[i] = 2
            elif level == '市级':
                level_rank[i] = 1
            else:
                level_rank[i] = 0

        table['level_rank'] = level_rank
        return table

    def solve_unaccept_value(self, value, key):

        if key == 'level_rank':
            value = 0

        return value