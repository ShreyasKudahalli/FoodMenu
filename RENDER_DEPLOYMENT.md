# Render Deployment Guide

## Step 1: Generate a Secure SECRET_KEY

Run this locally:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Step 2: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/RestaurantMenu.git
git push -u origin main
```

## Step 3: Deploy on Render

1. Go to [render.com](https://render.com)
2. Sign up / Log in
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository
5. Configure:
   - **Name:** restaurantmenu
   - **Environment:** Python 3
   - **Build Command:** `bash build.sh`
   - **Start Command:** `gunicorn RestaurantMenu.wsgi:application`
   - **Plan:** Free

## Step 4: Add Environment Variables

In Render Dashboard → Environment:

| Key | Value |
|-----|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | *(paste generated key from Step 1)* |
| `RENDER_EXTERNAL_HOSTNAME` | *Auto-filled by Render* |

## Step 5: Deploy

Click **Deploy** and wait for the build to complete.

## ⚠️ Important Notes

### Database Persistence
Render's free plan SQLite is **temporary**. For production:
- Use PostgreSQL (Render offers free tier)
- Update DATABASE_URL in settings

### Media Files
Uploaded images need cloud storage (AWS S3 recommended):
- Install `django-storages` and `boto3`
- Configure S3 bucket
- Update `settings.py` with S3 settings

### HTTPS & Security
Render automatically provides HTTPS. Security headers already configured in `settings.py`.

## Testing Locally Before Deploy
```bash
python manage.py collectstatic --noinput
DEBUG=False python manage.py runserver
```

## Troubleshooting

**Build fails:** Check `render.log` in Render dashboard
**Images not displaying:** Enable S3 storage (see Media Files section)
**500 errors:** Run `python manage.py migrate` on Render shell
