import os
import sys
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT

try:
    import pymysql
    
    # Connect to MySQL
    conn = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        port=int(MYSQL_PORT)
    )
    
    cursor = conn.cursor()
    
    # Show all tables
    print("📊 Tables in database:")
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    if tables:
        for table in tables:
            print(f"  - {table[0]}")
    else:
        print("  (No tables found)")
    
    # Show reports table structure
    print("\n📋 Reports table structure:")
    cursor.execute("DESCRIBE reports;")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  - {col[0]}: {col[1]}")
    
    # Show reports data
    print("\n📝 Reports data:")
    cursor.execute("SELECT * FROM reports;")
    rows = cursor.fetchall()
    if rows:
        cursor.execute("SELECT * FROM reports;")
        columns = [desc[0] for desc in cursor.description]
        print(f"  Columns: {', '.join(columns)}")
        for row in rows:
            print(f"  {row}")
    else:
        print("  (No reports yet)")
    
    # Show count
    cursor.execute("SELECT COUNT(*) FROM reports;")
    count = cursor.fetchone()[0]
    print(f"\n✅ Total reports: {count}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}", file=sys.stderr)
    sys.exit(1)
