import os
import re
from dotenv import load_dotenv
from supabase import create_client, Client

# โหลดค่าใน .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")
LOCAL_ROOT = os.getenv("LOCAL_ROOT")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def sanitize_filename(filename):
    return re.sub(r'[^a-zA-Z0-9._-]', '_', filename)

def upload_folder(local_folder, bucket_folder=""):
    for item in os.listdir(local_folder):
        local_path = os.path.join(local_folder, item)
        if os.path.isdir(local_path):
            sub_bucket_folder = f"{bucket_folder}/{sanitize_filename(item)}" if bucket_folder else sanitize_filename(item)
            upload_folder(local_path, sub_bucket_folder)
        else:
            safe_file_name = sanitize_filename(item)
            bucket_path = f"{bucket_folder}/{safe_file_name}" if bucket_folder else safe_file_name
            with open(local_path, "rb") as f:
                data = f.read()
                supabase.storage.from_(BUCKET_NAME).upload(bucket_path, data, {"upsert": "true"})
            print(f"✅ Uploaded {local_path} → {bucket_path}")

upload_folder(LOCAL_ROOT)
print("✅ Upload เสร็จเรียบร้อยทั้งหมด")
