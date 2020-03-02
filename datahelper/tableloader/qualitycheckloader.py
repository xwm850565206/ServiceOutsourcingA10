from datahelper.tableloader.tableloader import TableLoader


class QualityCheckLoader(TableLoader):
    """
    对原来表格里的数据进行处理，返回的是 entname，passpercent
    passpercent进行了空值的补全和0值处理，使用的是均值补全
    """

    def __init__(self):
        super().__init__()
        self.load_name = 'product_checkinfo_connect'
        self.avg_percent = 1

    def load(self, table):

        passpercent = table['passpercent']
        passpercent = [round(float(x), 4) for x in passpercent]
        self.cal_avg_percent(passpercent)

        for i, percent in enumerate(passpercent):
            if percent == 0 or percent is None:
                passpercent[i] = self.avg_percent

        table['passpercent'] = passpercent
        return table

    def solve_unaccept_value(self, value, key):
        if key == 'passpercent':
            value = self.avg_percent
        else:
            value = super().solve_unaccept_value(value, key)

        return value

    def cal_avg_percent(self, percent_set):

        sum_percent = 0
        cnt = 0
        for percent in percent_set:
            if percent != 0:
                sum_percent += percent
                cnt += 1

        if cnt != 0:
            self.avg_percent = sum_percent / cnt
            self.avg_percent = round(self.avg_percent, 4)
