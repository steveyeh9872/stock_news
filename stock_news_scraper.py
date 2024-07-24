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

def shorten_url(url):
    try:
        response = requests.get(f"http://tinyurl.com/api-create.php?url={url}")
        return response.text
    except:
        return url  # 如果縮短失敗，返回原始URL

def get_tw_stock_info():
    url = "https://tw.stock.yahoo.com/quote/^TWII"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        index = soup.find('span', {'class': 'Fz(32px)'}).text
        change = soup.find('span', {'class': 'Fz(20px)'}).text
        return f"台灣加權指數: {index} ({change})"
    except AttributeError:
        print("無法找到台灣加權指數信息。網頁結構可能已改變。")
        return "台灣加權指數: 無法獲取數據"

def get_us_stock_info():
    url = "https://finance.yahoo.com/quote/%5EGSPC"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        index = soup.find('fin-streamer', {'data-symbol': '^GSPC'}).text
        change = soup.find('fin-streamer', {'data-field': 'regularMarketChangePercent'}).text
        return f"S&P 500指數: {index} ({change})"
    except AttributeError:
        print("無法找到S&P 500指數信息。網頁結構可能已改變。")
        return "S&P 500指數: 無法獲取數據"

def get_tw_news():
    url = "https://tw.stock.yahoo.com/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    news_items = soup.find_all('div', {'class': 'Py(14px)'})[:5]  # 獲取前5條新聞
    
    news = []
    for item in news_items:
        title = item.find('h3').text.strip()
        link = item.find('a')['href']
        short_link = shorten_url(link)
        news.append(f"{title}\n{short_link}\n")
    
    return "\n".join(news) if news else "無法獲取台股新聞"

def get_us_news():
    url = "https://finance.yahoo.com/news"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    news_items = soup.find_all('h3', {'class': 'Mb(5px)'})[:5]  # 獲取前5條新聞
    
    news = []
    for item in news_items:
        title = item.text.strip()
        link = item.find('a')['href']
        if not link.startswith('http'):
            link = "https://finance.yahoo.com" + link
        short_link = shorten_url(link)
        news.append(f"{title}\n{short_link}\n")
    
    return "\n".join(news) if news else "無法獲取美股新聞"

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
    content = "今日股市資訊與新聞:\n\n"

    try:
        content += get_tw_stock_info() + "\n\n"
    except Exception as e:
        content += f"獲取台股資訊時出錯: {str(e)}\n\n"

    try:
        content += get_us_stock_info() + "\n\n"
    except Exception as e:
        content += f"獲取美股資訊時出錯: {str(e)}\n\n"

    content += "台股熱門新聞:\n"
    try:
        content += get_tw_news() + "\n\n"
    except Exception as e:
        content += f"獲取台股新聞時出錯: {str(e)}\n\n"

    content += "美股熱門新聞:\n"
    try:
        content += get_us_news() + "\n\n"
    except Exception as e:
        content += f"獲取美股新聞時出錯: {str(e)}\n\n"

    print(content)
    send_email(content)

if __name__ == "__main__":
    main()