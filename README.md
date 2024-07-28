# 股票資訊自動化通知系統

本專案使用 GitHub Actions 自動化抓取股票資訊並每日發送通知。

## Stock News

### 說明

抓取股票新聞資訊並每日發送通知。

### 執行檔案

- `daily_stock_news.yml`
- `stock_news_scraper.py`

### 設定

1. 前往 GitHub 儲存庫的 Settings > Secrets
2. 新增一個名為 `LINE_NOTIFY_TOKEN` 的 secret，值為您的 LINE Notify 權杖
3. 新增一個名為 `EMAIL_PASSWORD` 的 secret，值為您的 Gmail 應用程式密碼
4. 新增一個名為 `SENDER_EMAIL` 的 secret，值為您的 Gmail 地址
5. 新增一個名為 `RECEIVER_EMAIL` 的 secret，值為接收郵件的地址

### 執行

通過 GitHub Actions 自動執行

## Stock Price Notification

### 說明

抓取股票價格資訊並每日發送通知。

### 執行檔案

- `stock_price_notification.yml`
- `stock_price_notification.py`

### 設定

1. 前往 GitHub 儲存庫的 Settings > Secrets
2. 新增一個名為 `LINE_NOTIFY_TOKEN` 的 secret，值為您的 LINE Notify 權杖

### 執行

通過 GitHub Actions 自動執行

### 依賴套件

所有必要的 Python 套件都列在 `requirements.txt` 文件中。GitHub Actions 將自動安裝這些套件。

## 注意事項

- 確保您已正確設置 LINE Notify 並獲取了權杖。
- GitHub Actions 將根據設定的排程自動運行腳本。
- 您可以在 GitHub Actions 頁面查看執行記錄和結果。
