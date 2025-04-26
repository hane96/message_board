import sqlite3
from datetime import datetime
import os
from flask import current_app


def get_db_connection(): #建立SQLite連線object conn
    db_path = current_app.config['DATABASE'] #從init拿app.config['DATABASE']的路徑
    conn = sqlite3.connect(db_path) #連接到path上的資料庫 conn是執行SQL的物件
    conn.row_factory = sqlite3.Row  #把從SQLite拿到的tuple轉成dict的row
    return conn

# 初始化資料庫
def init_db():
    conn = get_db_connection() #生成連線物件 conn
    cursor = conn.cursor() #做一個cursor
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''') #初始化table
    conn.commit() #提交更新
    conn.close() #關閉conn會自動連cursor一起關掉

#新增留言
def add_message(content):
    conn = get_db_connection() 
    cursor = conn.cursor() 
    created_at = datetime.now().isoformat() #把現在時間的datatime物件轉成iso標準字串
    cursor.execute('''
        INSERT INTO messages (content, created_at)
        VALUES (?, ?)
    ''', (content, created_at))
    conn.commit() 
    conn.close() 

#取得所有留言
def get_messages():
    conn = get_db_connection() 
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages ORDER BY created_at DESC')
    messages = cursor.fetchall() #把query結果全部抓出來變成list
    conn.close()
    return messages

#取得單個留言
def get_latest_message():
    conn = get_db_connection() 
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages ORDER BY created_at DESC LIMIT 1')
    message = cursor.fetchone() #回傳單一筆row物件
    conn.close()
    return message
