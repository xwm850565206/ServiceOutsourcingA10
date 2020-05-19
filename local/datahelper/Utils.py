import numpy as np

ignore_set = {
    # 这是我认为不需要的参数，后面可能还要改
    # company_baseinfo
    'candate', 'revdate', 'opto', 'opfrom',

    # change_info
    'remark', 'dataflag', 'altitem', 'cxstatus', 'altdate', 'openo',

    # ent_contribution
    'comform', 'subconam', 'condate',

    # ent_contribution_year
    'subconcurrency', 'accondate', 'subconform', 'anchetype', 'subcondate',
    'acconcurrency', 'acconform', 'liacconam', 'lisubconam',

    # ent_insurance
    'cbrq', 'sbjgbh', 'xzbzmc', 'cbzt', 'dwbh',

    # justice_declare
    'declaredate',

    # justice_enforced
    'record_date', 'enforce_amount', 'case_no',

    # justice_judge_new
    'time', 'title', 'casetype', 'judgeresult', 'casecause', 'evidence',
    'courtrank', 'datatype', 'latypes',

    # jn_special_new_info
    # 'is_jnsn'

    # ent_social_security
    'updatetime'
}

# 美元和欧元的汇率，有些企业是外资的，也有可能是以外币结算的，这里我还没深入了解
DOLLAR_TO_RMB = 7.0215
EURO_TO_RMB = 7.6324

# 公司信用字段
target_credit = [
    'passpercent', 'is_kcont', 'credit_grade', 'is_justice_credit', 'is_justice_creditaic'
]
target_credit_weight = {
    'passpercent': 1.0, 'is_kcont': 3.0, 'credit_grade': 2.0, 'is_justice_credit': 3.0,
    'is_justice_creditaic': 3.0
}

# 公司技术字段
target_technique = [
    'ibrand_num', 'icopy_num', 'ipat_num', 'idom_num', 'is_jnsn'
]

target_technique_weight = {
    'ibrand_num': 0.25, 'icopy_num': 0.25, 'ipat_num': 0.25, 'idom_num': 0.25,
    'is_jnsn': 2.0
}

# 公司构成字段
target_construction = [
    'enttype', 'entcat', 'industryphy',
    'inv0', 'inv1', 'inv2', 'inv3', 'inv4', 'inv5', 'inv6', 'inv7', 'inv8', 'inv9', 'inv10', 'inv11', 'inv12',
    'inv13', 'inv14', 'inv15',
    'xzbz0', 'xzbz1', 'xzbz2', 'xzbz3', 'xzbz4', 'xzbz5', 'xzbz6', 'xzbz7', 'xzbz8',
    'regcapcur', 'investnum'
]

target_construction_weight = {
    'enttype': 1.0, 'entcat': 1.0, 'industryphy': 1.0,
    'inv': 1/16, 'xzbz': 1/9, 'regcapcur': 1.0, 'investnum': 1.0
}

# 公司规模字段
target_comsize = [
    'regcap', 'empnum', 'estdate', 'branchnum', 'shopnum', 'qcwynum', 'zhycnum', 'zlzpnum'
]

target_comsize_weight = {
    'regcap': 1.0, 'empnum': 1.0, 'estdate': 1.0, 'branchnum': 0.5, 'shopnum': 0.5,
    'qcwynum': 0.33, 'zhycnum': 0.33, 'zlzpnum': 0.33
}

# 公司实力字段
target_strength = [
    'bidnum', 'qcwynum', 'zhycnum', 'zlzpnum', 'is_infoa', 'is_infob', 'passpercent'
]

target_strength_weight = {
    'bidnum': 1.0, 'qcwynum': 0.33, 'zhycnum': 0.33, 'zlzpnum': 0.33,
    'is_infoa': 2.0, 'is_infob': 2.0, 'passpercent': 1.0
}

# 公司稳定字段 企业年报对外担保还未添加 todo
target_stable = [
    'alttime', 'defendant_num', 'is_bra', 'is_brap', 'pledgenum', 'taxunpaidnum', 'is_except',
    'unpaidsocialins_so110', 'unpaidsocialins_so210', 'unpaidsocialins_so310', 'unpaidsocialins_so410',
    'unpaidsocialins_so510'
]

