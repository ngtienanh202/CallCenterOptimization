import os
from flask import Flask
from flask_restful import Api
import pandas as pd
from src.Api.Optimize import Optimizer

app = Flask(__name__)
api = Api(app)

parser = requestParser()

api.add_resource()

if __name__ == "__main__":
    database = pd.read_csv('data/TotalData.csv')
    xgbModel = pickle.load(open('model/24-12/xgb.sav', 'rb'))
    port = os.environ['PORT']
    if (port == None):
        port == 4000
    app.run(debug=False, port = port)