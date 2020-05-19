from datahelper.tableloader.tableloader import TableLoader


class EntInsuranceLoader(TableLoader):
    """
    返回的是xzbz，一个公司的参保种类，是一个(1, 9)的01矩阵
    以及对应的entname
    """

    def __init__(self):
        super().__init__()
        self.load_name = 'enterprise_insurance'

    def load(self, table):

        xzbz = table['xzbz']
        cbztmc = table['cbztmc']
        company = table['entname']

        data = {}

        for i, name in enumerate(company):
            index = ord(xzbz[i]) - ord('A')
            if name in data:
                flag = (1 if cbztmc[i] == '参保缴费' else 0)
                data[name][index] = flag
            else:
                data[name] = [0 for i in range(9)]  # 这里应该是只有A~I 9 种

        xzbz = []
        company = []
        for name in data:
            company.append(name)
            xzbz.append(data[name])

        result = {'xzbz': xzbz, 'entname': company, 'key': table['key']}
        # table['xzbz'] = xzbz
        # table['entname'] = company
        return result

    def describe(self, table):

        sorted(table.keys())
        company = table['entname']
        xzbz = table['xzbz']
        data = {}

        for i, name in enumerate(company):
            data[name] = xzbz[i]

        self.segment_name[table['key']] = ['xzbz'+str(i) for i in range(9)]

        return data

    def solve_unaccept_value(self, value, key):

        if key == 'xzbz':
            value = 0
        else:
            value = super().solve_unaccept_value(value, key)

        return value

