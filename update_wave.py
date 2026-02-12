import requests
import json
from datetime import datetime

def get_wave_data():
    # 서해중부 안쪽먼바다 대표 좌표
    lat, lon = 37.0, 125.5
    url = f"https://marine-api.open-meteo.com/v1/marine?latitude={lat}&longitude={lon}&hourly=wave_height&timezone=Asia%2FSeoul&forecast_days=16"
    
    response = requests.get(url)
    data = response.json()
    
    hourly_time = data['hourly']['time']
    hourly_wave = data['hourly']['wave_height']
    
    result_json = {}
    
    # 데이터를 24시간 단위(하루)로 처리
    for i in range(0, len(hourly_wave), 24):
        day_waves = hourly_wave[i:i+24]
        if len(day_waves) < 24: break
        
        date_str = hourly_time[i].split('T')[0]
        
        # 오전(00-12시) 및 오후(12-24시) 분할
        am_waves = day_waves[0:12]
        pm_waves = day_waves[12:24]
        
        am_max = max(am_waves)
        pm_max = max(pm_waves)
        
        # 2.0m 초과 시 Closed 기준 적용
        result_json[date_str] = [
            {"t": "오전(Mateo)", "low": min(am_waves), "high": am_max, "s": "Closed" if am_max > 2.0 else "Open"},
            {"t": "오후(Mateo)", "low": min(pm_waves), "high": pm_max, "s": "Closed" if pm_max > 2.0 else "Open"}
        ]
    
    # 파일 저장
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(result_json, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get_wave_data()
