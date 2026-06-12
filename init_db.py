"""
Initialize MySQL database with tables for reports.
Run this script once to set up the database schema.
"""

import os
import sys
from flask import Flask
from config import SQLALCHEMY_DATABASE_URI
from models import db, Report

def init_database():
    """Create all database tables."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    
    db.init_app(app)
    
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database initialized successfully!")
            print(f"📊 Tables created: {[table for table in db.metadata.tables.keys()]}")
        except Exception as e:
            print(f"❌ Error initializing database: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    init_database()
