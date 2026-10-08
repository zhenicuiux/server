"""
کد شروع سریع (Starter Template)
ترکیب وب‌سایت + داشبورد وضعیت سرور + ربات تلگرام در یک فایل هماهنگ
قابل اجرا در Serv00، Hugging Face Spaces و سایر سرورهای لینوکسی
"""

import sys
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

SERVER_START_TIME = time.time()

HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>داشبورد سرور ابری | Cloud Server Dashboard</title>
    <style>
        body {
            font-family: system-ui, -apple-system, sans-serif;
            background-color: #0d1117;
            color: #c9d1d9;
            margin: 0;
            padding: 40px 20px;
            display: flex;
            justify-content: center;
        }
        .container {
            max-width: 800px;
            width: 100%;
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        h1 { color: #58a6ff; margin-top: 0; }
        .badge {
            display: inline-block;
            background: #238636;
            color: #ffffff;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
        }
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 25px;
        }
        .card {
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
        }
        .card .title { font-size: 13px; color: #8b949e; }
        .card .value { font-size: 20px; font-weight: bold; color: #f0f6fc; margin-top: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <span class="badge">● آنلاین و فعال</span>
        <h1>سرور ابری و داشبورد خدمات</h1>
        <p>این صفحه و خدمات مرتبط (وب‌سایت، ربات تلگرام و اسکریپت‌های تحلیلی) به شکل ۲۴ ساعته در سرور خارج از کشور در حال اجرا هستند.</p>

        <div class="card-grid">
            <div class="card">
                <div class="title">وضعیت وب‌سرور</div>
                <div class="value">۲۰۰ OK</div>
            </div>
            <div class="card">
                <div class="title">محیط اجرا</div>
                <div class="value">Python 3</div>
            </div>
            <div class="card">
                <div class="title">ربات تلگرام</div>
                <div class="value">فعال در پس‌زمینه</div>
            </div>
        </div>
    </div>
</body>
</html>
"""

class SimpleServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/dashboard":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_DASHBOARD.encode("utf-8"))
        elif self.path == "/health" or self.path == "/ping":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            uptime = int(time.time() - SERVER_START_TIME)
            response = json.dumps({"status": "healthy", "uptime_seconds": uptime})
            self.wfile.write(response.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # جلوگیری از لاگ‌های اضافی
        return

def telegram_bot_worker():
    """
    ترد اختصاصی برای اجرای ربات تلگرام
    می‌توانید کدهای کتابخانه python-telegram-bot یا telebot را در این بخش قرار دهید
    """
    print("[Telegram Bot] پس‌زمینه فعال شد. آماده پردازش پیام‌ها...")
    while True:
        # شبیه‌سازی فعالیت ربات یا حلقه پردازش
        time.sleep(60)

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1 and sys.argv[1] == "--port":
        port = int(sys.argv[2])

    # اجرای ربات در ترد پس‌زمینه
    bot_thread = threading.Thread(target=telegram_bot_worker, daemon=True)
    bot_thread.start()

    # اجرای وب‌سرور روی پورت مشخص
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, SimpleServerHandler)
    print(f"[Web Dashboard] سرور روی پورت {port} آغاز به کار کرد.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nسرور متوقف شد.")
