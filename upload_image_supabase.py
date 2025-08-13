import os
from dotenv import load_dotenv
from supabase import create_client, Client

# โหลดค่าใน .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")
LOCAL_ROOT = os.getenv("LOCAL_ROOT")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ===== โฟลเดอร์ local ที่เก็บรูป =====
LOCAL_ROOT = "images"  # สมมติโฟลเดอร์ local มี pic1, pic2 ... pic40

# ===== ฟังก์ชัน upload แบบ recursive =====
def upload_folder(local_folder, bucket_folder=""):
    for item in os.listdir(local_folder):
        local_path = os.path.join(local_folder, item)
        if os.path.isdir(local_path):
            # ถ้าเป็น folder → recursion
            sub_bucket_folder = f"{bucket_folder}/{item}" if bucket_folder else item
            upload_folder(local_path, sub_bucket_folder)
        else:
            # ถ้าเป็นไฟล์ → upload
            bucket_path = f"{bucket_folder}/{item}" if bucket_folder else item
            with open(local_path, "rb") as f:
                data = f.read()
                supabase.storage.from_(BUCKET_NAME).upload(bucket_path, data, {"upsert": 'true'})
            print(f"✅ Uploaded {local_path} → {bucket_path}")

# เริ่ม upload
upload_folder(LOCAL_ROOT)
print("✅ Upload เสร็จเรียบร้อยทั้งหมด")
