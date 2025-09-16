# Contact System Setup Instructions

## Overview
I've successfully created a complete contact system for your portfolio with the following features:

### ✅ Completed Features:
1. **Contact Page** (`/contact`) - Beautiful, responsive contact page with your info and contact form
2. **Admin Dashboard** (`/admin`) - View all submitted contact messages
3. **Database Integration** - PostgreSQL database to store contact submissions
4. **Email Notifications** - Receive email alerts for new submissions
5. **Form Validation** - Client and server-side validation
6. **Responsive Design** - Works perfectly on all devices

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Email Configuration
To enable email notifications, you need to:

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
3. **Update the email password** in `app.py`:
   - Replace `'your-app-password'` with your generated app password

### 3. Database Setup
The database connection is already configured with your provided credentials. The system will automatically create the `contact_submissions` table when you first run the app.

### 4. Secret Key
For production, change the secret key in `app.py`:
```python
app.secret_key = 'your-secure-secret-key-here'
```

## Usage

### Contact Page
- Visit `/contact` to see the contact page
- Users can fill out the form with their details
- Form submissions are saved to the database
- You'll receive email notifications for new submissions

### Admin Dashboard
- Visit `/admin/login` to access the admin login page
- **Default credentials**: username: `admin`, password: `admin123`
- **Important**: Change these credentials in `app.py` for security
- After login, view all contact submissions with details and timestamps
- Click "Reply" to open your email client with pre-filled recipient and subject
- Click "Logout" to end your admin session

## Contact Information Displayed
The contact page displays your information extracted from your resume:
- **Name**: Ogunjimi Samuel Seye
- **Email**: samueloluwapelumi8@gmail.com
- **Phone**: +234-707-770-5842
- **Portfolio**: my-portfolio-8047.onrender.com
- **Location**: Lagos, Nigeria
- **Social Media**: Facebook, Instagram, Twitter, YouTube

## Database Schema
The `contact_submissions` table includes:
- `id` - Primary key
- `name` - Submitter's name
- `email` - Submitter's email
- `subject` - Message subject
- `message` - Message content
- `submission_date` - Timestamp of submission

## Security Notes
- Form validation prevents empty submissions
- Email addresses are validated
- Database queries use parameterized statements to prevent SQL injection
- Flash messages provide user feedback
- Admin routes are protected with session-based authentication
- **Change default admin credentials** before deploying to production
- Sessions are configured with secure settings

## Testing
1. Start your Flask app: `python app.py`
2. Visit `http://localhost:5500/contact` to test the contact form
3. Fill out and submit the contact form
4. Visit `http://localhost:5500/admin/login` to access admin panel
5. Login with username: `admin`, password: `admin123`
6. View the submission in the admin dashboard
7. Check your email for the notification
8. Test the logout functionality

The contact system is now fully functional and ready to use!
