from datahelper import utils


class DataFilter:

    def __init__(self, is_init_dic, prefix=''):
        self.weight_dic = self._generate_weight()
        self.prefix = prefix

        if is_init_dic:
            self.init_dic = self.load_init_dic()
        else:
            self.init_dic = None

    def filter(self, data):
        return data

    def load_init_dic(self):
        init_dic = {}
        filename = self.prefix + 'init_dic.txt'
        with open(filename, 'r') as file:
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