target_stable_weight = {
    'alttime': 1.0, 'defendant_num': 1.0, 'is_bra': 0.25, 'is_brap': 0.25, 'pledgenum': 0.5, 'taxunpaidnum': 1.0,
    'is_except': 0.5,
    'unpaidsocialins_so110': 0.2, 'unpaidsocialins_so210': 0.2, 'unpaidsocialins_so310': 0.2,
    'unpaidsocialins_so410': 0.2, 'unpaidsocialins_so510': 0.2
}

# 有些字段的距离不是单纯的相减
binary_segment = {
    'regcapcur', 'entstatus', 'enttype', 'entcat', 'industryphy'
}


def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def dic_ignore(key):
    if key in ignore_set:
        return True
    return False


def file_set_filter(file_set_name):
    """
    因为有的参数和他的文件名不对应，这里需要做一个转换
    :param file_set_name: 转换的参数名
    :return:对应的文件名
    """

    if file_set_name == 'enterprise_onlineshop':
        return 'ent_onlineshop'
    elif file_set_name == 'enterprise_branch':
        return 'ent_branch'
    elif file_set_name == 'enterprise_contribution':
        return 'ent_contribution'
    elif file_set_name == 'enterprise_contribution_year':
        return 'ent_contribution_year'
    elif file_set_name == 'enterprise_guarantee':
        return 'ent_guarantee'
    elif file_set_name == 'enterprise_investment':
        return 'ent_investment'
    elif file_set_name == 'operation_bid':
        return 'ent_bid'
    elif file_set_name == 'enterprise_social_security':
        return 'ent_social_security'
    elif file_set_name == 'business_risk__quality_check':
        return 'product_checkinfo_connect'
    elif file_set_name == 'business_risk__abnormal':
        return 'business_risk_abnormal'
    elif file_set_name == 'business_risk__all_punish':
        return 'business_risk_all_punish'
    elif file_set_name == 'business_risk__rightpledge':
        return 'business_risk_rightpledge'
    elif file_set_name == 'business_risk__taxunpaid':
        return 'business_risk_taxunpaid'
    else:
        return file_set_name


def generate_segment_name_file(dataloader):
    with open("segment_dic.txt", 'w') as file:

        loader_set = dataloader.loader
        for loader in loader_set:
            for key in loader.segment_name:
                file.write('# ' + key + '\n')
                for segment in loader.segment_name[key]:
                    file.write(segment)
                    file.write(' ')
                file.write('\n')


def get_target_segment_data(dataloader, target_name):
    """
    切分公司数据，得到对应要打标签的数据
    :param dataloader: 初始化后得到二维数组数据的 DataLoader
    :param target_name: 有六种选项 分别是 target_credit, target_technique, target_construction,
    target_comsize, target_strength, target_stable
    :return: data 要使用聚类的数据 是 (n, m) 形状的二维数组, n是n个公司， m是字段总数
             sub_segment_name, 每一列对应的字段名
    """
    target_set = None
    if target_name == 'target_credit':
        target_set = target_credit
    elif target_name == 'target_technique':
        target_set = target_technique
    elif target_name == 'target_construction':
        target_set = target_construction
    elif target_name == 'target_comsize':
        target_set = target_comsize
    elif target_name == 'target_strength':
        target_set = target_strength
    elif target_name == 'target_stable':
        target_set = target_stable
    else:
        return None
    data = []
    for target_segment in target_set:
        index = dataloader.segment_list.index(target_segment)
        if index is None:
            print("没有找到字段:", target_segment)  # 正常情况下应该都能够找到的
            continue
        if isinstance(index, list):
            for i in index:
                data.append(dataloader.company_data[:, i])
        else:
            data.append(dataloader.company_data[:, index])

    data = np.array(data)
    data = data.T
    print("拆分完毕，数据形状为:", data.shape)

    return data, target_set


if __name__ == '__main__':
    a = [[1, 2, 3], [4, 5, 6]]
    a = np.array(a)
    b = [a[:, 0], a[:, 1], a[:, 2]]
    b = np.array(b)
    print(b)
    b = b.T
    print(b)
