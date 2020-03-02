
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
    'courtrank', 'datatype', 'latypes'
    
    # jn_special_new_info
    'is_jnsn'
}

# 美元和欧元的汇率，有些企业是外资的，也有可能是以外币结算的，这里我还没深入了解
DOLLAR_TO_RMB = 7.0215
EURO_TO_RMB = 7.6324


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


if __name__ == '__main__':
    pass
