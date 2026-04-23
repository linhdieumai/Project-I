import sqlite3
import os
from flask import Flask, request

app = Flask(__name__)

# LỖ HỔNG 1: Hardcoded Credentials (Thông tin nhạy cảm để lộ trong code)
# SonarQube thường bắt lỗi này rất gắt gao.
ADMIN_PASSWORD = "SuperSecretPassword123!"

@app.route("/login")
def login():
    # LỖ HỔNG 2: SQL Injection (Nối chuỗi trực tiếp vào query)
    # Semgrep có thể tìm lỗi này qua pattern matching cực nhanh.
    username = request.args.get('username')
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    
    # Thực thi query nguy hiểm
    cursor.execute(query)
    return "User logged in!"

@app.route("/ping")
def ping():
    # LỖ HỔNG 3: Command Injection (Thực thi lệnh hệ thống từ input người dùng)
    # Cả Semgrep và SonarQube đều sẽ cảnh báo lỗi nghiêm trọng này.
    hostname = request.args.get('hostname')
    os.system("ping -c 1 " + hostname)
    return "Pinged!"

if __name__ == "__main__":
    # LỖ HỔNG 4: Debug mode enabled (Nguy hiểm khi chạy production)
    app.run(debug=True)