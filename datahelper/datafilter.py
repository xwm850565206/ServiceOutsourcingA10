from datahelper import utils
import numpy as np


def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range


def standardization(data):
    mu = np.mean(data, axis=0)
    sigma = np.std(data, axis=0)
    return (data - mu) / sigma


class DataFilter:

    def __init__(self, is_init_dic, prefix=''):
        self.weight_dic = self._generate_weight()
        self.prefix = prefix

        if is_init_dic:
            self.init_dic = self.load_init_dic()
        else:
            self.init_dic = None

    def filter(self, data):
        """
        在个性化装载完以及修饰完后调用，负责数据的包装
        :param data: 一个字典，包含 key:表格名称 还有表格所包含的字段
        :return: 过滤，加权以及归一化后的数据
        """

        for key in data:
            if key == 'key':
                continue
            elif key == 'entname':
                continue

            raw_data = data[key]
            raw_data = np.array(raw_data)
            raw_data = standardization(raw_data)
            raw_data = normalization(raw_data)
            if key in self.weight_dic:
                raw_data = raw_data * self.weight_dic[key]
            data[key] = raw_data

        return data

    def load_init_dic(self):
        init_dic = {}
        filename = self.prefix + 'init_dic.txt'
        with open(filename, 'r', encoding='UTF-8') as file:
            cur_key = ''
            while True:
                line = file.readline()
                line = line.replace('\n', '')
                if line is None or line == '':
                    break
                if utils.is_Chinese(line):
                    tmp = line.split(' ')
                    tmp = set([x for x in tmp if x != ''])
                    init_dic[cur_key] = tmp
                else:
                    cur_key = line

        return init_dic

    @staticmethod
    def _generate_weight():
        weight_dic = {}
        return weight_dic


if __name__ == '__main__':
    datafilter = DataFilter(is_init_dic=True)

    print(datafilter.init_dic)
