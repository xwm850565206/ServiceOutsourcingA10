import json


class FCMPoint:

    def __init__(self, cluster, vectors, segments):
        self.cluster = cluster
        self.segments = segments  # 形状为(1, n) 的list
        self.vectors = vectors  # 形状为(cluster, len(segments))的list，每一列对应segment对应序号的值

        self.vector_to_label = {}  # 不一定有，这个要在文件里写，属于手动定义的范畴

    def toFileFormat(self):
        data_dic = {'cluster': self.cluster, 'vectors': self.vectors, 'segments': self.segments}
        return json.dump(data_dic)

    @staticmethod
    def toFCMPoint(self, file_string):
        """
        从文件中读取他的信息
        :param self:
        :param file_string: 文件内容
        :return:
        """
        data_dic = json.loads(file_string)
        return FCMPoint(data_dic['cluster'], data_dic['vectors'], data_dic['segments'])

    @staticmethod
    def distance(self, veca, vecb):
        assert len(veca) == len(vecb)

        dis = 0
        for i in range(len(veca)):
            dis += (veca[i] - vecb[i]) ** 2
        return dis

    def getLabel(self, data):
        """
        得到对应的标签
        :param data:形状是[{key, data}, {key, dadta}, ...]
        :return: 标签
        """
        # todo
        return None
