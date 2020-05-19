from datahelper.utils import *


class TableLoader:
    """
    表格处理的基类，也提供默认的处理办法
    """

    def __init__(self):
        self.load_name = 'table_loader'  # 这个值来判断是否是对应装载器，使用对应的装载器去读取对应的表格
        self.segment_name = {}  # 这个对象用来储存在展开后每一个段指向的字段

    def load(self, table):
        """
        每张表的数据的处理情况很可能不同，使用这个方法来对表格数据进行最初的处理
        :param table: 把表格中的数据读入后，进行第一层的处理，而后交给DataFilter类处理
        :return: 简单处理过后的表单数据
        """
        for key in table:
            if key == 'key':
                continue
            elif key == 'entname':
                continue
            elif key in ignore_set:
                continue
            data = table[key]
            for i, x in enumerate(data):
                try:
                    data[i] = round(float(x), 4)
                except ValueError:
                    data[i] = self.solve_unaccept_value(x, key)
            table[key] = data

        return table

    def describe(self, table):
        """
        在load完并且进行过滤后进行加工数据的方法，使用这个方法来展开数据等
        :param table: 由DataLoader load后的数据
        :return: 把数据展开成(n, m)形状返回
        """
        sorted(table.keys())
        data = {}
        company = table['entname']
        is_segment_init = False
        segment_list = []
        for i in range(len(company)):
            tmp = []
            for key in table:
                if key == 'entname' or key == 'key':
                    continue
                elif key in ignore_set:
                    continue
                else:
                    if not is_segment_init:
                        segment_list.append(key)
                    tmp.append(table[key][i])
            is_segment_init = True
            data[company[i]] = tmp

        self.segment_name[table['key']] = segment_list

        return data

    def solve_unaccept_value(self, value, key):
        """
        因为输入数据可能是空值等情况，使用这个函数来处理对应的空值情况
        :param value:
        :param key:
        :return:
        """
        value = 0
        return value
