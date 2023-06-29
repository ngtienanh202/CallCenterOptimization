from tqdm import tqdm
from datetime import datetime
from src.utils.encodeData import decodeDayWeek
import datetime


def convertStrtoDate(data_exportlist):
    """
    It takes a dataframe as input, and returns a list of datetime objects
    
    :param data_exportlist: the dataframe that contains the column of dates
    :return: A list of datetime objects
    """
    listEncode = []
    for i in tqdm(range(len(data_exportlist['Thời điểm gọi']))):
        data_exportlist['Thời điểm gọi'][i] = datetime.strptime(data_exportlist['Thời điểm gọi'][i], '%Y-%m-%d %H:%M:%S')
        listEncode.append(data_exportlist['Thời điểm gọi'][i])
    return listEncode

def convertToDayWeek(data_exportlist, i):
    """
    It takes in a dataframe and an index, and returns the day of the week of the date in the dataframe
    at that index
    
    :param data_exportlist: the dataframe that contains the data
    :param i: the index of the row in the dataframe
    :return: The day of the week
    """
    intday = datetime.date(year= data_exportlist['Thời điểm gọi'][i].year, 
                            month= data_exportlist['Thời điểm gọi'][i].month, 
                            day= data_exportlist['Thời điểm gọi'][i].day).weekday()
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return decodeDayWeek(days[intday])

def convertToHour(data_exportlist, i):
    """
    This function takes in a dataframe and an index, and returns the hour of the day of the call
    
    :param data_exportlist: the dataframe that contains the data
    :param i: the index of the row in the dataframe
    :return: The hour of the call
    """
    inthour = data_exportlist['Thời điểm gọi'][i].hour
    return inthour

def convertToDayMonth(data_exportlist, i):
    """
    This function takes in a dataframe and an index, and returns the day of the month of the date in the
    dataframe at that index
    
    :param data_exportlist: the dataframe that contains the data
    :param i: the index of the row in the dataframe
    :return: The day of the month of the call.
    """
    indate = data_exportlist['Thời điểm gọi'][i].day
    return indate

def convertToMonthYear(data_exportlist, i):
    """
    This function takes in a dataframe and an index, and returns the month of the date in the dataframe
    at that index
    
    :param data_exportlist: the dataframe that contains the data
    :param i: the index of the row in the dataframe
    :return: The month of the call
    """
    inmonth = data_exportlist['Thời điểm gọi'][i].month
    return inmonth

def convertList(listInlist):
    newList = []
    for i in range(len(listInlist)):
        newList.append(list(listInlist[i]))
    return newList