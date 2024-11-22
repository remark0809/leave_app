from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# LINE Notify Token
LINE_NOTIFY_TOKEN = "ei5dZQlZN1Bakw3GrdfR2voKFD4oXuTLrGwS9bwHM7L"

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>休暇申請</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }
            form { max-width: 300px; margin: auto; }
            input, textarea { width: 100%; margin: 10px 0; padding: 10px; }
            button { padding: 10px 20px; background: #0078D4; color: white; border: none; }
        </style>
    </head>
    <body>
        <h1>休暇申請フォーム</h1>
        <form id="leaveForm">
            <input type="text" name="名前" placeholder="名前" required>
            <input type="text" name="内容" placeholder="内容" required>
            <textarea name="備考" placeholder="備考（任意）"></textarea>
            <button type="submit">送信</button>
        </form>
        <script>
            const form = document.getElementById('leaveForm');
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                const formData = new FormData(form);
                const data = Object.fromEntries(formData);
                const response = await fetch('/submit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                if (response.ok) {
                    alert('申請が送信されました！');
                } else {
                    alert('送信に失敗しました。もう一度お試しください。');
                }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    name = data.get('名前')
    reason = data.get('内容')
    details = data.get('備考', '')

    # Format the message for LINE Notify
    message = f"休暇申請を受信しました:\n名前: {name}\n内容: {reason}\n備考: {details}"

    # Send to LINE
    line_notify(message)

    return jsonify({"status": "success"}), 200

def line_notify(message):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"}
    payload = {"message": message}
    requests.post(url, headers=headers, data=payload)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
