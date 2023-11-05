import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from datetime import date, timedelta, datetime
from pathlib import Path
from typing import Self
import pickle
import csv

# from app.domain.service import CurrencyService, GoldService


class CommodityPredictor:
    data_file = 'pull.csv'
    x_train = None
    y_train = None
    x_test = None
    y_test = None
    model = None

    def prepare_data(self) -> Self:
        df1 = pd.read_csv(self.data_file, delimiter=',')
        x = df1.iloc[:, 1:].values
        y = df1.iloc[:, 0].values
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=42)
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        return self

    def train(self) -> Self:
        regressor = LinearRegression()
        regressor.fit(self.x_train, self.y_train)
        self.model = regressor
        return self

    def test_model(self) -> Self:
        y_prediction = self.model.predict(self.x_test)
        np.set_printoptions(precision=2)
        print(f'{self.model.coef_ = }')
        print(f'{self.model.intercept_ = }')
        print('PREDICTED | REAL')
        print(np.concatenate((y_prediction.reshape(len(y_prediction), 1), self.y_test.reshape(len(y_prediction), 1)), axis=1))
        return self

    def save_to_file(self, filename) -> Self:
        with open(filename, 'wb') as f:
            pickle.dump(self.model, f)
        return self

    def load_from_file(self, filename) -> Self:
        with open(filename, 'rb') as f:
            self.model = pickle.load(f)
        return self

    def predict(self, date: str):
        return self.model.predict([[int(date.replace('-', ''))]])


class GoldPredictor(CommodityPredictor):
    def __init__(self):
        super().load_from_file(Path().cwd().joinpath('app/infrastructure/ml/model/gold_model.pkl'))

    # TODO this leads to a circular import error so I have to figure out another way
    # def gather_data(self) -> Self:
    #     step = int(timedelta(days=80).total_seconds())
    #     with open(self.data_file, mode='w') as file:
    #         writer = csv.DictWriter(file, fieldnames=["value", "date"])
    #         writer.writeheader()
    #         for stamp in range(int(datetime(year=2020, month=1, day=1).timestamp()),
    #                            int((datetime.today() - timedelta(days=80)).timestamp()),
    #                            step):
    #             for pull in GoldService().pull_gold_from_api(
    #                     date_begin=date.fromtimestamp(stamp).strftime("%Y-%m-%d"),
    #                     date_end=date.fromtimestamp(stamp + step).strftime("%Y-%m-%d")
    #             ).get_gold():
    #                 writer.writerow({'value': pull['cena'], 'date': int(pull['data'].replace('-', ''))})
    #     return self
