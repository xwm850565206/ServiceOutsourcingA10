from datahelper.dataloader import DataLoader
from datahelper.tableloader.companyinfoloader import CompanyInfoLoader
from datahelper.tableloader.changeinfoloader import ChangeInfoLoader
from datahelper.tableloader.entcontributeloader import EntContributeLoader
from datahelper.tableloader.entinsuranceloader import EntInsuranceLoader
from datahelper.tableloader.jncreditinfoloader import JnCreditInfoLoader
from datahelper.tableloader.jntechcenterloader import JnTechCenterLoader
from datahelper.tableloader.qualitycheckloader import QualityCheckLoader
from datahelper.tableloader.justicedeclareloader import JusticeDeclareLoader
from datahelper.tableloader.tableloader import TableLoader
import numpy as np

if __name__ == '__main__':
    loader = EntContributeLoader('../datahelper/')
    # loader = EntInsuranceLoader()
    # dataloader = DataLoader(is_init_dic=True, prefix='../datahelper/', load_set=[loader.load_name])
    #
    # test_data = dataloader.get_table_by_name(loader.load_name)
    #
    # print(test_data)
    # print(dataloader.get_loader_bu_name(loader.load_name).segment_name)
    dataloader = DataLoader(is_init_dic=True, prefix='../datahelper/')

    data = dataloader.company_data
    data = np.array(data)
    print(data.shape)

    # a = np.zeros((5, ))
    # b = np.ones((5, ))
    # print(a)
    # for i in range(5):
    #     a[i] = b[i]
    #
    # print(a)
