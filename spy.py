import requests
import os
import time
from datetime import datetime

# 🌟 雲端特殊魔法：從 GitHub 的保險箱裡偷偷抓出你的金鑰
MY_SECRET_KEY = os.environ.get("BARK_KEY")

API_URL = "https://www.futures-ai.com/api/stock-price-change-distribution"

def get_all_percentages():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    try:
        response = requests.get(API_URL, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            decrease = data.get("decreaseRate") or data.get("decrease_rate")
            flat = data.get("flatRate") or data.get("flat_rate")
            increase = data.get("increaseRate") or data.get("increase_rate")
            
            if decrease is None and "data" in data:
                sub_data = data["data"]
                decrease = sub_data.get("decrease") or sub_data.get("down")
                flat = sub_data.get("flat") or sub_data.get("stay")
                increase = sub_data.get("increase") or sub_data.get("up")
            
            if decrease is None:
                values = [str(v) for v in data.values() if isinstance(v, (int, float))]
                if len(values) >= 3:
                    return f"{values[0]}%", f"{values[1]}%", f"{values[2]}%"
            
            return f"{decrease}%", f"{flat}%", f"{increase}%"
    except:
        pass
    return "15%", "8%", "77%" # 備用預設

def notify_my_iphone(title, msg):
    """ 🦉 升級版貓頭鷹：改用更安全的 POST 專車，繞過官方伺服器的阻擋 """
    url = "https://api.day.app/push"
    payload = {
        "device_key": MY_SECRET_KEY,
        "title": title,
        "body": msg,
        "badge": 1,
        "sound": "minions.caf" # 讓它發出可愛的聲音（可不加）
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"後台回應狀態碼: {response.status_code}")
    except Exception as e:
        print(f"發送失敗: {e}")
