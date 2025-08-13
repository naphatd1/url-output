import json
import os

# โฟลเดอร์ input (JSON) และ output (.txt)
input_folder = "output_json"
output_folder = "output_url"
os.makedirs(output_folder, exist_ok=True)

# วนอ่านทุกไฟล์ JSON ใน input_folder
for json_file in os.listdir(input_folder):
    if json_file.endswith(".json"):
        json_path = os.path.join(input_folder, json_file)
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # ดึงเฉพาะ URL
        urls = [item["url"] for item in data]

        # สร้างชื่อไฟล์ txt จากชื่อ folder (เช่น pic1.json → pic1.txt)
        txt_file_name = os.path.splitext(json_file)[0] + ".txt"
        txt_path = os.path.join(output_folder, txt_file_name)

        # เขียนเป็น JSON array ลงไฟล์ txt
        with open(txt_path, "w", encoding="utf-8") as f_txt:
            f_txt.write("[\n")
            for i, url in enumerate(urls):
                comma = "," if i < len(urls)-1 else ""
                f_txt.write(f'"{url}"{comma}\n')
            f_txt.write("]\n")

        print(f"✅ สร้าง {txt_file_name} → {len(urls)} URL")
