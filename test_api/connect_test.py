import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()  # 載入 .env 檔案

# 設定
API_URL = "https://api-gateway.netdb.csie.ncku.edu.tw/api/tags"
API_KEY = os.getenv("API_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

try:
    print(f"正在連線至 {API_URL} ...")
    response = requests.get(API_URL, headers=headers, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ 連線成功！可用模型如下：")
        # Ollama 的回傳結構通常是 {"models": [{"name": "llama3:latest", ...}]}
        if "models" in data:
            for model in data["models"]:
                print(f" - {model['name']}")
        else:
            print("回傳格式怪怪的，直接印出：", data)
    else:
        print(f"❌ 失敗 (Status: {response.status_code})")
        print(response.text)

except Exception as e:
    print(f"⚠️ 連線錯誤: {e}")