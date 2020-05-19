from network.DataMapHelper import DataMapHelper


class FCMComputer:

    def __init__(self):
        self.data_map_helper = DataMapHelper.getInstance()
        self.fcm_points = {}
        for belong in self.data_map_helper.belong:
            self.fcm_points[belong] = self.__load_fcm_point(belong)

    def __load_fcm_point(self, belong):



        return []

    def compute(self, data_dic):
        pass