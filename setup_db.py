#!/usr/bin/env python3
"""
Database setup script for Render deployment
Run this script to initialize your database tables
"""

import os
import sys
from urllib.parse import urlparse
import psycopg2

def get_database_url():
    """Get database URL from environment variable"""
    return os.getenv('DATABASE_URL')

def parse_database_url():
    """Parse DATABASE_URL into connection parameters"""
    database_url = get_database_url()
    
    if database_url:
        parsed = urlparse(database_url)
        return {
            'host': parsed.hostname,
            'port': parsed.port,
            'database': parsed.path[1:],
            'user': parsed.username,
            'password': parsed.password
        }
    else:
        print("Error: DATABASE_URL environment variable not set")
        sys.exit(1)

def create_tables():
    """Create database tables"""
    db_config = parse_database_url()
    
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Create contact_submissions table
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
        
        print("✅ Database tables created successfully!")
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_tables()
