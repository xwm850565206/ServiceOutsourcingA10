from datahelper.tableloader.tableloader import TableLoader


class JusticeDeclareLoader(TableLoader):
    """
    返回的是 entname，defendant_num，
    defendant_num 为这个企业一共成为被告的次数
    """
    def __init__(self):
        super().__init__()
        self.load_name = 'justice_declare'

    def load(self, table):

        defendant = table['defendant']
        company = table['entname']
        data = {}
        result = {}

        for i, name in enumerate(company):
            if name in data:
                data[name] += int(defendant[i])
            else:
                data[name] = int(defendant[i])
        defendant = []
        company = []
        for key in data:
            company.append(key)
            defendant.append(data[key])

        result['entname'] = company
        result['defendant_num'] = defendant
        result['key'] = table['key']
        return result
