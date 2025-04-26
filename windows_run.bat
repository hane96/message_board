@echo off
:: 啟動虛擬環境
call venv\Scripts\activate

:: 安裝套件
pip install -r requirements.txt

:: 執行Flask
flask run

:: 自動關閉
deactivate
