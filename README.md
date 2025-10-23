# Lokwo_Denis_Portfolio
My personal Portfolio

## Local development

1. Create and activate a virtualenv.
2. Install requirements (optional packages below):

```powershell
pip install -r requirements.txt
```

3. Run migrations and create a superuser:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

4. Run the server:

```powershell
python manage.py runserver
```

## Environment variables (optional)
- EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS — configure SMTP for production
- DEFAULT_FROM_EMAIL — default sending address
- CONTACT_EMAIL — recipient address for contact form
- RECAPTCHA_SITE_KEY, RECAPTCHA_SECRET — if you enable reCAPTCHA

## Optional packages
- requests — used for verifying reCAPTCHA server-side (if enabled)
- python-dotenv — recommended for local env var management
