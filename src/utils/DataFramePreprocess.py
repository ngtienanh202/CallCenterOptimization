import pandas as pd
from tqdm import tqdm

def drop_columns_by_list(data, list_columns):
    """
    This function takes in a dataframe and a list of columns to drop, and returns a dataframe with the
    columns dropped
    
    :param data: the dataframe you want to drop columns from
    :param list_columns: list of columns to be dropped
    :return: A dataframe with the columns in the list dropped.
    """
    if type(data) is pd.core.frame.DataFrame:
        for i in tqdm(range(len(data.columns))):
            if data.columns[i] == 'AGREEMENTID':
                primaryKey = data['AGREEMENTID']
                pass
        data = data.drop(columns = list_columns)
        return data, primaryKey
    else:
        raise TypeError("This data type is incorrect")

def drop_component_duplicate(data):
    """
    This function takes in a dataframe and drops the duplicate rows
    
    :param data: This is the dataframe that you want to drop duplicates from
    :return: A dataframe with no duplicates
    """
    if type(data) is pd.core.frame.DataFrame:
        data = data.drop_duplicates(ignore_index= True)
        return data
    else:
        raise TypeError("This data type is incorrect")

def drop_out_lier(data):
    """
    It takes in a dataframe and returns a dataframe with the outliers dropped
    
    :param data: the dataframe that we want to clean
    :return: A dataframe with outliers removed
    """
    rmv_index_list = []
    call_status = list(data['Mã tổng đài'])
    bot_detail = list(data['Mã kết thúc bot'])
    status = list(data['Trạng thái'])
    for i in range(0,len(call_status)):
        if call_status[i] == 'VOICEMAIL_DETECTION':
            if bot_detail[i] == 'DEFAULT_FALL':
                rmv_index_list.append(i)
    for i in range(0,len(status)):
        if status[i] == 'Lỗi':
            rmv_index_list.append(i)
    
    rmv_index_list = list(set(rmv_index_list))

    for i in range(0, len(rmv_index_list)):
        data = data.drop(axis = 0, index = rmv_index_list[i])

    return data

def drop_duplicates(data):
    """
    This function takes in a dataframe and returns a dataframe with duplicates dropped
    
    :param data: The dataframe you want to clean
    :return: The dataframe with the duplicates dropped.
    """
    data = data.drop_duplicates()
    return data