# Supabase Image Uploader

โปรเจคนี้ใช้สำหรับอัปโหลดรูปจากโฟลเดอร์ `images` ขึ้นไปยัง Supabase Storage

## โครงสร้างโฟลเดอร์
```
images/
├── pic1/
│   ├── 1.jpg
│   ├── 2.jpg
│   └── ...
├── pic2/
│   ├── 1.jpg
│   ├── 2.jpg
│   └── ...
...
├── pic40/
│   ├── 1.jpg
│   ├── 2.jpg
```

## สิ่งที่ต้องติดตั้ง
```bash
pip install supabase
pip install python-dotenv
```

## การตั้งค่า Environment Variables
สร้างไฟล์ `.env` ใน root ของโปรเจค และเพิ่มข้อมูลดังนี้
```
SUPABASE_URL=https://<your-project-ref>.supabase.co
SUPABASE_KEY=<your-service-role-key>
SUPABASE_BUCKET=your-bucket-name
```

> **หมายเหตุ:** อย่าแชร์ `SUPABASE_KEY` บน GitHub หรือที่สาธารณะ

## วิธีใช้งาน
1. เตรียมไฟล์รูปในโฟลเดอร์ `images`
2. รันสคริปต์อัปโหลด:
```bash
python upload_images.py
```
