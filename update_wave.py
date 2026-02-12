import requests
import json
from datetime import datetime, timedelta

def update_port_data():
    lat, lon = 37.0, 125.5
    # 향후 16일치 데이터를 가져옵니다.
    url = f"https://marine-api.open-meteo.com/v1/marine?latitude={lat}&longitude={lon}&hourly=wave_height&timezone=Asia/Seoul&forecast_days=16"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        hourly_time = data['hourly']['time']
        hourly_wave = data['hourly']['wave_height']
        
        new_data = {}
        
        # 24시간 단위로 루프 돌며 오전/오후 분할
        for i in range(0, len(hourly_wave), 24):
            day_waves = hourly_wave[i:i+24]
            if len(day_waves) < 24: break
            
            date_str = hourly_time[i].split('T')[0]
            
            # 오전(00-12시), 오후(12-24시) 분할 및 최대값 계산
            am_waves = day_waves[0:12]
            pm_waves = day_waves[12:24]
            
            am_max = max(am_waves)
            pm_max = max(pm_waves)
            
            # 2.0m 초과 시 Closed 기준 적용
            new_data[date_str] = [
                {"t": "오전(Mateo)", "low": str(min(am_waves)), "high": str(am_max), "s": "Closed" if am_max > 2.0 else "Open"},
                {"t": "오후(Mateo)", "low": str(min(pm_waves)), "high": str(pm_max), "s": "Closed" if pm_max > 2.0 else "Open"}
            ]
            
        # 기존 데이터와 병합 (과거 기록 유지)
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                old_data = json.load(f)
                old_data.update(new_data)
                final_data = old_data
        except:
            final_data = new_data

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)
            
        print(f"Update Success: {datetime.now()}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_port_data()
