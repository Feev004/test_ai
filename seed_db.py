import os
import sys
from flask import Flask
from config import SQLALCHEMY_DATABASE_URI
from models import db, Report
from datetime import datetime

def seed_sample_data():
    """Add sample reports to database."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    
    db.init_app(app)
    
    with app.app_context():
        try:
            # Check if data already exists
            existing_count = Report.query.count()
            if existing_count > 0:
                print(f"⚠️  Database already has {existing_count} reports. Skipping...")
                return
            
            # Sample data
            sample_reports = [
                Report(
                    title="Sales Report Q1 2024",
                    content="Quarterly sales analysis showing 15% growth",
                    ai_response="Sales performance exceeded targets with strong market demand in Asia-Pacific region."
                ),
                Report(
                    title="Project Status Update",
                    content="Current status of modernization project",
                    ai_response="Project is on track with 65% completion. Team velocity is stable and sprint goals are being met."
                ),
                Report(
                    title="Customer Feedback Summary",
                    content="Aggregated feedback from customer surveys",
                    ai_response="Overall satisfaction score is 4.2/5. Key improvement areas are response time and documentation."
                ),
                Report(
                    title="Technical Performance Metrics",
                    content="API response time and database query analysis",
                    ai_response="Performance metrics show 98% uptime. Average response time is 245ms, which is within acceptable range."
                ),
                Report(
                    title="Team Productivity Analysis",
                    content="Code commits, pull requests, and deployment frequency",
                    ai_response="Team productivity increased by 12% this month. Deployment frequency improved from 2x to 3x per week."
                ),
            ]
            
            # Add to database
            for report in sample_reports:
                db.session.add(report)
            
            db.session.commit()
            
            print(f"✅ Successfully added {len(sample_reports)} sample reports!")
            print("\n📊 Sample Reports:")
            for i, report in enumerate(sample_reports, 1):
                print(f"\n{i}. {report.title}")
                print(f"   Content: {report.content[:50]}...")
                print(f"   AI Response: {report.ai_response[:50]}...")
            
        except Exception as e:
            print(f"❌ Error adding sample data: {e}", file=sys.stderr)
            db.session.rollback()
            sys.exit(1)

if __name__ == "__main__":
    seed_sample_data()
