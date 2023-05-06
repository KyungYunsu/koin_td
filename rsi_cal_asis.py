import ccxt
import pandas as pd
import talib

# binance 거래소에서 'BTC/USDT' 선물 거래 정보를 가져옴
exchange = ccxt.binance({
    'rateLimit': 1000,  # 요청 제한 설정
    'enableRateLimit': True,  # 요청 제한 활성화
    'futures': True  # 선물 거래 정보 가져오기
})
ohlcv = exchange.fetch_ohlcv('BTC/USDT', timeframe='15m')  # 일봉 데이터 가져오기

# pandas DataFrame으로 변환
df = pd.DataFrame(
    ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)

# RSI 계산
rsi = talib.RSI(df['close'], timeperiod=14)
df['rsi'] = rsi
df_reverse = df.iloc[::-1]
# print(len(ohlcv))
# print(df_reverse['rsi'].head(10))
print(df_reverse)