from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    # 這是原本首頁載入的邏輯
    return render_template('index.html')

# --- 新增這個路由來處理 Chatbot 的非同步訊息 ---
@app.route('/get_response', methods=['POST'])
def get_response():
    # 注意：fetch 發過來的是 JSON 格式，所以要用 request.json
    data = request.json
    user_input = data.get('user_string')
    
    print(f"收到使用者訊息: {user_input}")
    
    # 這裡回傳機器人的回覆給前端，格式要是 JSON
    return jsonify({
        "reply": f"收到您的訊息了！關於「{user_input}」，我們會請專員回覆。"
    })

if __name__ == '__main__':
    app.run(debug=True)