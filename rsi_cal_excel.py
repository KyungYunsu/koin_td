import ccxt
import pandas as pd
import talib
import datetime
import os
import pytz


# 시간 받아오기
current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%Y월%m년%d일 %H시%M분_")

# data 디렉토리 경로
data_dir = './data'

# data 디렉토리가 존재하지 않을 경우 생성
if not os.path.exists(data_dir):
    os.makedirs(data_dir)


class MyExchange:

    def __init__(self):
        self.exchange = ccxt.binance({
            'rateLimit': 1000,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future'
            }
        })
        self.timezone = pytz.timezone('Asia/Seoul')  # 한국 시간대 설정

    def get_ohlcv_data(self, symbol, timeframe):
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe)
        df = pd.DataFrame(
            ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['timestamp'] = df['timestamp'].apply(
            lambda x: pytz.utc.localize(x).astimezone(self.timezone))  # 시간대 변환
        df['timestamp'] = df['timestamp'].dt.tz_localize(None)  # 시간대 정보 제거
        df.set_index('timestamp', inplace=True)
        return df

    def get_open_close_rsi_data(self, symbol, timeframe, timeperiod=14):
        df = self.get_ohlcv_data(symbol, timeframe)
        rsi_close = talib.RSI(df['close'], timeperiod=timeperiod)
        rsi_open = talib.RSI(df['open'], timeperiod=timeperiod)
        df['close_rsi'] = rsi_close
        df['open_rsi'] = rsi_open
        df['high_profit'] = (df['high'] - df['open']) / df['open'] * 100
        df['low_profit'] = (df['low'] - df['open']) / df['open'] * 100
        df['close_profit'] = (df['close'] - df['open']) / df['open'] * 100
        df_data = df.iloc[::-1]

        return df_data


my_exchange = MyExchange()
btc_usdt_open_close_rsi_data_1h = my_exchange.get_open_close_rsi_data(
    'BTC/USDT', '1h')

btc_usdt_open_close_rsi_data_30m = my_exchange.get_open_close_rsi_data(
    'BTC/USDT', '30m')

btc_usdt_open_close_rsi_data_15m = my_exchange.get_open_close_rsi_data(
    'BTC/USDT', '15m')

btc_usdt_open_close_rsi_data_5m = my_exchange.get_open_close_rsi_data(
    'BTC/USDT', '5m')

btc_usdt_open_close_rsi_data_3m = my_exchange.get_open_close_rsi_data(
    'BTC/USDT', '3m')
# btc_usdt_open_rsi_data = my_exchange.get_open_rsi_data('BTC/USDT', '15m')
# 함수 결과값 출력
# print(btc_usdt_rsi_data)
# 행렬 변환 출력
print(btc_usdt_open_close_rsi_data_15m)
# print(btc_usdt_open_rsi_data)
# 엑셀 출력
my_exchange = MyExchange()

# 엑셀 파일 경로 설정
file_name = str(formatted_time) + 'btc_usdt_data.xlsx'
file_path = os.path.join(data_dir + '/' + file_name)

# ExcelWriter 생성
writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

# 엑셀 파일 생성
# btc_usdt_open_close_rsi_data_15m.to_excel(file_path)
btc_usdt_open_close_rsi_data_3m.to_excel(
    writer, sheet_name='3Minutes', index=True, float_format='%.3f')
btc_usdt_open_close_rsi_data_5m.to_excel(
    writer, sheet_name='5Minutes', index=True,  float_format='%.3f')
btc_usdt_open_close_rsi_data_15m.to_excel(
    writer, sheet_name='15Minutes', index=True, float_format='%.3f')
btc_usdt_open_close_rsi_data_30m.to_excel(
    writer, sheet_name='30Minutes', index=True, float_format='%.3f')
btc_usdt_open_close_rsi_data_1h.to_excel(
    writer, sheet_name='1hour', index=True, float_format='%.3f')


writer.save()

# 생성된 파일 경로 출력
print("엑셀 파일이 생성된 경로:", file_path)
