# 🚀 Render Deployment Guide for My Portfolio

## 📋 Prerequisites
1. GitHub repository with your code
2. Render account (sign up at [render.com](https://render.com))
3. PostgreSQL database (already provided by Aiven)

## 🔧 Database Information
- **Service URI**: `postgres://avnadmin:AVNS_mT5_XzYo4EvApbAW4ci@pg-24910b25-samueloluwapelumi8-0a9b.k.aivencloud.com:25379/defaultdb?sslmode=require`
- **Database name**: `defaultdb`
- **Host**: `pg-24910b25-samueloluwapelumi8-0a9b.k.aivencloud.com`
- **Port**: `25379`
- **User**: `avnadmin`
- **Password**: `AVNS_mT5_XzYo4EvApbAW4ci`

## 🚀 Deployment Steps

### Step 1: Prepare Your Repository
1. Make sure all files are committed to your GitHub repository
2. Verify that `.env` file is in `.gitignore` (it should be ignored)
3. Ensure all necessary files are present:
   - `app.py` (updated with environment variables)
   - `requirements.txt`
   - `Procfile`
   - `render.yaml`
   - `.gitignore`

### Step 2: Deploy Web Service on Render
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `my-portfolio`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

### Step 3: Set Environment Variables
In your Render web service settings, add these environment variables:

```
DATABASE_URL=postgres://avnadmin:AVNS_mT5_XzYo4EvApbAW4ci@pg-24910b25-samueloluwapelumi8-0a9b.k.aivencloud.com:25379/defaultdb?sslmode=require
MAIL_USERNAME=samueloluwapelumi8@gmail.com
MAIL_PASSWORD=your-gmail-app-password
ADMIN_USERNAME=your-secure-admin-username
ADMIN_PASSWORD=your-secure-admin-password
SECRET_KEY=your-super-secret-key-here
```

### Step 4: Deploy
1. Click **"Deploy"**
2. Wait for the deployment to complete (usually 2-5 minutes)
3. Your app will be available at `https://your-app-name.onrender.com`

## 🔐 Security Setup

### Gmail App Password
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Navigate to **Security** → **2-Step Verification**
3. Scroll down to **App passwords**
4. Generate a new app password for "Mail"
5. Use this password as `MAIL_PASSWORD` in Render

### Admin Credentials
- Change `ADMIN_USERNAME` and `ADMIN_PASSWORD` to secure values
- Use a strong, unique password for admin access

### Secret Key
- Generate a secure secret key using:
  ```python
  import secrets
  print(secrets.token_hex(32))
  ```

## 🗄️ Database Setup
After deployment, your database tables will be created automatically when the app starts. If you need to manually set up the database:

1. Connect to your Render service
2. Run: `python setup_db.py`

## 📁 File Structure
```
myPortfolio/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Render deployment command
├── render.yaml           # Render configuration
├── .gitignore            # Git ignore rules
├── .env                  # Environment variables (local only)
├── setup_db.py           # Database setup script
├── templates/            # HTML templates
├── static/              # CSS, JS, images
└── RENDER_DEPLOYMENT.md  # This guide
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Database Connection Error
- Verify `DATABASE_URL` is set correctly
- Check if database is accessible from Render
- Ensure SSL mode is set to `require`

#### 2. Email Not Working
- Verify `MAIL_PASSWORD` is an app password, not your regular password
- Check Gmail 2-factor authentication is enabled
- Ensure `MAIL_USERNAME` is correct

#### 3. App Won't Start
- Check Render logs for errors
- Verify all dependencies are in `requirements.txt`
- Ensure `Procfile` is correct

#### 4. Environment Variables Not Loading
- Verify variables are set in Render dashboard
- Check variable names match exactly
- Restart the service after adding variables

### Checking Logs
1. Go to your Render service dashboard
2. Click on **"Logs"** tab
3. Look for error messages or warnings

## 🔄 Updates and Maintenance

### Updating Your App
1. Make changes to your code
2. Commit and push to GitHub
3. Render will automatically redeploy

### Environment Variable Changes
1. Update variables in Render dashboard
2. Restart the service

### Database Changes
- Modify `setup_db.py` if you need to add new tables
- Run the script after deployment

## 📞 Support
- Render Documentation: [render.com/docs](https://render.com/docs)
- Flask Documentation: [flask.palletsprojects.com](https://flask.palletsprojects.com/)
- PostgreSQL Documentation: [postgresql.org/docs](https://www.postgresql.org/docs/)

## ✅ Checklist Before Deployment
- [ ] All files committed to GitHub
- [ ] `.env` file is in `.gitignore`
- [ ] Environment variables prepared
- [ ] Gmail app password generated
- [ ] Admin credentials changed
- [ ] Secret key generated
- [ ] Database URL verified
- [ ] All dependencies in `requirements.txt`

## 🎉 After Deployment
- Test all pages of your portfolio
- Test contact form submission
- Test admin login
- Verify email notifications work
- Check database connection

Your portfolio should now be live and secure! 🚀
