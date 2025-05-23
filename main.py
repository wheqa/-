# requirements.txt
streamlit
requests

import streamlit as st
import requests

# OpenWeatherMap API 키를 secrets.toml에서 가져옵니다.
# 실제 배포 시에는 이렇게 사용하는 것이 보안상 안전합니다.
API_KEY = st.secrets["OPENWEATHERMAP_API_KEY"]
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city_name):
    """
    도시 이름을 받아 OpenWeatherMap API에서 날씨 정보를 가져옵니다.
    """
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric",  # 섭씨 온도를 원하면 'metric', 화씨는 'imperial'
        "lang": "kr"        # 한국어로 날씨 정보를 가져옵니다.
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # HTTP 오류가 발생하면 예외 발생
        weather_data = response.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        st.error(f"날씨 정보를 가져오는 데 오류가 발생했습니다: {e}")
        return None

def display_weather(weather_data):
    """
    가져온 날씨 데이터를 스트림릿에 표시합니다.
    """
    if weather_data:
        st.subheader(f"{weather_data['name']}의 현재 날씨")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("온도", f"{weather_data['main']['temp']:.1f}°C")
            st.metric("체감 온도", f"{weather_data['main']['feels_like']:.1f}°C")
        with col2:
            st.metric("최저/최고 온도", f"{weather_data['main']['temp_min']:.1f}°C / {weather_data['main']['temp_max']:.1f}°C")
            st.metric("습도", f"{weather_data['main']['humidity']}%")
        with col3:
            st.metric("기압", f"{weather_data['main']['pressure']} hPa")
            st.metric("바람", f"{weather_data['wind']['speed']:.1f} m/s")

        st.write(f"**날씨**: {weather_data['weather'][0]['description'].capitalize()}")

        # 날씨 아이콘 표시 (옵션)
        icon_code = weather_data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        st.image(icon_url, width=100)

    else:
        st.warning("도시 이름을 확인하거나, 잠시 후 다시 시도해주세요.")

# Streamlit 앱의 메인 부분
st.title("간단 날씨 정보 앱 ☀️")

city = st.text_input("도시 이름을 입력하세요 (예: Seoul, Tokyo, New York)", "Seoul")

if st.button("날씨 확인"):
    if city:
        weather_data = get_weather(city)
        display_weather(weather_data)
    else:
        st.warning("도시 이름을 입력해주세요.")

st.markdown("---")
st.markdown("powered by [OpenWeatherMap](https://openweathermap.org/)")
