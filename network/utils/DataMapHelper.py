from local.datahelper.Utils import *


class DataMapHelper:

    def __init__(self):
        self.belong = ["target_credit", "target_technique", "target_construction", "target_comsize", "target_strength",
                       "target_stable"]

    @staticmethod
    def getInstance():
        return data_map_helper


data_map_helper = DataMapHelper()
