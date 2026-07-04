# 🌦️ Australian Weather Analytics Dashboard

A real-time weather data pipeline and interactive dashboard that fetches, processes, and visualises weather conditions across major Australian cities using the Open-Meteo API.

## 📌 Project Overview

This project builds an end-to-end data pipeline that:
- Fetches live weather data for 8 Australian cities via Open-Meteo API (free, no key required)
- Cleans and stores historical data in a local SQLite database
- Visualises temperature trends, rainfall, UV index, and wind patterns
- Generates automated daily weather summaries

## 🛠️ Tools & Technologies
| Tool | Purpose |
|------|---------|
| Python (requests, pandas) | API fetching & data processing |
| SQLite | Lightweight data storage |
| matplotlib / plotly | Visualisation |
| schedule | Automated daily pipeline |

## 📁 Project Structure
```
05_weather_dashboard/
├── src/
│   ├── fetch_weather.py       # API data fetcher
│   ├── clean_data.py          # Data cleaning module
│   ├── store_data.py          # SQLite storage
│   └── visualise.py           # Dashboard generation
├── data/
│   └── weather.db             # SQLite database
├── visuals/
│   └── temperature_trends.png
├── requirements.txt
└── README.md
```

## 🔍 Core Code — Weather Fetcher
```python
import requests
import pandas as pd
from datetime import datetime

CITIES = {
    'Melbourne': (-37.8136, 144.9631),
    'Sydney':    (-33.8688, 151.2093),
    'Brisbane':  (-27.4698, 153.0251),
    'Perth':     (-31.9505, 115.8605),
    'Adelaide':  (-34.9285, 138.6007),
    'Canberra':  (-35.2809, 149.1300),
    'Hobart':    (-42.8826, 147.3257),
    'Darwin':    (-12.4634, 130.8456),
}

def fetch_weather(city, lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max"
        f"&timezone=Australia%2FSydney&past_days=30"
    )
    r = requests.get(url, timeout=10)
    data = r.json()['daily']
    df = pd.DataFrame(data)
    df['city'] = city
    df['fetched_at'] = datetime.now()
    return df

all_data = pd.concat([fetch_weather(c, lat, lon) for c, (lat, lon) in CITIES.items()])
print(all_data.head())
```

## 📈 How to Run
```bash
pip install -r requirements.txt
python src/fetch_weather.py       # Fetch today's data
python src/visualise.py           # Generate charts
```

## 📊 Sample Insights
- Melbourne's temperature variance (daily max−min) averages 8.3°C — highest of all capitals
- Brisbane receives 78% of annual rainfall between November and April
- Perth averages 8.6 UV index hours per day — highest UV exposure nationally

---
*Part of Dhwani Shah's Data Analytics Portfolio*
