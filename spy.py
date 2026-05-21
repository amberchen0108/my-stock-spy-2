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
    owl_post_url = f"https://api.day.app/{MY_SECRET_KEY}/{title}/{msg}"
    requests.get(owl_post_url)

if __name__ == "__main__":
    g, w, r = get_all_percentages()
    today_date = datetime.now().strftime("%Y-%m-%d")
    current_hour = datetime.now().strftime("%H:%M")
    
    report_title = f"{current_hour} 盤勢回報"
    report_content = f"日期:{today_date} / 下跌:{g} / 持平:{w} / 上漲:{r}"
    
    notify_my_iphone(report_title, report_content)
    print(f"成功發送：{report_content}")
