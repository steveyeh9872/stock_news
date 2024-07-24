import os
import requests
from bs4 import BeautifulSoup
import smtplib
import json
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
    url = "https://query1.finance.yahoo.com/v8/finance/chart/%5ETWII"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = json.loads(response.text)
        
        # 獲取最新的收盤價
        price = data['chart']['result'][0]['meta']['regularMarketPrice']
        
        # 獲取漲跌幅
        previous_close = data['chart']['result'][0]['meta']['chartPreviousClose']
        change_percent = (price - previous_close) / previous_close * 100

        # 設定漲跌顏色
        color = "red" if change_percent >= 0 else "green"
        
        return f"<strong>台灣加權指數</strong>: {price:.2f} (<span style='color:{color};'>{change_percent:+.2f}%</span>)"
    except Exception as e:
        print(f"無法獲取台灣加權指數信息: {e}")
        return "<strong>台灣加權指數</strong>: 無法獲取數據"

def get_us_stock_info():
    url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = json.loads(response.text)
        
        # 獲取最新的收盤價
        price = data['chart']['result'][0]['meta']['regularMarketPrice']
        
        # 獲取漲跌幅
        previous_close = data['chart']['result'][0]['meta']['chartPreviousClose']
        change_percent = (price - previous_close) / previous_close * 100

        # 設定漲跌顏色
        color = "red" if change_percent >= 0 else "green"
        
        return f"<strong>S&P 500指數</strong>: {price:.2f} (<span style='color:{color};'>{change_percent:+.2f}%</span>)"
    except Exception as e:
        print(f"無法獲取S&P 500指數信息: {e}")
        return "<strong>S&P 500指數</strong>: 無法獲取數據"

def get_tw_news():
    url = "https://tw.stock.yahoo.com/tw-market/"
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
    url = "https://finance.yahoo.com/topic/stock-market-news/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 更新選擇器以匹配提供的 HTML 結構
        news_items = soup.select('h3 > a')
        if not news_items:
            print("無法找到新聞項目。HTML結構:")
            print(soup.prettify()[:1000])  # 打印前1000個字符的HTML，用於調試
            return "無法獲取美股新聞，請檢查網站結構是否變化"
        
        news = []
        for item in news_items[:5]:  # 只獲取前5條新聞
            title = item['title']
            link = item['href']
            if link and not link.startswith('http'):
                link = "https://finance.yahoo.com" + link
            short_link = shorten_url(link)
            news.append(f"{title}\n{short_link}\n")
        
        return "\n".join(news) if news else "無法獲取美股新聞"
    
    except requests.RequestException as e:
        print(f"請求錯誤: {e}")
        return f"獲取美股新聞時發生錯誤: {str(e)}"
    except Exception as e:
        print(f"未預期的錯誤: {e}")
        return f"處理美股新聞時發生未知錯誤: {str(e)}"

def send_email(content):
    sender_email = os.environ['SENDER_EMAIL']
    receiver_email = os.environ['RECEIVER_EMAIL']
    password = os.environ['EMAIL_PASSWORD']

    message = MIMEMultipart("alternative")
    message["Subject"] = f"每日股市資訊與新聞 - {datetime.now().strftime('%Y-%m-%d')}"
    message["From"] = sender_email
    message["To"] = receiver_email

    # 轉換純文本內容為HTML
    html = f"""\
    <html>
      <body>
        {content}
      </body>
    </html>
    """

    part = MIMEText(html, "html")
    message.attach(part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

def main():
    content = "<h2>今日股市資訊與新聞:</h2>"

    try:
        tw_info = get_tw_stock_info()
        content += f"<p>{tw_info}</p>"
    except Exception as e:
        print(f"獲取台股資訊時出錯: {e}")
        content += "<p><strong>台灣加權指數</strong>: 獲取資訊失敗</p>"

    try:
        us_info = get_us_stock_info()
        content += f"<p>{us_info}</p>"
    except Exception as e:
        print(f"獲取美股資訊時出錯: {e}")
        content += "<p><strong>S&P 500指數</strong>: 獲取資訊失敗</p>"

    content += "<h3>台股熱門新聞:</h3>"
    try:
        tw_news = get_tw_news()
        content += f"<p>{tw_news.replace('\n', '<br>')}</p>"
    except Exception as e:
        print(f"獲取台股新聞時出錯: {e}")
        content += "<p>獲取台股新聞失敗</p>"

    content += "<h3>美股熱門新聞:</h3>"
    try:
        us_news = get_us_news()
        content += f"<p>{us_news.replace('\n', '<br>')}</p>"
    except Exception as e:
        print(f"獲取美股新聞時出錯: {e}")
        content += "<p>獲取美股新聞失敗</p>"

    print(content)  # 打印整個內容以便調試
    send_email(content)

if __name__ == "__main__":
    main()