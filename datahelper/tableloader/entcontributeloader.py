from datahelper.tableloader.tableloader import TableLoader
from datahelper.datafilter import DataFilter


class EntContributeLoader(TableLoader):
    """
    返回的是公司的每种股资类型以及占股比例
    """

    def __init__(self, prefix=''):
        super().__init__()
        self.load_name = 'ent_contribution'
        self.datafilter = DataFilter(is_init_dic=True, prefix=prefix)

    def load(self, table):

        data = {}
        sum_conam = {}
        sum_invtype = {}
        subconam = table['subconam']
        for i, x in enumerate(subconam):
            try:
                subconam[i] = round(float(x), 4)
            except ValueError:
                subconam[i] = self.solve_unaccept_value(x, 'subconam')

        company = table['entname']
        invtype = table['invtype']

        for i, name in enumerate(company):

            if name in sum_conam:
                sum_conam[name] += subconam[i]
            else:
                sum_conam[name] = subconam[i]

            if name in sum_invtype:
                if invtype[i] in sum_invtype[name]:
                    sum_invtype[name][invtype[i]] += subconam[i]
                else:
                    sum_invtype[name][invtype[i]] = subconam[i]
            else:
                sum_invtype[name] = {}
                sum_invtype[name][invtype[i]] = subconam[i]

        for name in sum_conam:
            for invtype in sum_invtype[name]:
                try:
                    sum_invtype[name][invtype] /= sum_conam[name]
                except ZeroDivisionError:
                    sum_invtype[name][invtype] = self.solve_unaccept_value(sum_conam[name], 'sum_conam')

        company = []
        inv = []
        invtype_set = self.datafilter.init_dic['invtype']
        invtype_list = list(invtype_set)

        for name in sum_invtype:
            company.append(name)
            type_set = [0 for i in range(len(invtype_list))]
            for invtype in sum_invtype[name]:
                if invtype != '':
                    index = invtype_list.index(invtype)
                    type_set[index] = sum_invtype[name][invtype]
            inv.append(type_set)
        data['entname'] = company
        data['inv'] = inv
        data['key'] = table['key']
        return data

    def describe(self, table):

        company = table['entname']
        inv = table['inv']
        data = {}

        for i, name in enumerate(company):
            data[name] = inv[i]

        self.segment_name[table['key']] = ['inv' for i in range(len(self.datafilter.init_dic['invtype']))]

        return data

    def solve_unaccept_value(self, value, key):
        if key == 'subconam':
            value = 0
        elif key == 'sum_conam':
            value = 1
        else:
            value = super().solve_unaccept_value(value, key)

        return value
