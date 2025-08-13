from supabase import create_client, Client
from dotenv import load_dotenv
import csv, json, os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_KEY") # ต้องใช้ service key
BUCKET_NAME = os.getenv("BUCKET_NAMES")
UPLOADS_FOLDER = os.getenv("UPLOADS_FOLDERS")

supabase: Client = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

os.makedirs("output_csv", exist_ok=True)
os.makedirs("output_json", exist_ok=True)

subfolders = supabase.storage.from_(BUCKET_NAME).list(UPLOADS_FOLDER)
total_files = 0

for sf in subfolders:
    if sf["metadata"] is None:
        folder_name = sf["name"]
        folder_path = f"{UPLOADS_FOLDER}/{folder_name}"
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
        # CSV
        with open(f"output_csv/{folder_name}.csv", "w", newline="", encoding="utf-8") as f_csv:
            writer = csv.DictWriter(f_csv, fieldnames=["folder","file_name","url"])
            writer.writeheader()
            writer.writerows(file_data)
        # JSON
        with open(f"output_json/{folder_name}.json", "w", encoding="utf-8") as f_json:
            json.dump(file_data, f_json, indent=4, ensure_ascii=False)
        print(f"📂 {folder_name} → {len(file_data)} ไฟล์ (CSV & JSON)")

print(f"\n✅ เสร็จแล้ว! รวมทั้งหมด {total_files} ไฟล์")
