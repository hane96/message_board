
# Message_board Flask API

這是為了練習 Flask 開發的簡單留言板後端。使用 Flask 和 SQLite，提供了基本的留言功能（創建、讀取留言）。並用 HTML + JS寫了簡單的前端，可以拿來測試 API。

### 功能

- **新增留言**: 透過 `POST` 新增留言。
- **查看留言**: 透過 `GET` 取得所有留言。
- **資料儲存**: 將留言儲存在 SQLite 內。

### 需要的套件

可以透過這個安裝專案所需的所有套件：

```bash
pip install -r requirements.txt
```

### 使用方式

1. 先建立虛擬環境並啟動它：

   ```bash
   python -m venv venv
   source venv/Scripts/activate 
   ```

2. 安裝所需套件：

   ```bash
   pip install -r requirements.txt
   ```

3. 執行 Flask 伺服器：

   ```bash
   python run.py
   ```

4. 伺服器啟動後，打開瀏覽器進入 `http://127.0.0.1:5000`，就可以看到留言板頁面。

( windows可以直接用寫好的windows_run.bat )

### 預設 API 端點

- **GET /messages**: 取得所有留言。
- **POST /messages**: 新增留言，必須提供 `content` 欄位。

### 其他說明

這是個簡單的練習專案，前端會載入 `frontend.html` 頁面，並透過 JavaScript 連接到 API。

你可以進一步查看我的 [note.md](./note.md)，裡面有更多細節和開發過程的學習筆記。
```