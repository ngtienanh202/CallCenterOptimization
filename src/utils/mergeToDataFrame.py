import pandas as pd
import tqdm as tqdm

def merge_data(export_dir, import_dir):

    df_After_Merge = pd.DataFrame(columns=['STT', 'CallID', 'Số khách hàng', 'Hotline', 'Thời điểm gọi',
        'Thời lượng gọi', 'Trạng thái', 'Mã tổng đài', 'Mã kết thúc bot',
        'Action', 'ASR Process (ms)', 'Bot Process (ms)', 'TTS Process (ms)',
        'Time in call', 'User Say', 'Intent', 'Độ tự tin (%)', 'Entities',
        'Entity Value', 'QC Độ trễ', 'QC User Say', 'QC Intent',
        'Đánh giá Intent', 'Tỷ lệ nhận diện STT', 'Đánh giá STT', 'Audio',
        'Đơn giá', 'CUSTOMER', 'AGREEMENTID', 'CURRES_PHONE', 'CUSTOMER',
        'AGREEMENTID', 'PRODUCT', 'AMOUNT_FINANCE', 'TENURE', 'DUEDAY',
        'CURRES_PHONE', 'MAX_DPD', 'MOB', 'DISBURSALDATE', 'PHONE_REF1',
        'NAME_1', 'RELATIONSHIP_1', 'PHONE_REF2', 'NAME_2', 'RELATIONSHIP_2',
        'PHONE_REF3', 'NAME_3', 'RELATIONSHIP_3', 'GENDER', 'NC',
        'FIRST_PAID_DATE', 'REMAINING_PEROID', 'DPD', 'PERMNENT_PROVINCE'])

    dfex = pd.read_excel(export_dir)
    
    dfim = pd.read_excel(import_dir)
    
    dfim = dfim.drop('Unnamed: 0',axis=1)
    lista = list(dfex['AGREEMENTID'])
    listb = list(dfim['AGREEMENTID'])
    for row_index_ex in tqdm(range(0,len(lista))):
        try:
            item = lista[row_index_ex]
            row_index_im = listb.index(item)
        
            df_temp = pd.concat([dfex.iloc[row_index_ex],dfim.iloc[row_index_im]])
            
            df_After_Merge = df_After_Merge.append(df_temp, ignore_index = True)
        except:
            print('FAIL')
            continue

    return df_After_Merge

def build_merge_data(exportlist_in_xlsx,importlist_in_xlsx):
    df_After_Merge = pd.DataFrame(columns=['STT', 'CallID', 'Số khách hàng', 'Hotline', 'Thời điểm gọi',
        'Thời lượng gọi', 'Trạng thái', 'Mã tổng đài', 'Mã kết thúc bot',
        'Action', 'ASR Process (ms)', 'Bot Process (ms)', 'TTS Process (ms)',
        'Time in call', 'User Say', 'Intent', 'Độ tự tin (%)', 'Entities',
        'Entity Value', 'QC Độ trễ', 'QC User Say', 'QC Intent',
        'Đánh giá Intent', 'Tỷ lệ nhận diện STT', 'Đánh giá STT', 'Audio',
        'Đơn giá', 'CUSTOMER', 'AGREEMENTID', 'CURRES_PHONE', 'CUSTOMER',
        'AGREEMENTID', 'PRODUCT', 'AMOUNT_FINANCE', 'TENURE', 'DUEDAY',
        'CURRES_PHONE', 'MAX_DPD', 'MOB', 'DISBURSALDATE', 'PHONE_REF1',
        'NAME_1', 'RELATIONSHIP_1', 'PHONE_REF2', 'NAME_2', 'RELATIONSHIP_2',
        'PHONE_REF3', 'NAME_3', 'RELATIONSHIP_3', 'GENDER', 'NC',
        'FIRST_PAID_DATE', 'REMAINING_PEROID', 'DPD', 'PERMNENT_PROVINCE'])

    for exportfile in tqdm(exportlist_in_xlsx):
        exportfilename = str(exportfile)
        exportfile_arr = exportfilename.split('_')[4].split('.')[0]
        date = exportfile_arr
        
        for import_file in importlist_in_xlsx:
            if(import_file.find(str(date)) > 0):
               
                
                print("len of data merge: " + str(len(df_After_Merge)))
                df_merge = merge_data(exportfile,import_file)
                df_After_Merge = pd.concat([df_After_Merge,df_merge])
    return df_After_Merge


def format_time(minutes):
    hours_total = minutes // 60
    # Get additional minutes with modulus
    minutes_total = minutes % 60
    # Create time as a string
    if int(minutes_total) < 10 :
        time_string = "{}h0{}".format(hours_total, minutes_total)
    else:
        time_string = "{}h{}".format(hours_total, minutes_total)
    return time_string