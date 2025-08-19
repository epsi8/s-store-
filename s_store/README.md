# S-Store (Flipkart-like Demo)

A ready-to-use Django e‑commerce template with:
- Search, categories, product pages
- Cart, wishlist, profile
- Orders with Razorpay (test-mode)
- Reviews/ratings
- Responsive (mobile + desktop) with Bootstrap 5
- Django Admin

## Quick Start

```bash
python -m venv .venv && . .venv/Scripts/activate  # Windows (PowerShell) 
# or: source .venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
cp .env.example .env  # then put your Razorpay keys (optional)
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Go to http://127.0.0.1:8000

### Add sample data
Login to /admin and create Categories and Products (upload images).

### Payments
- Put your `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` into `.env` for live/test payments.
- Without keys, checkout falls back to a demo "Cash on Delivery" button.

### Notes
This is a clean starter, not Flipkart's exact UI, but has the same core flows.
