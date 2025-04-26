from flask import Flask, request, jsonify, send_file
from app import db
import os

def create_app():
    app = Flask(__name__)  #建立flask的寫法 flask用__name__決定目前app的根目錄在哪

    app.config['SECRET_KEY'] = 'secret_key' #加密用的

    app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), '..', 'db', 'messages.db')# 設定db路徑

    with app.app_context(): #進入app_context
        db.init_db()

    @app.route('/messages', methods=['GET']) #顯示所有message
    def get_all_messages():
        messages = db.get_messages() #從db拿message
        return jsonify([ #把每一筆message存成python dict再包成list回傳
            {
                'id': message['id'],
                'content': message['content'],
                'created_at': message['created_at']
            } for message in messages
        ])
    
    @app.route('/latest_message', methods=['GET']) #顯示最近的message
    def get_latest_message():
        message = db.get_latest_message() #從db拿單筆message
        if message is None:
            return jsonify({'message': 'No message'}), 404
        return jsonify({
                'id': message['id'],
                'content': message['content'],
                'created_at': message['created_at']
        })

    @app.route('/messages', methods=['POST']) #新增message
    def create_message():
        content = request.json.get('content') #拿留言文字
        if not content: 
            return jsonify({'error': 'Content is required'}), 400 #沒有輸入內容傳錯誤訊息
        db.add_message(content) #把留言寫進SQLite
        return jsonify({'message': 'Message created successfully'}), 201 #新增成功
    
    @app.route('/')
    def index():
        return '留言板後端 API 運作中！\n 使用 /messages 存取留言資料。\n 使用 /frontend到前端互動'

    @app.route('/frontend')
    def frontend():
        return send_file('frontend.html')

    return app
