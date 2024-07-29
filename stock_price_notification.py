import yfinance as yf
import requests
import os
from datetime import datetime
import pytz

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

# 股票代碼列表
#stocks = ['0050.TW', '00830.TW', '00662.TW', '00757.TW']
stocks = ['2330.TW', '00631L.TW', '00675L.TW', '00757.TW']

def get_stock_info(symbol):
    stock = yf.Ticker(symbol)
    
    # 獲取最新的股票數據
    hist = stock.history(period="2d")
    current_price = hist['Close'].iloc[-1]
    
    # 獲取過去52週的數據
    hist_52w = stock.history(period="52wk")
    high_price = hist_52w['High'].max()
    
    percentage = (current_price / high_price - 1) * 100
    return current_price, percentage

message = "\n今日股票價格通知:\n\n"

for stock in stocks:
    try:
        price, percentage = get_stock_info(stock)
        message += f"{stock}: 當前價格 {price:.2f}, 相對最高點 {percentage:.2f}%\n"
    except Exception as e:
        print(f"獲取股票 {stock} 數據時出錯: {e}")
        message += f"{stock}: 無法獲取數據\n"

# 發送 LINE 通知
print(message) # 打印整個內容以便調試
send_line_notify(message)