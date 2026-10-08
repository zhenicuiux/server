# راهنمای اجرای سرور کانتینری ۱۶ گیگابایتی در `Hugging Face Spaces`

یکی از قدرتمندترین و تا حدی ناشناخته‌ترین روش‌ها برای اجرای وب‌سایت، داشبورد و ربات‌های پس‌زمینه با مشخصات سخت‌افزاری بسیار بالا (۱۶ گیگابایت رم و ۲ هسته پردازنده) بدون پرداخت هیچ‌گونه هزینه، استفاده از قابلیت `Docker Spaces` در وب‌سایت `Hugging Face` است.

---

## ۱. مزایای این بستر

- **سخت‌افزار بسیار قدرتمند:** ۲ هسته پردازنده اختصاصی و ۱۶ گیگابایت رم (برای مقایسه: اکثر هاست‌های پولی اشتراکی کمتر از ۲ گیگابایت رم ارائه می‌دهند).
- **اتصال ۲۴/۷ پایدار:** در صورتی که پورت پیش‌فرض کانتینر (`7860`) باز باشد و پاسخ وب دهد، سرور فعال می‌ماند.
- **دامنه و گواهی SSL رایگان:** یک نشانی `https://username-spacename.hf.space` با گواهی معتبر دریافت می‌کنید.
- **عدم نیاز به کارت اعتباری:** ثبت‌نام صرفاً با یک ایمیل انجام می‌شود.

---

## ۲. ساخت `Space` داکر

۱. وارد حساب کاربری خود در [HuggingFace.co](https://huggingface.co/) شوید.
۲. روی گزینه **New Space** کلیک کنید.
۳. در بخش **Space SDK**، گزینه **Docker** (Blank) را انتخاب کنید.
۴. وضعیت دسترسی را **Public** قرار دهید.
۵. دکمه **Create Space** را بزنید.

---

## ۳. فایل‌های نمونه برای اجرای وب‌سایت و ربات به صورت هم‌زمان

درون ریپازیتوری اس پیس، دو فایل زیر را بسازید:

### فایل `Dockerfile`
```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# هاگینگ‌فیس ترافیک وب را روی پورت 7860 دریافت می‌کند
EXPOSE 7860

CMD ["python", "app.py"]
```

### فایل `requirements.txt`
```text
fastapi
uvicorn
python-telegram-bot
requests
```

### فایل `app.py` (اجرای هم‌زمان داشبورد وب و ربات تلگرام)
```python
import asyncio
import threading
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head><title>Cloud Dashboard</title></head>
        <body style="font-family: sans-serif; text-align: center; padding-top: 50px; background: #0d1117; color: #fff;">
            <h1>🚀 سرور و داشبورد فعال است</h1>
            <p>سیستم پردازش ابری، وب‌سایت و ربات ۲۴ ساعته در حال اجرا هستند.</p>
        </body>
    </html>
    """

def run_telegram_bot():
    # کدهای مربوط به پولینگ یا لاجیک ربات تلگرام در یک ترد مجزا
    print("Telegram bot background thread started...")

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    bot_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=7860)
```

---

## ۴. جلوگیری از به خواب رفتن (`Prevent Sleeping`)

اگرچه فضاهای داکر در اغلب موارد بدون وقفه فعال هستند، اما برای اطمینان ۱۰۰ درصدی از این که در روزهای بدون بازدید هم هرگز خاموش نشوند:
- وارد سایت رایگان [UptimeRobot.com](https://uptimerobot.com/) شوید.
- یک مانیتور رایگان از نوع `HTTP(s)` با آدرس فضای خود (`https://username-spacename.hf.space`) بسازید.
- بازه زمانی پینگ را روی ۵ دقیقه تنظیم کنید.
- این کار تضمین می‌کند که هرگز کانتینر شما متوقف نخواهد شد.
