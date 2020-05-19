import numpy as np
from datahelper import datainfo
from datahelper import datafilter
from datahelper import utils
from datahelper.tableloader.companyinfoloader import CompanyInfoLoader
from datahelper.tableloader.changeinfoloader import ChangeInfoLoader
from datahelper.tableloader.entcontributeloader import EntContributeLoader
from datahelper.tableloader.entinsuranceloader import EntInsuranceLoader
from datahelper.tableloader.jncreditinfoloader import JnCreditInfoLoader
from datahelper.tableloader.jntechcenterloader import JnTechCenterLoader
from datahelper.tableloader.qualitycheckloader import QualityCheckLoader
from datahelper.tableloader.justicedeclareloader import JusticeDeclareLoader
from datahelper.tableloader.tableloader import TableLoader

import csv


class DataLoader:

    def __init__(self, is_init_dic, prefix='', load_set=None, filter_func='standard'):
        self.is_init_dic = is_init_dic

        self.data_info = datainfo.DataInfo(prefix)
        self.data_filter = datafilter.DataFilter(is_init_dic, prefix=prefix)
        self.loader = [
            TableLoader(),  # 默认的装载器
            CompanyInfoLoader(prefix=prefix), ChangeInfoLoader(), EntContributeLoader(prefix=prefix),
            EntInsuranceLoader(), JnCreditInfoLoader(), JnTechCenterLoader(),
            JusticeDeclareLoader(), QualityCheckLoader()
        ]

        self.filedir = prefix + self.data_info.filedir + '/Data_FCDS_hashed'
        self.filter_func = filter_func
        self.data = self.load(load_set)

        self.company_list = self.get_company_list()
        self.segment_list = []
        self.company_data = self.generate_company_data()  # 生成聚类需要的形状
        self.segment_length = len(self.segment_list)
        self.shape = (len(self.company_list), self.segment_length)

        print("总数据形状为:", self.shape)

        if not is_init_dic:
            self.generate_init_dic()

    def load(self, file_set=None):

        if file_set is None:
            file_set = self.data_info.file_set

        data = []
        for key in file_set:
            data.append(self._load(utils.file_set_filter(key)))

        return data

    def _load(self, key):
        wb = csv.reader(open(self.filedir + '/' + key + '.csv', 'r', encoding='UTF-8'))
        ws = [x for x in wb]
        result_dic = {}

        print('load: ' + key)

        for index in range(len(ws[0])):
            _data = [x[index] for x in ws]  # 这里导入数据很冗余了，后面还是改改
            _key = _data[0]
            _data = _data[1:]

            result_dic[_key] = _data
            index += 1

        table_loader = self.get_loader_bu_name(key)

        result_dic['key'] = key  # 处理过程可能需要

        result_dic = table_loader.load(result_dic)  # 个性化装载
        result_dic = table_loader.describe(result_dic)  # 展开，修饰

        result_dic['key'] = key  # 防止处理后丢失

        return result_dic

    def generate_company_data(self):
        """
        生成(n, m)形状的数据，其中n是n个公司，m是m种字段，相当于对数据进行最后一次处理，这之后就可以用于计算了
        :return: company_data
        """
        print("begin to reshape and join all data")

        is_init_segment_list = False  # 生成数据的同时把每一列对应的字段也要初始化完毕
        company_data = [[] for i in range(len(self.company_list))]  # 生成(n, ?)形状的list，根据字段总数确定?
        for i, name in enumerate(self.company_list):
            company = []
            for table in self.data:
                table_loader = self.get_loader_bu_name(table['key'])
                segment_name = table_loader.segment_name[table['key']]
                if not is_init_segment_list:
                    self.segment_list.extend(segment_name)
                if name in table:
                    cur_data = table[name]
                    company.extend(cur_data)
                else:
                    tmp = []
                    for segment in segment_name:
                        tmp.append(table_loader.solve_unaccept_value(None, segment))
                    company.extend(tmp)
            company_data[i] = company
            is_init_segment_list = True

        company_data = np.array(company_data)
        company_data = self.data_filter.filter(company_data, self.segment_list, self.filter_func)

        print("finish join data")
        return company_data

    def generate_init_dic(self):
        """
        生成中文信息字典，用于参考和对照
        :return:
        """
        with open('init_dic.txt', 'w') as file:

            for table in self.data:
                for key in table:

                    if utils.dic_ignore(key):
                        continue

                    flag = False

                    data = table[key]
                    tmp_set = set()
                    for i in data:
                        if not flag and utils.is_Chinese(i):
                            flag = True
                        tmp_set.add(i)

                    if not flag:
                        continue

                    file.write(key)
                    file.write('\n')
                    for i in tmp_set:
                        file.write(str(i))
                        file.write(' ')
                    file.write('\n')

    def get_table_by_name(self, key):
        """
        按照表名获取表
        :param key:
        :return:
        """
        for table in self.data:
            if table['key'] == key:
                return table
        return None

    def get_loader_bu_name(self, load_name):
        """
        按照装载器名获取装载器
        :param load_name:
        :return:
        """
        for loader in self.loader:
            if loader.load_name == load_name:
                return loader
        return self.loader[0]  # 返回默认装载器

    def get_company_list(self):
        """
        统计出所有的公司
        :return: 所有在表格中出现过的公司名字
        """
        print("begin to generate company list")

        company_set = set()

        for table in self.data:
            for name in table:
                if name == 'key':
                    continue
                company_set.add(name)

        print("finish generate company list")

        return list(company_set)


if __name__ == '__main__':

    dataloader = DataLoader(is_init_dic=True)
    # data, sub_segment_name = utils.get_target_segment_data(dataloader, 'target_credit')
    #
    # print(sub_segment_name)
    # print(data)

    print(dataloader.segment_list)

    # print(dataloader.data)

