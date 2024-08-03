import yfinance as yf
import os
from datetime import datetime, timedelta
import requests

# 定義ETF列表
etfs = ['0050.TW', '00830.TW', '00662.TW', '00757.TW']

def get_etf_data(symbol, period='5y'):
    etf = yf.Ticker(symbol)
    hist = etf.history(period=period)
    return hist['Close']

def calculate_drawdown(price):
    peak = price.cummax()
    drawdown = (price - peak) / peak
    return drawdown

def analyze_etf(symbol):
    prices = get_etf_data(symbol)
    drawdown = calculate_drawdown(prices)
    
    # 計算歷史平均回撤和最大回撤
    avg_drawdown = drawdown.mean()
    max_drawdown = drawdown.min()
    
    # 設定個性化回撤區間
    light_drawdown = avg_drawdown / 3
    medium_drawdown = avg_drawdown * 2 / 3
    heavy_drawdown = max_drawdown * 0.8  # 使用80%的最大回撤作為重度回撤閾值
    
    # 獲取當前價格和計算當前回撤
    current_price = prices.iloc[-1]
    current_drawdown = drawdown.iloc[-1]
    
    return {
        'symbol': symbol,
        'current_price': current_price,
        'current_drawdown': current_drawdown,
        'light_drawdown': light_drawdown,
        'medium_drawdown': medium_drawdown,
        'heavy_drawdown': heavy_drawdown
    }

def send_line_notify(message):
    line_notify_token = os.environ['LINE_NOTIFY_TOKEN']
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': message}
    try:
        response = requests.post(line_notify_api, headers=headers, data=data)
        if response.status_code == 200:
            print(f"Line Notify sent. Status code: {response.status_code}")
        else:
            print(f"Failed to send Line Notify. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Error sending Line Notify: {e}")

def main():
    messages = []
    for etf in etfs:
        result = analyze_etf(etf)
        
        message = f"ETF: {result['symbol']}\n"
        message += f"當前價格: {result['current_price']:.2f}\n"
        message += f"當前回撤: {result['current_drawdown']:.2%}\n"
        
        if result['current_drawdown'] <= result['heavy_drawdown']:
            message += "警告: 重度回撤! 考慮大幅加碼\n"
        elif result['current_drawdown'] <= result['medium_drawdown']:
            message += "注意: 中度回撤, 考慮中幅加碼\n"
        elif result['current_drawdown'] <= result['light_drawdown']:
            message += "提示: 輕度回撤, 考慮小幅加碼\n"
        
        messages.append(message)
    
    # 發送Line通知
    send_line_notify('\n\n'.join(messages))

if __name__ == "__main__":
    main()