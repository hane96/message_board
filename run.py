from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True) #debug=True 讓每次修改.py時會自動重啟server


