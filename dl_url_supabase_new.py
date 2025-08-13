# dl_supabase_complete.py

import os
import csv
import json
import re
from datetime import datetime, timezone, timedelta
from supabase import create_client, Client
from dotenv import load_dotenv
from collections import deque

# ========================
# โหลดค่า .env
# ========================
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_KEY") 
BUCKET_NAME = "photo"
ROOT_FOLDER = "uploads"

supabase: Client = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

# ========================
# สร้างโฟลเดอร์ output
# ========================
os.makedirs("output_csv", exist_ok=True)
os.makedirs("output_json", exist_ok=True)

# ========================
# ประเภทไฟล์ภาพ
# ========================
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff"}

# ========================
# helper: โหลดไฟล์ JSON เดิม
# ========================
def load_existing_json(folder_name):
    path = f"output_json/{folder_name}.json"
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return []

# ========================
# helper: natural sort
# ========================
def natural_sort_key(s):
    parts = re.split(r'(\d+)', s)
    return [int(p) if p.isdigit() else p.lower() for p in parts]

# ========================
# ดึงไฟล์แบบ iterative + skip duplicates
# ========================
queue = deque([ROOT_FOLDER])
tz = timezone(timedelta(hours=7))

while queue:
    current_path = queue.popleft()
    folder_name = os.path.basename(current_path)  # ใช้ชื่อ folder สุดท้าย

    print(f"⏳ กำลังโหลด folder: {folder_name}")

    existing_files = load_existing_json(folder_name)
    existing_file_names = set(f["file_name"] for f in existing_files)

    try:
        items = supabase.storage.from_(BUCKET_NAME).list(current_path)
    except Exception as e:
        print(f"❌ Error listing {current_path}: {e}")
        continue

    new_entries = []

    for item in items:
        if item["metadata"] is None:  # folder
            queue.append(f"{current_path}/{item['name']}")
        else:  # file
            ext = os.path.splitext(item["name"])[1].lower()
            if item["name"] == ".DS_Store" or ext not in IMAGE_EXTENSIONS:
                continue
            if item["name"] in existing_file_names:
                print(f"⏩ Skip existing: {item['name']}")
                continue

            file_path = f"{current_path}/{item['name']}"
            signed_url = supabase.storage.from_(BUCKET_NAME).create_signed_url(file_path, 3600)["signedURL"]
            new_entries.append({
                "folder": folder_name,
                "file_name": item["name"],
                "url": signed_url,
                "timestamp": datetime.now(tz).isoformat()
            })

    if new_entries:
        all_entries = existing_files + new_entries
        # sort แบบ natural
        all_entries.sort(key=lambda x: natural_sort_key(x["file_name"]))

        # CSV
        csv_path = f"output_csv/{folder_name}.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as f_csv:
            writer = csv.DictWriter(f_csv, fieldnames=["folder", "file_name", "url", "timestamp"])
            writer.writeheader()
            writer.writerows(all_entries)

        # JSON
        json_path = f"output_json/{folder_name}.json"
        with open(json_path, "w", encoding="utf-8") as f_json:
            json.dump(all_entries, f_json, indent=4, ensure_ascii=False)

        print(f"📂 {folder_name} → Added {len(new_entries)} new files")
    else:
        print(f"📂 {folder_name} → No new files")

print("\n🎉 เสร็จเรียบร้อยทั้งหมด!")
