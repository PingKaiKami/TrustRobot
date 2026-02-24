# TrustRobot

## 1. 建置專案
```
git clone https://github.com/PingKaiKami/TrustRobot.git
```

## 2. 測試
```
python test.py
```

## 整合部分 `test.py` 中
``` python
@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    user_input = data.get('user_string')
    
    print(f"收到使用者訊息: {user_input}")
    
    return jsonify({
        "reply": f"收到您的訊息了！關於「{user_input}」，我們會請專員回覆。"
    })
```

`user_input`是指使用者傳過來的內容，請將這個跟 RAG 結合

最後 RAG 回傳的結果請寫在???中 `return jsonify({"reply": f"???"})`
