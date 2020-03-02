from datahelper.tableloader.tableloader import TableLoader


class ChangeInfoLoader(TableLoader):
    """
    累加公司的变更次数
    """
    def __init__(self):
        super().__init__()
        self.load_name = 'change_info'

    def load(self, table):

        data = {}

        alttime = table['alttime']
        company = table['entname']

        for i, name in enumerate(company):
            tmp = 0
            try:
                tmp = int(alttime[i])
            except ValueError:
                tmp = 0
            if name in data:
                data[name] = data[name] + tmp
            else:
                data[name] = tmp
        alttime = []
        company = []

        for key in data:
            alttime.append(data[key])
            company.append(key)

        table['alttime'] = alttime
        table['entname'] = company

        return table



