from supabase import create_client, Client
from dotenv import load_dotenv
import os
import csv
import json

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_KEY") 
BUCKET_NAME = "photo"
ROOT_FOLDER = "uploads"

supabase: Client = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

os.makedirs("output_csv", exist_ok=True)
os.makedirs("output_json", exist_ok=True)

subfolders = supabase.storage.from_(BUCKET_NAME).list(ROOT_FOLDER)

total_files = 0

for sf in subfolders:
    if sf["metadata"] is None:  
        folder_name = sf["name"]
        folder_path = f"{ROOT_FOLDER}/{folder_name}"
        files = supabase.storage.from_(BUCKET_NAME).list(folder_path)

        file_data = []
        for f in files:
            file_path = f"{folder_path}/{f['name']}"
            signed_url = supabase.storage.from_(BUCKET_NAME).create_signed_url(file_path, 3600)["signedURL"]
            file_data.append({
                "folder": folder_name,
                "file_name": f["name"],
                "url": signed_url
            })

        total_files += len(file_data)
        
        csv_path = f"output_csv/{folder_name}.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as f_csv:
            writer = csv.DictWriter(f_csv, fieldnames=["folder", "file_name", "url"])
            writer.writeheader()
            writer.writerows(file_data)

        json_path = f"output_json/{folder_name}.json"
        with open(json_path, "w", encoding="utf-8") as f_json:
            json.dump(file_data, f_json, indent=4, ensure_ascii=False)

        print(f"📂 {folder_name} → {len(file_data)} URLs saved ({csv_path}, {json_path})")

print(f"\n✅ เสร็จแล้ว! รวมทั้งหมด {total_files} URLs")
