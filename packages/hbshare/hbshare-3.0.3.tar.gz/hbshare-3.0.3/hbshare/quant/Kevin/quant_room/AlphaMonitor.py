"""
超额收益观测体系
"""
import hbshare as hbs
import pandas as pd
import numpy as np
import datetime


class AlphaMonitor:
    def __init__(self, trade_date, benchmark_id='000905'):
        self.trade_date = trade_date
        self.benchmark_id = benchmark_id
        self._load_data()

    @staticmethod
    def _load_shift_date(date):
        trade_dt = datetime.datetime.strptime(date, '%Y%m%d')
        pre_date = (trade_dt - datetime.timedelta(days=100)).strftime('%Y%m%d')

        sql_script = "SELECT JYRQ, SFJJ, SFZM, SFYM FROM funddb.JYRL WHERE JYRQ >= {} and JYRQ <= {}".format(
            pre_date, date)
        res = hbs.db_data_query('readonly', sql_script, page_size=5000)
        df = pd.DataFrame(res['data']).rename(
            columns={"JYRQ": 'calendarDate', "SFJJ": 'isOpen',
                     "SFZM": "isWeekEnd", "SFYM": "isMonthEnd"}).sort_values(by='calendarDate')
        df['isOpen'] = df['isOpen'].astype(int).replace({0: 1, 1: 0})
        df['isWeekEnd'] = df['isWeekEnd'].fillna(0).astype(int)
        df['isMonthEnd'] = df['isMonthEnd'].fillna(0).astype(int)

        trading_day_list = df[df['isMonthEnd'] == 1]['calendarDate'].tolist()

        return trading_day_list[-1]

    @staticmethod
    def _load_benchmark_components(date):
        sql_script = "SELECT * FROM hsjy_gg.SecuMain where SecuCategory = 4 and " \
                     "SecuCode in ('000300', '000905', '000852')"
        res = hbs.db_data_query('readonly', sql_script)
        index_info = pd.DataFrame(res['data'])
        inner_code_series = index_info.set_index('SECUCODE')['INNERCODE']

        weight = []
        for benchmark_id in ['000300', '000905', '000852']:
            inner_code = inner_code_series.loc[benchmark_id]
            sql_script = "SELECT (select a.SecuCode from hsjy_gp.SecuMain a where a.InnerCode = b.InnerCode and " \
                         "rownum = 1) SecuCode, b.EndDate, b.Weight FROM hsjy_gg.LC_IndexComponentsWeight b WHERE " \
                         "b.IndexCode = '{}' and b.EndDate = to_date('{}', 'yyyymmdd')".format(inner_code, date)
            data = pd.DataFrame(hbs.db_data_query('readonly', sql_script)['data'])
            weight_df = data.rename(
                columns={"SECUCODE": "ticker", "ENDDATE": "effDate", "WEIGHT": "weight"})
            weight_df['benchmark_id'] = benchmark_id
            weight.append(weight_df[['ticker', 'benchmark_id']])

        return pd.concat(weight)

    def _load_data(self):
        # 个股收益
        sql_script = "SELECT SYMBOL, SNAME, VOTURNOVER, PCHG FROM finchina.CHDQUOTE WHERE" \
                     " TDATE = {}".format(self.trade_date)
        data = pd.DataFrame(hbs.db_data_query('readonly', sql_script, page_size=5000)['data'])
        data = data[data['SYMBOL'].str[0].isin(['0', '3', '6'])]
        data = data[data['VOTURNOVER'] > 1e-8]
        data = data[~data['SNAME'].str.contains('ST')]
        data = data[~data['SNAME'].str.contains('N')]
        data = data[~data['SNAME'].str.contains('C')]
        market_df = data.rename(
            columns={"SYMBOL": "ticker", 'PCHG': "return"})[['ticker', 'return']].dropna()
        # 指数收益
        trade_dt = datetime.datetime.strptime(self.trade_date, '%Y%m%d')
        pre_date = (trade_dt - datetime.timedelta(days=30)).strftime('%Y%m%d')
        sql_script = "SELECT JYRQ as TRADEDATE, SPJG as TCLOSE from funddb.ZSJY WHERE ZQDM = '{}' " \
                     "and JYRQ >= {} and JYRQ <= {}".format(self.benchmark_id, pre_date, self.trade_date)
        data = pd.DataFrame(hbs.db_data_query('readonly', sql_script)['data'])
        data['index_return'] = data['TCLOSE'].pct_change()
        index_return = data.set_index('TRADEDATE').loc[self.trade_date, 'index_return']
        # 指数成分数据
        shift_date = self._load_shift_date(self.trade_date)
        benchmark_cp = self._load_benchmark_components(shift_date)

        market_df = pd.merge(market_df, benchmark_cp, on='ticker', how='left')
        market_df['benchmark_id'].fillna('other', inplace=True)


if __name__ == '__main__':
    AlphaMonitor('20220105')