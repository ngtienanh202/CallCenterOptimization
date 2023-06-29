import pandas as pd
from tqdm import tqdm
from datetime import datetime, date
import pickle
from time import time
from src.utils import libSort
import calendar
from datetime import datetime as dpa
from calendar import monthrange
from src.utils.convert_data_type import convertList, convertToHour
from src.utils.QueryData import GetPhone, checkNumberDayRemaining, SearchInfor, GetMinute, GetIndex
from src.utils.mergeToDataFrame import format_time
from flask_restful import Resource
from flask import jsonify
import time
from flask_restful import reqparse

database = pd.read_csv('data/TotalData.csv')
xgbModel = pickle.load(open('model/24-12/xgb.sav', 'rb'))

parser = reqparse.requestParser()
parser.ad_arguments('id')
def convertPhone(database):
    listPhone = []
    for i in tqdm(range(len(database['CURRES_PHONE']))):
        if str(database['CURRES_PHONE'][i]) == "nan":
            listPhone.append(0)
        else:
            listPhone.append(int(database['CURRES_PHONE'][i]))
    return listPhone
def encodeTimeCall(data):
    listEncode = []
    for i in tqdm(range(len(data['Thời điểm gọi']))):
        a = dpa.strptime(data['Thời điểm gọi'][i], '%Y-%m-%d %H:%M:%S')
        listEncode.append(a)
    return listEncode
def convertToTime(data):
    hourToCall = []
    for i in tqdm(range(len(data['Thời điểm gọi']))):
        hourToCall.append(convertToHour(data, i))
    return hourToCall
listTimeEncode = []
for i in tqdm(range(len(database['TimeCall']))):
    listTimeEncode.append(int(int(database['TimeCall'][i]) * 60) + GetMinute(database, i))
database['TimeCall'] = listTimeEncode
database.rename(columns = {'Trạng thái':'Result'}, inplace = True)
def labelEncoder(data):
    encoderLabel = []
    for i in tqdm(range(len(data['Result']))):
        if data['Result'][i] == 'Không thành công' or data['Result'][i] == 'Lỗi':
            encoderLabel.append(0)
        elif data['Result'][i] == 'Nghe máy':
            encoderLabel.append(1)
    return encoderLabel

database['CURRES_PHONE'] = convertPhone(database)
database['Thời điểm gọi'] = encodeTimeCall(database)
database['TimeCall'] = convertToTime(database)
database['Result'] = labelEncoder(database)

class Optimizer(Resource):
    def post(self):
        args = parser.parser_args()
        if args['id'] != None:
            start = time.time()
            listID = GetIndex(data= database, id= listAgreedmentID)
            Phone, Product, Nc = SearchInfor(data= database, index= listID[0], NCIndex= listID[-1])
            NowDay, LimitInMonth, NowMonth = checkNumberDayRemaining()
            whatInsideToModel = [[Phone, Product, Nc]]
            listResult = pd.DataFrame()
            for i in tqdm(range(len(whatInsideToModel))):
                for j in range(NowDay, LimitInMonth + 1):
                    perCent = []
                    listTimeAvailabel = []
                    for k in tqdm(range(480, 12001, 15)):
                        preds = xgbModel.predict_proba([[whatInsideToModel[i][0],
                                                        whatInsideToModel[i][1],
                                                        whatInsideToModel[i][2],
                                                        k,
                                                        j,
                                                        NowMonth]])
                        preds = preds.tolist()
                        perCent.append(preds[0][1])
                        listTimeAvailabel.append(k)
                    whenIsGoodTime = libSort.nlargest(10,zip(perCent, listTimeAvailabel))
                    whenIsGoodTime = convertList(whenIsGoodTime)
                    StandardScaleTime = []
                    for ff in range(len(whenIsGoodTime)):
                        HereWeLive = (f"{round(float(whenIsGoodTime[ff][0] * 100),3)}", whenIsGoodTime[ff][1])
                        StandardScaleTime.append(HereWeLive)
                    DayinWeeks = date(year= datetime.date(datetime.now()).year,
                                        month=NowMonth,
                                        day= int(j))
                    listResult[f'{j}/{NowMonth}/{datetime.date(datetime.now()).year} - {calendar.day_name[DayinWeeks.weekday()]}'] = StandardScaleTime