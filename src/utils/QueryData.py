import pandas as pd
from src.utils.encodeData import encodeProductInference
from datetime import datetime
from tqdm import tqdm
from calendar import monthrange

def GetPhone(data, Phone):
    """
    It takes in a dataframe and a phone number, and returns a list of indices of the dataframe where the
    phone number matches the input phone number
    
    :param data: the dataframe
    :param Phone: The phone number you want to search for
    :return: A list of indices where the value of the column CURRES_PHONE is equal to the value of the
    variable Phone.
    """
    listPhone = []
    for i in range(len(data['CURRES_PHONE'])):
        if int(data['CURRES_PHONE'][i]) == int(Phone):
            listPhone.append(i)
    return listPhone

def GetIndex(data, id):
    """
    It takes in a dataframe and an ID number, and returns a list of indices where the ID number is found
    in the dataframe
    
    :param data: the dataframe
    :param id: The ID of the agreement you want to get the index of
    :return: A list of indices where the AGREEMENTID is equal to the id.
    """
    listID = []
    for i in range(len(data['AGREEMENTID'])):
        if int(data['AGREEMENTID'][i]) == int(id):
            listID.append(i)
    return listID

def GetListCallInDay(day, historyCall, database):
    """
    This function returns a list of call indexes in a day and the total number of calls in that day
    
    :param day: the day you want to get the list of calls
    :param historyCall: list of all call history
    :param database: the database that you want to get the list of calls in a day
    :return: ListCallInDay is a list of index of historyCall in database.
    """
    ListCallInDay = []
    TotalCount = 0
    for i in tqdm(range(len(historyCall))):
        if int(database['Thời điểm gọi'][historyCall[i]].day) == int(day):
            ListCallInDay.append(historyCall[i])
            TotalCount = TotalCount + 1
    return ListCallInDay, TotalCount

def GetNumberSuccessInDay(listCallInDays, database):
    """
    This function takes in a list of indices of calls in a day and a database, and returns a list of
    indices of successful calls in that day and the total number of successful calls in that day
    
    :param listCallInDays: list of indices of calls in a day
    :param database: the dataframe that contains all the data
    :return: listIndexSuccess is a list of index of the successful calls in the listCallInDays.
    TotalSuccess is the total number of successful calls in the listCallInDays.
    """
    listIndexSuccess = []
    TotalSuccess = 0
    for i in tqdm(range(len(listCallInDays))):
        if database['Result'][listCallInDays[i]] == 1:
            listIndexSuccess.append(listCallInDays[i])
            TotalSuccess = TotalSuccess + 1 
    return listIndexSuccess, TotalSuccess

def HowManyCallInTime(listCallInDays, database, time,  threshhold = 15, isSuccess = False):
    listIndexInTime = []
    TotalIntime = 0
    for i in tqdm(range(len(listCallInDays))):
        if time in range((int(database['TimeCall'][listCallInDays[i]]) - threshhold), (int(database['TimeCall'][listCallInDays[i]]) + threshhold)):
            listIndexInTime.append(listCallInDays[i])
            TotalIntime = TotalIntime + 1
    if isSuccess == True:
        return listIndexInTime, TotalIntime
    else:
        return listIndexInTime

# def HowManySuccessInTime(listIndexInTime, database):
#     listSuccessInTime = []
#     TotalSuccessInTime = []
#     for i in tqdm(range(len(listIndexInTime))):
#         if database['Result']['lios']

def SearchInfor(data, index, NCIndex):
    """
    This function takes in the dataframe, the index of the row, and the index of the NC column, and
    returns the phone number, product, and NC
    
    :param data: the dataframe
    :param index: the index of the dataframe
    :param NCIndex: the index of the NC in the NC list
    :return: Phone, Product, Nc
    """
    Phone = data['CURRES_PHONE'][index]
    Product = encodeProductInference(data['PRODUCT'][index])
    Nc = data['NC'][NCIndex]
    return Phone, Product, Nc

def checkNumberDayRemaining():
    """
    It returns the current day, the number of days in the current month, and the current month
    :return: The current day, the number of days in the current month, and the current month.
    """
    currentDay = datetime.date(datetime.now()).day
    currentYear = datetime.date(datetime.now()).year
    currentMonth = datetime.date(datetime.now()).month
    allDayInMonth = monthrange(int(currentYear), int(currentMonth))[1]
    return currentDay, allDayInMonth, currentMonth

def GetMinute(data ,i):
    """
    It takes in a dataframe and an index, and returns the minute of the call
    
    :param data: the dataframe
    :param i: the index of the row you want to get the data from
    :return: The minute of the call
    """
    Additions =data['Thời điểm gọi'][i].minute
    return Additions