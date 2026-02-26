# TrustRobot

## 0. 介紹

本專案是為`2026永豐金控商業競賽`所建置的，目的是讓人們更加了解何謂信託

## 1. 建置專案
```
git clone https://github.com/PingKaiKami/TrustRobot.git
```

## 2. 下載插件 (建議於虛擬環境下執行)
```
pip install -r requirements.txt
```

## 3. 使用
```
python app.py
```


## 注意

到時候將`mode`刪除時 這邊的`mode`請幫我一並刪除
```
fetch('/get_response', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
        mode: "products", // need fix
        question: message
    })
})
```