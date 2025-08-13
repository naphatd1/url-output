from supabase import create_client, Client
from dotenv import load_dotenv
import os
import requests

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_KEY") 
BUCKET_NAME = "photo"
ROOT_FOLDER = "uploads"

supabase: Client = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

subfolders = supabase.storage.from_(BUCKET_NAME).list(ROOT_FOLDER)

for sf in subfolders:
    if sf["metadata"] is None: 
        folder_name = sf["name"]
        folder_path = f"{ROOT_FOLDER}/{folder_name}"
        files = supabase.storage.from_(BUCKET_NAME).list(folder_path)

        local_folder = os.path.join("downloaded", folder_name)
        os.makedirs(local_folder, exist_ok=True)

        for f in files:
            file_path = f"{folder_path}/{f['name']}"
            
            signed_url = supabase.storage.from_(BUCKET_NAME).create_signed_url(file_path, 3600)["signedURL"]

            resp = requests.get(signed_url)
            if resp.status_code == 200:
                local_file_path = os.path.join(local_folder, f["name"])
                with open(local_file_path, "wb") as img_file:
                    img_file.write(resp.content)
                print(f"✅ Downloaded {local_file_path}")
            else:
                print(f"❌ Failed to download {file_path}")

print("\n🎉 เสร็จสิ้นการดาวน์โหลดรูปทั้งหมด!")
