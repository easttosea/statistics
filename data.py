# -*- coding: utf-8 -*-
import datetime
import pandas as pd
import logging


class Statistics(object):
    def __init__(self):
        self.normal_delivery_order = None
        self.credit_delivery_order = None
        self.initial_position = {}
        self.date = datetime.date(2015, 1, 1)
        self.normal_position = None
        self.normal_cash = None

    def read_delivery_order(self):
        self.normal_delivery_order = pd.read_csv('a.csv', encoding='GBK')
        self.credit_delivery_order = pd.read_csv('b.csv', encoding='GBK')
        self.normal_delivery_order['成交日期'] = [datetime.datetime.strptime(str(date_str), '%Y%m%d').date() for
                                              date_str in self.normal_delivery_order['成交日期']]
        self.normal_delivery_order['证券代码'] = ['{0:0>6s}'.format(str(code_str)) for code_str in
                                              self.normal_delivery_order['证券代码']]
        contract_number = []
        for row in self.normal_delivery_order.iterrows():
            operation = row[1]['摘要']
            if '基金' in operation:
                contract_number.append(row[1]['合同编号'] + 100000)
            else:
                contract_number.append(row[1]['合同编号'])
        self.normal_delivery_order.合同编号 = contract_number
        self.normal_delivery_order = self.normal_delivery_order.sort_values(by=['成交日期', '合同编号'])
        self.normal_delivery_order = self.normal_delivery_order.set_index('成交日期')

    def get_position(self):
        normal_position = {'600010': ['包钢股份', 5500], '600506': ['香梨股份', 10000],
                           '600737': ['中粮屯河', 17000], '600583': ['海油工程', 9300]}
        normal_cash = 1500000
        normal_position_list = []
        normal_cash_list = []
        for row in self.normal_delivery_order.iterrows():
            date = row[0]
            # 追加持仓列表、现金列表数据
            while date > self.date:
                for code in normal_position:
                    normal_position_list.append([self.date, code, normal_position[code][0], normal_position[code][1]])
                normal_cash_list.append([self.date, normal_cash])
                self.date = self.date + datetime.timedelta(days=1)
            # 改变持仓信息
            operation = row[1]['摘要']
            code = row[1]['证券代码']
            name = row[1]['证券名称']
            volume = row[1]['成交数量']
            amount = row[1]['发生金额']
            if operation in ['证券买入', '证券卖出', '质押回购拆出', '拆出质押购回']:
                try:
                    normal_position[code][1] += volume
                    normal_cash += amount
                    if normal_position[code][1] == 0:
                        normal_position.pop(code)
                    elif normal_position[code][1] < 0:
                        logging.error('持仓为负  交易情况：{0},{1},{2},{3},{4}股  交易后持仓：{5}股'.format(
                                date, operation, code, name, volume, normal_position[code][1]))
                except KeyError:
                    normal_position[code] = [name, volume]
                    normal_cash += amount
                if normal_cash < 0:
                    logging.error('现金为负  交易情况：{0},{1},{2},{3},{4}股,{5}元  交易后现金：{6}元'.format(
                            date, operation, code, name, volume, amount, normal_cash))

#            if operation in ['证券买入', '证券卖出', '担保品划入', '担保品划出', '红股入帐', '新股入帐',
#                             '基金分拆', '基金合并', '开放基金赎回', '托管转出', '托管转入', 'ETF赎回基金过户']:
#                try:
#                    normal_position[code][1] += volume
#                    if normal_position[code][1] == 0:
#                        normal_position.pop(code)
#                    elif normal_position[code][1] < 0:
#                        print(date, operation, code, name, volume, normal_position[code][1])
#                except KeyError:
#                    normal_position[code] = [name, volume]

        self.normal_position = pd.DataFrame(normal_position_list, columns=['日期', '证券代码', '证券名称', '数量'])
        self.normal_cash = pd.DataFrame(normal_cash_list, columns=['日期', '现金'])
        writer = pd.ExcelWriter('statistics.xlsx')
        self.normal_position.to_excel(writer, sheet_name='普通帐户-证券')
        self.normal_cash.to_excel(writer, sheet_name='普通帐户-现金')


def main():
    my_statistics = Statistics()
    my_statistics.read_delivery_order()
    my_statistics.get_position()


if __name__ == '__main__':
    main()
