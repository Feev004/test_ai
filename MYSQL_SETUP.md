# MySQL Database Setup Guide

## ขั้นตอนการตั้งค่า

### 1. ติดตั้ง MySQL Server
ดาวน์โหลดและติดตั้ง MySQL จากที่นี่: https://dev.mysql.com/downloads/mysql/

### 2. ติดตั้ง Python Dependencies
```powershell
pip install -r requirements.txt
```

### 3. ตั้งค่า Environment Variables
```powershell
# Windows PowerShell
$env:MYSQL_HOST = "localhost"
$env:MYSQL_USER = "root"
$env:MYSQL_PASSWORD = "your-password"
$env:MYSQL_DB = "report_db"
$env:MYSQL_PORT = "3306"
$env:OPENROUTER_API_KEY = "your-api-key"
```

### 4. Initialize Database
```powershell
python .\init_db.py
```
คำสั่งนี้จะสร้าง table `reports` ในฐานข้อมูล

### 5. รัน Flask App
```powershell
python .\index.py
# หรือ ใช้ ngrok
python .\index.py --ngrok
```

---

## API Endpoints

### Get All Reports
```
GET /api/reports
```

### Get Single Report
```
GET /api/reports/<id>
```

### Create Report
```
POST /api/reports
Content-Type: application/json

{
  "title": "Report Title",
  "content": "Report content or message"
}
```

### Update Report
```
PUT /api/reports/<id>
Content-Type: application/json

{
  "title": "New Title",
  "content": "New content",
  "ai_response": "AI response"
}
```

### Delete Report
```
DELETE /api/reports/<id>
```

---

## Database Schema

```sql
CREATE TABLE reports (
  id INT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(255) NOT NULL,
  content LONGTEXT,
  ai_response LONGTEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

---

## ปัญหาที่อาจเจอ

| ปัญหา | วิธีแก้ |
|------|--------|
| `Access denied for user 'root'` | เช็ค MYSQL_PASSWORD ให้ถูกต้อง |
| `Can't connect to MySQL server` | ตรวจสอบว่า MySQL Server กำลังรัน |
| `Unknown database 'report_db'` | รัน `python .\init_db.py` ก่อน |
| `ModuleNotFoundError: No module named 'pymysql'` | รัน `pip install -r requirements.txt` |
