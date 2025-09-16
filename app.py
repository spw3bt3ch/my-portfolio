from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, session
from flask_mail import Mail, Message
from flask_session import Session
import psycopg2
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hashlib
import secrets
from urllib.parse import urlparse

app = Flask(__name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration from environment variables
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'contact_admin:'
Session(app)

# Database configuration from environment variables
def get_database_url():
    """Get database URL from environment variable"""
    return os.getenv('DATABASE_URL')

def parse_database_url():
    """Parse DATABASE_URL into connection parameters"""
    database_url = get_database_url()
    
    if database_url:
        # Parse the DATABASE_URL
        parsed = urlparse(database_url)
        return {
            'host': parsed.hostname,
            'port': parsed.port,
            'database': parsed.path[1:],  # Remove leading '/'
            'user': parsed.username,
            'password': parsed.password
        }
    else:
        # Fallback to individual environment variables
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 5432)),
            'database': os.getenv('DB_NAME', 'defaultdb'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', '')
        }

# Email configuration from environment variables
MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'samueloluwapelumi8@gmail.com')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'your-app-password')

# Admin credentials from environment variables
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

# Configure Flask-Mail
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD

mail = Mail(app)

def get_db_connection():
    """Create and return a database connection"""
    try:
        db_config = parse_database_url()
        conn = psycopg2.connect(**db_config)
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None

def init_database():
    """Initialize the database with the contact_submissions table"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contact_submissions (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    subject VARCHAR(200) NOT NULL,
                    message TEXT NOT NULL,
                    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            cursor.close()
            conn.close()
            print("Database table created successfully")
        except psycopg2.Error as e:
            print(f"Database initialization error: {e}")
    else:
        print("Failed to connect to database")

def send_email_notification(name, email, subject, message):
    """Send email notification for new contact submission"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = MAIL_USERNAME
        msg['To'] = MAIL_USERNAME  # Send to yourself
        msg['Subject'] = f"New Contact Form Submission: {subject}"
        
        # Email body
        body = f"""
        New contact form submission received:
        
        Name: {name}
        Email: {email}
        Subject: {subject}
        Message: {message}
        
        Submitted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(MAIL_USERNAME, MAIL_USERNAME, text)
        server.quit()
        
        print("Email notification sent successfully")
        return True
    except Exception as e:
        print(f"Email sending error: {e}")
        return False

def send_reply_email(recipient_email, recipient_name, subject, reply_message):
    """Send reply email to user"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = MAIL_USERNAME
        msg['To'] = recipient_email
        msg['Subject'] = f"Re: {subject}"
        
        # Email body
        body = f"""
        Dear {recipient_name},
        
        Thank you for contacting me through my portfolio website. I have received your message and here is my reply:
        
        {reply_message}
        
        Best regards,
        Ogunjimi Samuel Seye
        ICT Instructor & Web Developer
        
        ---
        This is an automated reply from my portfolio contact system.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(MAIL_USERNAME, recipient_email, text)
        server.quit()
        
        print(f"Reply email sent successfully to {recipient_email}")
        return True
    except Exception as e:
        print(f"Reply email sending error: {e}")
        return False

def is_admin_logged_in():
    """Check if admin is logged in"""
    return session.get('admin_logged_in', False)

def require_admin_login(f):
    """Decorator to require admin login for certain routes"""
    def decorated_function(*args, **kwargs):
        if not is_admin_logged_in():
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route("/")
def about_me():
    return render_template('aboutme.html', titlename='About Me')

@app.route("/tetris")
def tetris():
    return render_template('tetris.html', titlename='Tetris Game')

@app.route("/resume")
def resume():
    return render_template('resume.html', titlename='My Resume')

@app.route("/contact")
def contact():
    return render_template('contact.html', titlename='Contact Me')

@app.route("/submit_contact", methods=['POST'])
def submit_contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Validate form data
        if not all([name, email, subject, message]):
            flash('All fields are required!', 'error')
            return redirect(url_for('contact'))
        
        # Save to database
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO contact_submissions (name, email, subject, message)
                    VALUES (%s, %s, %s, %s)
                ''', (name, email, subject, message))
                conn.commit()
                cursor.close()
                conn.close()
                
                # Send email notification
                send_email_notification(name, email, subject, message)
                
                flash('Thank you for your message! I will get back to you soon.', 'success')
                return redirect(url_for('contact'))
            except psycopg2.Error as e:
                print(f"Database error: {e}")
                flash('Sorry, there was an error submitting your message. Please try again.', 'error')
                return redirect(url_for('contact'))
        else:
            flash('Database connection error. Please try again later.', 'error')
            return redirect(url_for('contact'))
    
    return redirect(url_for('contact'))

@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html', titlename='Admin Login')

@app.route("/admin/logout")
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin_login'))

@app.route("/admin")
@require_admin_login
def admin():
    """Admin endpoint to view submitted contact data"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, email, subject, message, submission_date
                FROM contact_submissions
                ORDER BY submission_date DESC
            ''')
            submissions = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('admin.html', titlename='Admin - Contact Submissions', submissions=submissions)
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return "Database error occurred"
    else:
        return "Database connection failed"

@app.route("/admin/reply/<int:submission_id>", methods=['GET', 'POST'])
@require_admin_login
def admin_reply(submission_id):
    """Admin reply to a specific submission"""
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed.', 'error')
        return redirect(url_for('admin'))
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, email, subject, message, submission_date
            FROM contact_submissions
            WHERE id = %s
        ''', (submission_id,))
        submission = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not submission:
            flash('Submission not found.', 'error')
            return redirect(url_for('admin'))
        
        if request.method == 'POST':
            reply_message = request.form.get('reply_message')
            
            if not reply_message:
                flash('Reply message is required.', 'error')
                return render_template('reply.html', titlename='Reply to Message', submission=submission)
            
            # Send reply email
            if send_reply_email(submission[2], submission[1], submission[3], reply_message):
                flash(f'Reply sent successfully to {submission[2]}', 'success')
                return redirect(url_for('admin'))
            else:
                flash('Failed to send reply email. Please try again.', 'error')
        
        return render_template('reply.html', titlename='Reply to Message', submission=submission)
        
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        flash('Database error occurred.', 'error')
        return redirect(url_for('admin'))

if __name__ == "__main__":
    # Initialize database on startup
    init_database()
    app.run(host='0.0.0.0', debug=True, port=5500)