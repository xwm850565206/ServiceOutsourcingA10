from datahelper import utils
from datahelper.tableloader.tableloader import TableLoader
from datahelper.datafilter import DataFilter


class CompanyInfoLoader(TableLoader):
    """
    将company_baseinfo中的资金进行预处理和汇率转换
    """

    def __init__(self, prefix=''):
        super().__init__()
        self.load_name = 'company_baseinfo'
        self.data_filter = DataFilter(is_init_dic=True, prefix=prefix)
        self.currency = ['人民币', '美元', '欧元']

    def load(self, table):
        result = {}
        regcapcur = table['regcapcur']
        regcap = table['regcap']

        for i, x in enumerate(regcap):
            try:
                regcap[i] = round(float(x), 4)
            except ValueError:
                regcap[i] = self.solve_unaccept_value(regcap[i], 'regcap')

        for i, x in enumerate(regcapcur):

            if x == '' or x == None:
                regcapcur[i] = '人民币'
            elif x == '美元':
                regcap[i] = regcap[i] * utils.DOLLAR_TO_RMB
            elif x == '欧元':
                regcap[i] = regcap[i] * utils.EURO_TO_RMB

            if regcap[i] > 999:
                regcap[i] /= 1000  # 这里有个很大的问题，数据有的是万元 有的是元，现在姑且先这么处理

            regcapcur[i] = self.currency.index(regcapcur[i])

        result['regcapcur'] = regcapcur
        result['regcap'] = regcap

        entstatus = table['entstatus']
        entstatus_set = self.data_filter.init_dic['entstatus']
        entstatus_list = list(entstatus_set)
        for i, status in enumerate(entstatus):
            index = self.solve_unaccept_value(status, 'entstatus')
            if status != '':
                index = entstatus_list.index(status)
            entstatus[i] = index
        result['entstatus'] = entstatus

        enttype = table['enttype']
        enttype_set = self.data_filter.init_dic['enttype']
        enttype_list = list(enttype_set)
        for i, etype in enumerate(enttype):
            index = self.solve_unaccept_value(etype, 'enttype')
            if etype != '':
                index = enttype_list.index(etype)
            enttype[i] = index
        result['enttype'] = enttype

        entcat = table['entcat']
        entcat_set = self.data_filter.init_dic['entcat']
        entcat_list = list(entcat_set)
        for i, cat in enumerate(entcat):
            index = self.solve_unaccept_value(cat, 'entcat')
            if cat != '':
                index = entcat_list.index(cat)
            entcat[i] = index
        result['entcat'] = entcat

        industryphy = table['industryphy']
        industryphy_set = self.data_filter.init_dic['industryphy']
        industryphy_list = list(industryphy_set)
        for i, industry in enumerate(industryphy):
            index = self.solve_unaccept_value(industry, 'industryphy')
            if industry != '':
                index = industryphy_list.index(industry)
            industryphy[i] = index
        result['industryphy'] = industryphy

        empnum = table['empnum']
        for i, x in enumerate(empnum):
            try:
                empnum[i] = int(x)
            except ValueError:
                empnum[i] = self.solve_unaccept_value(x, 'empnum')
        result['empnum'] = empnum

        result['estdate'] = [round(float(x), 4) for x in table['estdate']]
        result['entname'] = table['entname']
        result['key'] = table['key']

        return result

    def solve_unaccept_value(self, value, key):

        if key == 'regcapcur':
            value = self.currency.index('人民币')
        elif key == 'regcap':  # 一般是吊销企业或者注销的，这里会出现空值，按照意思应该是用0补全
            value = 0
        elif key == 'entstatus':  # 要是数据缺失，默认是在营企业
            value = 2
        elif key == 'enttype':
            value = len(self.data_filter.init_dic['enttype'])  # 这个属性其实应该说是只有0和1的差异，聚类的时候不该用减法
        elif key == 'entcat':
            value = len(self.data_filter.init_dic['entcat'])
        elif key == 'industryphy':
            value = len(self.data_filter.init_dic['industryphy'])
        else:
            value = super().solve_unaccept_value(value, key)

        return value
