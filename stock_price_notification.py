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
stocks = ['00830.TW', '00662.TW', '00757.TW']

def get_stock_info(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    current_price = info['currentPrice']
    high_price = info['fiftyTwoWeekHigh']
    percentage = (current_price / high_price - 1) * 100
    return current_price, percentage

message = "\n今日股票價格通知:\n\n"

for stock in stocks:
    price, percentage = get_stock_info(stock)
    message += f"{stock}: 當前價格 {price:.2f}, 相對最高點 {percentage:.2f}%\n"

# 發送 LINE 通知
send_line_notify(message)

# 輸出日誌
tw_timezone = pytz.timezone('Asia/Taipei')
current_time = datetime.now(tw_timezone).strftime("%Y-%m-%d %H:%M:%S")
print(f"通知已發送 - {current_time}")