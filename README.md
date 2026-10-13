# Shielda Captcha for Python (پکیج رسمی پایتون برای شیلدا)

[![PyPI version](https://img.shields.io/pypi/v/shielda-captcha.svg)](https://pypi.org/project/shielda-captcha/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

پکیج رسمی پایتون برای سرویس امنیتی **شیلدا (Shielda)**. سازگار با تمامی فریم‌ورک‌های وب پایتون از جمله **Django**، **FastAPI** و **Flask**.

---

## 📦 نصب با pip

```bash
pip install shielda-captcha
```

---

## 🚀 نحوه استفاده

### ۱. استفاده عمومی (FastAPI / Flask / کدهای پایتون)

```python
from shielda import Shielda

# مقداردهی اولیه با کلیدهای دریافت شده از شیلدا
shielda = Shielda(
    site_key="YOUR_SITE_KEY",
    secret_key="YOUR_SECRET_KEY"
)

# اعتبارسنجی توکن ارسال شده از فرم کلاینت
token = request.form.get("darban-captcha-response")

# روش ۱: خروجی بولین (ساده)
if shielda.verify(token):
    print("کپچا با موفقیت تایید شد!")
else:
    print("خطا در تایید کپچا یا کاربر ربات است.")

# روش ۲: جزییات کامل پاسخ سرور
result = shielda.verify_with_details(token)
if result.success:
    print(f"تایید شد در تاریخ: {result.challenge_ts} برای هاست: {result.hostname}")
else:
    print(f"کدهای خطا: {result.error_codes}")
```

### ۲. نمونه در FastAPI

```python
from fastapi import FastAPI, Form, HTTPException
from shielda import Shielda

app = FastAPI()
shielda = Shielda("YOUR_SITE_KEY", "YOUR_SECRET_KEY")

@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    captcha_token: str = Form(..., alias="darban-captcha-response")
):
    if not shielda.verify(captcha_token):
        raise HTTPException(status_code=400, detail="کد کپچا نامعتبر است.")
    
    return {"message": "ورود موفقیت‌آمیز"}
```

---

## 📄 لایسنس
[MIT License](LICENSE) - [https://shielda.ir](https://shielda.ir)
