import pandas as pd


class Statistics(object):
    def __init__(self):
        self.normal_delivery_order = None
        self.credit_delivery_order = None

    def read_delivery_order(self):
        self.normal_delivery_order = pd.read_csv('a.csv', encoding='GBK')
        self.credit_delivery_order = pd.read_csv('b.csv', encoding='GBK')
        print(self.normal_delivery_order)
        print(self.credit_delivery_order)

    def get_position(self):
        pass


