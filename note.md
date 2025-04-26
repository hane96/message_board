# Flask 專案學習筆記

## 虛擬環境 (venv)

- 開啟虛擬環境: 
  ```bash
  source venv/Scripts/activate
  ```

- 關閉虛擬環境: 
  ```bash
  deactivate
  ```

虛擬環境 (venv) 類似一種隔離層，獨立出一個套件空間。例如：
- 專案 A 需要使用 Flask 1.0，而專案 B 需要使用 Flask 2.0。如果直接在全域 Python 安裝，則會有版本衝突的問題。使用 venv 隔開後，就不會有版本衝突的問題。

### 安裝所需套件
```bash
pip install flask flask_sqlalchemy flask_cors
```

- 可以使用 `pip freeze > requirements.txt` 把所需的套件生成需求清單 (requirements.txt)，這樣別人可以一鍵安裝需要的套件。

## Flask 框架介紹

Flask 是一種 Web 應用框架，可以簡單創建網頁伺服器並處理 client 端的 request。其主要功能包括：

1. 處理 HTTP request:
   - GET (讀取資料)
   - POST (創建資料)
   - DELETE (刪除資料)
   - PUT/PATCH (更新資料)

2. 動態網頁: 配合 HTML 引擎，根據後端的資料生成動態網頁，並根據使用者的 request 輸出不同內容。

3. 資料庫互動: Flask 可以連接資料庫並進行操作。

4. 表單處理: 可以處理 HTML 表單，讓使用者傳資料到 server。

5. API: 適合做 RESTful API，可以將 app 連接前端或其他 app。

## Flask 的具體流程

1. 使用者輸入網址發送 GET request，會被送到 Flask app。
2. Flask 根據 URL 找到對應的處理函數（例如 `home()`）。
3. 處理函數會返回一個回應，可能是文字或動態的 HTML 頁面。
4. Flask 將處理後的結果傳回給使用者的瀏覽器，並可繼續與網站互動。

## 主要程式

### run.py

```python
app.run(debug=True)
```

- `debug=True` 會讓每次修改程式 (改 `.py` 檔並儲存) 時自動重啟伺服器，不需要手動重開。

### app.py

```python
def create_app():
    app = Flask(__name__)  # 建立 Flask 應用
    with app.app_context():  # 進入 app context
        db.init_db()
```

- `app = Flask(__name__)`：這是建立 Flask 的寫法，`__name__` 決定目錄位置。
- `with app.app_context()`：進入 app context，並執行 `db.init_db()`。這裡的 app context 就像是裝載 app 所有資訊的大資料包，需要在有 app context 的情況下才能使用一些特定功能。

### 路由設定

```python
@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify(messages)
```

- `@app.route('/messages', methods=['GET'])`：這裡 `/messages` 是網址路徑，`methods=['GET']` 指定只處理 GET 請求。
- `jsonify()`：會將回傳的資料自動轉換成 JSON 格式並設定 `Content-Type: application/json`。

```python
@app.route('/messages', methods=['POST'])
def post_message():
    content = request.json.get('content')
    # 處理 POST 請求，將留言內容儲存
```

- `request.json.get('content')`：取得前端傳來的 JSON 資料中的 `content` 欄位。

### 回應格式

Flask 路由回傳的格式通常是 JSON 加上 HTTP status code：
- `200`: 成功
- `201`: 資源創建成功
- `400`: 請求錯誤
- `404`: 找不到資源
- `500`: 伺服器錯誤

## 資料庫操作

### `db.py`

```python
def get_db_connection():
    db_path = current_app.config['DATABASE']  # 拿取資料庫的路徑
    conn = sqlite3.connect(db_path)  # 連接資料庫
    conn.row_factory = sqlite3.Row  # 使結果以字典格式返回
    return conn
```

- `conn = sqlite3.connect(db_path)`：建立資料庫連線。
- `conn.row_factory = sqlite3.Row`：將資料庫回傳的結果轉為字典格式。

### 初始化資料庫

```python
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()  # 提交更改
    conn.close()  # 關閉連線
```

- `CREATE TABLE IF NOT EXISTS messages`：若資料表不存在則創建一個 `messages` 表格，包含 `id`、`content` 和 `created_at` 欄位。

### 取得留言

```python
def get_messages():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages ORDER BY created_at DESC')
    messages = cursor.fetchall()  # 取得所有留言
    conn.close()
    return messages
```

- `cursor.fetchall()`：將查詢結果轉換為列表。
- `ORDER BY created_at DESC`：按留言的創建時間排序。

## 測試和前端

### 1. 在 `__init__.py` 內的設定

```python
@app.route('/frontend')
def frontend():
    return send_file('frontend.html')
```

- `send_file()` 是 Flask 提供的函式，可以傳送靜態檔案，如 HTML、圖片、PDF、CSV 等。

### 2. HTML 基本結構

HTML 是一種階層式的標記語言，基本結構大致如下：
- 開始標籤：`<div>`
- 內部內容
- 結束標籤：`</div>`

```html
<!DOCTYPE html> <!-- 定義 HTML 的版本 -->
<html> <!-- 網頁最外層 -->
    <head> <!-- 設定區 -->
        <meta charset="UTF-8"> <!-- 設定字元編碼，UTF-8 支援中文 -->
        <title>留言板</title> <!-- 網頁標題 -->
    </head>
    <body> <!-- 網頁內容區 -->
        <h1>留言板</h1> <!-- 標題，字體較大 -->
        <input type="text" id="messageInput" placeholder="輸入留言內容"> <!-- 輸入框 -->
        <button onclick="postMessage()">送出留言</button> <!-- 按鈕，點擊觸發 JavaScript 函式 -->
    </body>
</html>
```

### 3. JavaScript 部分

```javascript
// 使用 fetch 來向 API 取得留言
const res = await fetch('/messages');  // 發送 GET 請求到 /messages 路徑
```

- `fetch('/messages')` 等同於將網址的相對路徑變更為 `/messages` 並使用 GET 方法。完整範例為：

```javascript
await fetch('/messages', {
    method: 'GET'  // 明確指定方法為 GET
});
```

### 4. 非同步處理 (Async 和 Await)

- `async` 和 `await` 用來處理非同步程式碼。這裡的 `await` 是用來等待 API 回應的過程，讓網頁的其他部分不會因為等待而卡住。

流程如下：
1. 網頁正常執行。
2. 當需要發送請求時，`fetch` 會向 API 發送請求並等待回應，這時其他程式碼會繼續執行。
3. 當回應到達後，處理回應資料。

```javascript
const list = document.getElementById('messageList');
list.innerHTML = '';  // 清空留言列表

messages.forEach(msg => {  // 逐一處理留言
    const li = document.createElement('li');  // 創建一個新的 li 元素
    li.textContent = `[${msg.created_at}] ${msg.content}`;  // 設定顯示的內容
    list.appendChild(li);  // 將新創建的 li 添加到留言列表中
});
```

- `appendChild()` 用來快速將元素添加到列表中，相比 `innerHTML +=`，`appendChild()` 不會重新處理整個 HTML 結構，因此效率較高。

### 5. 發送 POST 請求 (傳送留言)

```javascript
await fetch('/messages', {
    method: 'POST',  // 使用 POST 方法
    headers: { 'Content-Type': 'application/json' },  // 設定傳送的資料格式為 JSON
    body: JSON.stringify({ content })  // 將留言內容轉為 JSON 字串
});
```

- `fetch` 用來發送資料。這裡的 `body` 是將 JavaScript 物件轉換成 JSON 格式字串。
- `POST` 方法用於提交資料給伺服器，並將留言內容送到 `/messages` 路徑。


