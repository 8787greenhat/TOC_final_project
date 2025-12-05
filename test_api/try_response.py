import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()  # 載入 .env 檔案

# ================= 設定區 =================
API_CHAT_URL = "https://api-gateway.netdb.csie.ncku.edu.tw/api/chat"
API_KEY = os.getenv("API_KEY")
MODEL_NAME = "gpt-oss:120b" 
# =========================================

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Ollama 原生格式 payload
payload = {
    "model": MODEL_NAME,
    "messages": [
        {
            "role": "user", 
            "content": "今天 WNBA 的比賽哪一場比賽比分最接近"
        }
    ],
    "stream": True # 先設為 False 方便除錯，確定能跑再開 True
}

print(f"🚀 發送請求給模型 [{MODEL_NAME}]...")

try:
    # Timeout 設定：連線 10 秒，讀取等待 300 秒 (避免複雜 Prompt 被斷線)
    with requests.post(API_CHAT_URL, headers=headers, json=payload, stream=True, timeout=(10, 300)) as response:
        response.raise_for_status() # 檢查是否有 4xx/5xx 錯誤
        
        print("🤖 AI 回應：\n")
        full_content = "" # 用來收集完整回應
        
        # 關鍵修正：使用 iter_lines() 處理 NDJSON
        for line in response.iter_lines():
            if line: # 過濾掉空行
                try:
                    # 每一行都是一個獨立的 JSON 物件
                    json_obj = json.loads(line.decode('utf-8'))
                    
                    # 抓取內容 (Ollama 格式)
                    if 'message' in json_obj and 'content' in json_obj['message']:
                        content_chunk = json_obj['message']['content']
                        print(content_chunk, end='', flush=True) # 即時印出
                        full_content += content_chunk
                    
                    # 檢查是否結束
                    if json_obj.get('done', False):
                        print("\n\n(傳輸結束)")
                        
                except json.JSONDecodeError:
                    print(f"\n[解析錯誤] 無法解析這行: {line}")

except Exception as e:
    print(f"\n❌ 發生錯誤: {e}")