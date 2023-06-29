import pandas as pd
from tqdm import tqdm


def decodeDayWeek(day: str):
    """
    It takes a string as input and returns an integer
    
    :param day: The day of the week
    :type day: str
    :return: The day of the week.
    """
    if day == 'Monday':
        return 2
    elif day == 'Tuesday':
        return 3
    elif day == 'Wednesday':
        return 4
    elif day == 'Thursday':
        return 5
    elif day == 'Friday':
        return 6
    elif day == 'Saturday':
        return 7
    elif day == 'Sunday':
        return 8

def decodeTime(data):
    """
    It takes a dataframe, and returns a list of the hour of the day for each row in the dataframe
    
    :param data: the dataframe
    :return: A list of the hour of the day that the call was made.
    """
    timeRange = []
    for i in tqdm(range(len(data['Thời điểm gọi']))):
        timeRange.append(data['Thời điểm gọi'][i].hour)
    return timeRange

def labelEncoder(data):
    """
    It takes a dataframe as input, and returns a list of integers
    
    :param data: The dataframe that contains the data
    :return: A list of 0 and 1
    """
    encoderLabel = []
    for i in tqdm(range(len(data['Result']))):
        if data['Result'][i] == 'Không thành công' or data['Result'][i] == 'Lỗi':
            encoderLabel.append(0)
        elif data['Result'][i] == 'Nghe máy':
            encoderLabel.append(1)
    return encoderLabel

def encodeProduct(data):
    """
    It takes the column 'PRODUCT' from the dataframe 'data' and encodes it into a list of integers
    
    :param data: The dataframe that contains the column to be encoded
    :return: A list of integers
    """
    encoder = []
    for i in tqdm(range(len(data['PRODUCT']))):
        if data['PRODUCT'][i] == 'Cash Loan':
            encoder.append(0)
        elif data['PRODUCT'][i] == 'TOPUP - XSELL':
            encoder.append(1)
        elif data['PRODUCT'][i] == 'CONSUMER DURABLE LOAN':
            encoder.append(2)
        elif data['PRODUCT'][i] == 'TWO-WHEEL LOAN':
            encoder.append(3)
        elif data['PRODUCT'][i] == 'SERVICE PACKAGE LOAN':
            encoder.append(5)
    return encoder

def encodeProductInference(data):
    if data== 'Cash Loan':
        return 0
    elif data == 'TOPUP - XSELL':
        return 1
    elif data == 'CONSUMER DURABLE LOAN':
        return 2
    elif data == 'TWO-WHEEL LOAN':
        return 3
    elif data == 'SERVICE PACKAGE LOAN':
        return 5