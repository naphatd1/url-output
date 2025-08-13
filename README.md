# URL to Supabase Picture Uploader

สคริปต์ Python สำหรับดาวน์โหลดรูปภาพจาก URL และอัปโหลดไปยัง Supabase Storage

## 📌 คุณสมบัติ
- ดึงรูปภาพจาก URL (อ่านจากไฟล์ CSV, JSON หรือกำหนดเองในโค้ด)
- อัปโหลดรูปภาพไปยัง Supabase Storage
- รองรับการตั้งค่า Environment Variables ผ่าน `.env`
- บันทึกผลลัพธ์ทั้ง **CSV** และ **JSON** ในโฟลเดอร์ `output_csv` และ `output_json`

---

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


## 📦 การติดตั้ง

### 1️⃣ Clone โปรเจค
```bash
git clone https://github.com/your-repo/url-supabase-picture.git
cd url-supabase-picture

### 2️⃣ สร้าง Virtual Environment (แนะนำ)
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # macOS / Linux
venv\Scripts\activate     # Windows

### 3️⃣ ติดตั้ง Dependencies
bash
Copy
Edit
pip install -r requirements.txt

### ⚙️ การตั้งค่า Environment Variables
สร้างไฟล์ .env และใส่ค่าตามนี้

.env
Copy
Edit
SUPABASE_URL=https://xxxxxxxx.supabase.co
SUPABASE_KEY=your_service_role_key
BUCKET_NAME=images
BUCKET_NAMES=photo
LOCAL_ROOT=images
UPLOADS_FOLDERS = uploads