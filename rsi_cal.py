import ccxt
import pandas as pd
import talib

class MyExchange:
    
    def __init__(self):
        self.exchange = ccxt.binance({
            'rateLimit': 1000,
            'enableRateLimit': True,
            'futures': True
        })

    def get_ohlcv_data(self, symbol, timeframe):
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe)
        df = pd.DataFrame(
            ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    
    def get_rsi_data(self, symbol, timeframe, timeperiod=14):
        df = self.get_ohlcv_data(symbol, timeframe)
        rsi = talib.RSI(df['close'], timeperiod=timeperiod)
        df['rsi'] = rsi
        df_data = df.iloc[::-1]
        return df_data

    
my_exchange = MyExchange()
btc_usdt_rsi_data = my_exchange.get_rsi_data('BTC/USDT', '15m')
# 함수 결과값 출력
# print(btc_usdt_rsi_data)
# 행렬 변환 출력
print(btc_usdt_rsi_data.transpose())
# 엑셀 출력
my_exchange = MyExchange()
btc_usdt_rsi_data = my_exchange.get_rsi_data('BTC/USDT', '15m')
btc_usdt_rsi_data.transpose().to_excel('btc_usdt_rsi_data.xlsx')