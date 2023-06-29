import pandas as pd



def data_import_processing():
    file_path = input("Please enter file path need process: ")
    data = pd.read_excel(file_path)
    data_input = data[['PRODUCT','CURRES_PHONE','NC']]
    agreement_id_list = data['AGREEMENTID']
    return data_input, agreement_id_list

