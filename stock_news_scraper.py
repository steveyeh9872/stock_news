import os

# 在 send_email 函數中
sender_email = os.environ['SENDER_EMAIL']
receiver_email = os.environ['RECEIVER_EMAIL']
password = os.environ['EMAIL_PASSWORD']

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def get_tw_stock_info():
    url = "https://tw.stock.yahoo.com/quote/^TWII"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    index = soup.find('span', {'class': 'Fz(32px)'}).text
    change = soup.find('span', {'class': 'Fz(20px)'}).text
    
    return f"台灣加權指數: {index} ({change})"

def get_us_stock_info():
    url = "https://finance.yahoo.com/quote/%5EGSPC"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    index = soup.find('fin-streamer', {'class': 'Fw(b) Fz(36px)'}).text
    change = soup.find('fin-streamer', {'class': 'Fw(500) Pstart(8px) Fz(24px)'}).text
    
    return f"S&P 500指數: {index} ({change})"

def get_tw_news():
    url = "https://tw.stock.yahoo.com/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    news_items = soup.find_all('div', {'class': 'Py(14px)'})[:5]  # 獲取前5條新聞
    
    news = []
    for item in news_items:
        title = item.find('h3').text
        link = item.find('a')['href']
        news.append(f"{title}\n{link}\n")
    
    return "\n".join(news)

def get_us_news():
    url = "https://finance.yahoo.com/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    news_items = soup.find_all('h3', {'class': 'Mb(5px)'})[:5]  # 獲取前5條新聞
    
    news = []
    for item in news_items:
        title = item.text
        link = "https://finance.yahoo.com" + item.find('a')['href']
        news.append(f"{title}\n{link}\n")
    
    return "\n".join(news)

def send_email(content):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = f"每日股市資訊與新聞 - {datetime.now().strftime('%Y-%m-%d')}"

    message.attach(MIMEText(content, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.send_message(message)

def main():
    tw_info = get_tw_stock_info()
    us_info = get_us_stock_info()
    tw_news = get_tw_news()
    us_news = get_us_news()
    
    content = f"""
    今日股市資訊與新聞:

    {tw_info}

    {us_info}

    台股熱門新聞:
    {tw_news}

    美股熱門新聞:
    {us_news}
    """
    
    print(content)
    send_email(content)

if __name__ == "__main__":
    main()