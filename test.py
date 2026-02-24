from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    user_input = data.get('user_string')
    
    print(f"收到使用者訊息: {user_input}")
    
    return jsonify({
        "reply": f"收到您的訊息了！關於「{user_input}」，我們會請專員回覆。"
    })

if __name__ == '__main__':
    app.run(debug=True)