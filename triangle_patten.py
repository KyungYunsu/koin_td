import ccxt
import pandas as pd
import talib
import datetime
import pytz

# 시간 받아오기
current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%Y월%m년%d일 %H시%M분_")


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

    def get_triangle_pattern(self, symbol, timeframe):
        df = self.get_ohlcv_data(symbol, timeframe)
        asc_pattern = talib.CDL_ASCENDINGTRIANGLE(
            df['open'], df['high'], df['low'], df['close'])
        desc_pattern = talib.CDL_DESCENDINGTRIANGLE(
            df['open'], df['high'], df['low'], df['close'])
        df['asc_pattern'] = asc_pattern
        df['desc_pattern'] = desc_pattern
        df_data = df.iloc[::-1]
        return df_data


my_exchange = MyExchange()
btc_usdt_triangle_data_15m = my_exchange.get_triangle_pattern(
    'BTC/USDT', '15m')

# 상승삼각형 패턴 여부 출력
asc_triangle = [100 if pattern >
                0 else 0 for pattern in btc_usdt_triangle_data_15m['asc_pattern']]
print("상승삼각형 패턴 여부:", asc_triangle)

# 하락삼각형 패턴 여부 출력
desc_triangle = [-100 if pattern <
                 0 else 0 for pattern in btc_usdt_triangle_data_15m['desc_pattern']]
print("하락삼각형 패턴 여부:", desc_triangle)

# 시간과 함께 패턴 여부 출력
for idx, timestamp in enumerate(btc_usdt_triangle_data_15m.index):
    print(timestamp, "상승삼각형:", asc_triangle[idx], "하물삼각형:", desc_triangle[idx])
