import json
import os

input_folder = "output_json"
output_folder = "output_txt"
os.makedirs(output_folder, exist_ok=True)

for json_file in os.listdir(input_folder):
    if json_file.endswith(".json"):
        json_path = os.path.join(input_folder, json_file)
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        urls = [item["url"] for item in data]

        txt_file_name = os.path.splitext(json_file)[0] + ".txt"
        txt_path = os.path.join(output_folder, txt_file_name)

        with open(txt_path, "w", encoding="utf-8") as f_txt:
            for url in urls:
                f_txt.write(url + "\n")

        print(f"✅ สร้าง {txt_file_name} → {len(urls)} URL")
