import pandas as pd
import pickle

xgb_reg = pickle.load(open("/home/ai_car/AthenaBow/model/xgb_reg2.sav", "rb"))
a = str(input("Please paste the path of file: "))
file = pd.read_excel(a)

for i in range()