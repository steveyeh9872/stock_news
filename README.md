# 股票資訊自動化通知系統

本專案使用 GitHub Actions 自動化抓取股票資訊並每日發送通知。

## 重要通知

**LINE Notify 服務將於 2025 年 4 月停止**。本專案已更新為使用 LINE Messaging API。如需設定 LINE Messaging API，請參考[設定教學](https://hackmd.io/@flagmaker/r1fcsp20R)。

## Stock News

### 說明

抓取股票新聞資訊並每日發送通知。

### 執行檔案

- `daily_stock_news.yml`
- `stock_news_scraper.py`

### 設定

1. 前往 GitHub 儲存庫的 Settings > Secrets
2. 新增以下 secrets：
   - `EMAIL_PASSWORD`：Gmail 應用程式密碼
   - `SENDER_EMAIL`：Gmail 地址
   - `RECEIVER_EMAIL`：接收郵件的地址
   - `LINE_CHANNEL_ACCESS_TOKEN`：LINE Messaging API 的 Channel Access Token
   - `LINE_USER_ID`：您的 LINE 用戶 ID

## Stock Price Notification

### 說明

抓取股票價格資訊並每日發送通知。

### 執行檔案

- `stock_price_notification.yml`
- `stock_price_notification.py`

### 設定

1. 前往 GitHub 儲存庫的 Settings > Secrets
2. 新增以下 secrets：
   - `LINE_CHANNEL_ACCESS_TOKEN`：LINE Messaging API 的 Channel Access Token
   - `LINE_USER_ID`：您的 LINE 用戶 ID

## Stock Price Analysis Notification

### 說明

抓取股票價格資訊，分析下降幅度與加碼量，並每日發送通知。追蹤股票包括：

- NVIDIA (NVDA)
- 台積電 (2330.TW)
- Microsoft (MSFT)
- Amazon (AMZN)
- Netflix (NFLX)
- QQQ
- VTI
- SMH

### 執行檔案

- `stock_analysis.yml`
- `stock_analysis.py`

### 設定

1. 前往 GitHub 儲存庫的 Settings > Secrets
2. 新增以下 secrets：
   - `LINE_CHANNEL_ACCESS_TOKEN`：LINE Messaging API 的 Channel Access Token
   - `LINE_USER_ID`：您的 LINE 用戶 ID

### 執行

所有功能都通過 GitHub Actions 自動執行。您可以在 Actions 頁面查看執行記錄和結果。

### 依賴套件

所有必要的 Python 套件都列在 `requirements.txt` 文件中。GitHub Actions 將自動安裝這些套件。

## LINE Messaging API 設定說明

1. 建立 LINE Developers 帳號
2. 創建 Messaging API Channel
3. 取得 Channel Access Token 和 User ID
4. 在 GitHub Secrets 中設定必要的環境變數

詳細設定步驟請參考：https://hackmd.io/@flagmaker/r1fcsp20R

## 注意事項

- LINE Notify 將於 2025/04 停止服務，請務必更新至 LINE Messaging API
- 確保已正確設置 LINE Messaging API 的相關設定
- 定期檢查 Channel Access Token 的有效性
- 免費額度：每月 500 則免費訊息
- 您可以在 GitHub Actions 頁面查看執行記錄和結果
