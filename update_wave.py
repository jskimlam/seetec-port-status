import requests
import json
from datetime import datetime

def update_port_data():
    lat, lon = 37.0, 125.5
    url = f"https://marine-api.open-meteo.com/v1/marine?latitude={lat}&longitude={lon}&hourly=wave_height&timezone=Asia/Seoul&forecast_days=17"
    
    try:
        response = requests.get(url)
        data = response.json()
        hourly_time = data['hourly']['time']
        hourly_wave = data['hourly']['wave_height']
        
        # 기존 데이터 불러오기
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                stored_data = json.load(f)
        except:
            stored_data = {}

        # 17일치 루프
        for i in range(0, len(hourly_wave), 24):
            day_waves = hourly_wave[i:i+24]
            if len(day_waves) < 24: break
            date_str = hourly_time[i].split('T')[0]
            
            am_max = max(day_waves[0:12])
            pm_max = max(day_waves[12:24])
            
            new_day_records = [
                {"t": "오전(Mateo)", "low": str(min(day_waves[0:12])), "high": str(am_max), "s": "Closed" if am_max > 2.0 else "Open"},
                {"t": "오후(Mateo)", "low": str(min(day_waves[12:24])), "high": str(pm_max), "s": "Closed" if pm_max > 2.0 else "Open"}
            ]

            # 피크 홀드 로직: 기존 데이터가 있으면 비교 후 큰 값 유지
            if date_str in stored_data:
                for idx, new_rec in enumerate(new_day_records):
                    old_high = float(stored_data[date_str][idx]['high'])
                    new_high = float(new_rec['high'])
                    if new_high > old_high:
                        stored_data[date_str][idx] = new_rec # 더 높은 파고가 나오면 갱신
            else:
                stored_data[date_str] = new_day_records

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(stored_data, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_port_data()
