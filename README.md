# TrustRobot - 智慧大豐：信託智能助理平台

本專案是為`2026永豐金控商業競賽`所建置的，當中的「智慧大豐」是一個結合 RAG (檢索增強生成) 技術與 生成式 AI (LLM) 的現代化信託知識平台。
目的是在透過直覺的網頁交互介面，為使用者提供精準、即時且具備法規基礎的信託諮詢服務。

## 🌟 核心功能
- 多維度知識庫：整合「信託 QA」與「深度的信託專題文章」，支援動態內容載入。
- RAG 智能對話：後端串接 OpenAI API，根據使用者所處的分頁自動切換檢索模式（文章模式/產品模式）。
- 優化交互體驗：
    - 類似 LINE 的對話介面，包含機器人角色「智慧大豐」。
    - 即時「思考中」動畫，降低使用者等待焦慮。
    - 不重整網頁的非同步通訊 (AJAX/Fetch API)。

## 🛠️ 使用技術
- 前端	HTML5, CSS3 (Custom Variables), JavaScript (Fetch API, Async/Await)
- 後端	Python, Flask
- AI 模型	OpenAI GPT-4o-mini (可自行切換)
- 檢索技術	RAG (Retrieval-Augmented Generation), Vector Embedding
- 資料處理	Jinja2 模板引擎, JSON 通訊協定

## 🚀 快速開始

### 1. 複製專案
確保您的電腦已安裝 Python 3.8+。

```bash
git clone https://github.com/your-username/TrustRobot.git
cd TrustRobot
```
### 2. 安裝環境
```bash
# 建立並啟動虛擬環境
python -m venv venv
source venv/bin/activate  # Windows 使用 venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt
```

### 3. 設定環境變數
在根目錄建立 .env 檔案，並填入您的 API Key：

```
OPENAI_API_KEY=your_api_key_here
```

### 4. 資料入庫與啟動伺服器

```bash
python ingest.py # 初始化向量資料庫
```

### 5. 啟動伺服器

```bash
python app.py # 啟動 Flask 伺服器
```

啟動後訪問 http://127.0.0.1:5000 即可進入平台。

## 📂 專案目錄結構
```text
TRUSTROBOT/
├── data/               # 知識庫原始文件 (法規、產品文本)
├── db/                 # 向量資料庫儲存路徑 (如 ChromaDB, FAISS)
├── static/             # 靜態資源目錄
│   └── articles/       # 存放專題文章 HTML 片段 (如 article1.html)
├── templates/          # HTML 模板目錄
│   └── index.html      # 前端 UI 主頁面
├── venv/               # Python 虛擬環境
├── .env                # 環境變數 (API Key 等敏感資訊)
├── .gitignore          # 忽略清單 (venv, .env, __pycache__)
├── app.py              # 後端 Flask 主程式 (API 路由與 RAG 控制)
├── ingest.py           # 知識庫預處理腳本 (向量化入庫)
├── README.md           # 專案說明文件 (本檔案)
├── req.json            # 測試請求範例
└── requirements.txt    # 專案依賴套件清單
```

## ⚠️ 免責聲明
本專案提供之資訊僅供參考，不構成法律或稅務建議。
信託業務之執行與法律判斷受個案影響，具體規劃請務必諮詢 **永豐銀行信託處** 專業顧問或相關法律人士。