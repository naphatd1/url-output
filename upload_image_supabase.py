import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAMES")
LOCAL_ROOT = os.getenv("LOCAL_ROOT")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

LOCAL_ROOT = "images" 

def upload_folder(local_folder, bucket_folder=""):
    for item in os.listdir(local_folder):
        local_path = os.path.join(local_folder, item)
        if os.path.isdir(local_path):
            sub_bucket_folder = f"{bucket_folder}/{item}" if bucket_folder else item
            upload_folder(local_path, sub_bucket_folder)
        else:
            bucket_path = f"{bucket_folder}/{item}" if bucket_folder else item
            with open(local_path, "rb") as f:
                data = f.read()
                supabase.storage.from_(BUCKET_NAME).upload(bucket_path, data, {"upsert": 'true'})
            print(f"✅ Uploaded {local_path} → {bucket_path}")

upload_folder(LOCAL_ROOT)
print("✅ Upload เสร็จเรียบร้อยทั้งหมด")
