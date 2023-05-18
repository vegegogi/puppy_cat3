import streamlit as st
import pandas as pd
import datetime
from datetime import date
import matplotlib.pyplot as plt
import matplotlib 
from io import BytesIO
import folium
from streamlit_folium import st_folium
import seaborn as sns
import plotly.express as px
#==========================================================================

def main() : 
    st.set_page_config(layout="wide")
    st.title("맛집을 한번 가보자😋")


    # 데이터 불러오기
    pet_food = pd.read_csv('./pet_food_FN3.csv')
    
    # 상좌: 지역 선택 버튼
    st.subheader("맛집 탐방하고 싶은 지역을 설정하세요")
    seoul_gu_list = [
        '강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구',
        '동대문구', '동작구', '마포구', '서대문구', '서초구', '성동구', '성북구', '송파구', '양천구', '영등포구',
        '용산구', '은평구', '종로구', '중구', '중랑구'
    ]
    selected_region = st.selectbox("서울 26개구 중 선택", seoul_gu_list)
    tmp_df = pet_food['지역(구)'] == selected_region

    # 상우: polium 맵
    st.subheader("강아지랑 같이 갈 수 있는 맛집은 어딜까?")
            
    # 데이터프레임 생성 예시
    data = {'가게명': list(pet_food['가게명']),
            '메인메뉴': list(pet_food['메인메뉴']),
            '지역(구)': list(pet_food['지역(구)']),
            '카테고리1' : list(pet_food['카테고리1']),
            '위도': list(pet_food['y']),
            '경도': list(pet_food['x'])}
    
    df = pd.DataFrame(data)

    # 서울 특별시의 위도와 경도
    seoul_latitude = 37.5665
    seoul_longitude = 126.9780

    # 지도 생성
    map = folium.Map(location=[seoul_latitude, seoul_longitude], zoom_start=11)

    # 데이터프레임 반복 처리하여 마커 추가
    for index, row in df[tmp_df].iterrows():
        if row['카테고리1'] == '카페':
            icon_color = 'black'
            icon_name = 'coffee'
        else:
            icon_color = 'pink'
            icon_name = 'cutlery'
        
        popup_content = folium.Popup("<b>가게명:</b> " + row['가게명'] + "<br><b>메인메뉴:</b> " + str(row['메인메뉴']) + "<br><b>지역(구):</b> " + str(row['지역(구)']) , max_width=200)
        marker = folium.Marker([row['위도'], row['경도']], popup=popup_content, icon=folium.Icon(color=icon_color, icon=icon_name, prefix='fa'))
        
        # 아이콘에 맞게 마크 추가
        if row['카테고리1'] == '카페':
            marker.add_to(map)
        else:
            marker.add_to(map)

    st_data = st_folium(map, width = 1500)

if __name__ == "__main__" :
    main()
