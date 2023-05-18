import os
import io
import csv
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

import matplotlib.pyplot as plt
import seaborn as sns
import folium
import streamlit as st
from streamlit_folium import st_folium
st.set_page_config(layout="wide")


pet_place_clean = pd.read_csv('./pet_place_clean_ver1.csv').iloc[:, 1:]
df = pd.DataFrame(pet_place_clean)
df['카테고리'] = df['카테고리3'].map({'미술관': '문화시설', '박물관': '문화시설', '여행지': '문화시설', '동물병원' : '의료시설', '동물약국' : '의료시설'})
df1 = df[df['반려동물 동반 가능정보']=='동반가능']
seoul = df1[df1['시도 명칭'] == '서울특별시']
seoul1 = seoul[['시설명','카테고리','카테고리3','시군구 명칭','도로명주소','전화번호','휴무일','운영시간','주차 가능여부','위도','경도']]
seoul1.reset_index()
seoul2 = seoul1
medical = seoul2[seoul2['카테고리'] == '의료시설']
life = seoul2[seoul2['카테고리'] == '문화시설']

# 문화 제목
plt.rc('font', family='NanumGothic')
st.title("서울특별시 반려동물 문화서비스🎨")
# 문화 사이드바
st.subheader('🔔반려동물 문화서비스 조회🔔')
select_gu = st.selectbox(
        '확인하고 싶은 시군구를 선택하세요',
        ['종로구','중구','용산구','성동구','광진구','동대문구','중랑구','성북구','강북구','도봉구','노원구','은평구','서대문구','마포구','양천구',
        '강서구','구로구','금천구','영등포구','동작구','관악구','서초구','강남구','송파구','강동구']
    )
tmp_df = life['시군구 명칭'] == select_gu

# 문화 리스트
st.subheader("운영 시설 리스트",)
st.dataframe(life[tmp_df].head(), height=200)

# 사이드바에 문화시설 cvs 파일 다운로드 버튼
st.markdown("**반려동물 문화시설 정보 다운로드**")
csv_data = life[tmp_df].to_csv(index=False)
# Button code
st.download_button("CSV 파일 다운로드 받기", csv_data, file_name='life_facility_data.csv')

# 문화 시설 지도
st.subheader("운영 시설 지도")
data = {'시설명': list(life['시설명']),
            '휴무일': list(life['휴무일']),
            '운영시간': list(life['운영시간']),
            '위도': list(life['위도']),
            '경도': list(life['경도'])}
df = pd.DataFrame(data)

    # 서울 특별시의 위도와 경도
seoul_latitude = 37.5665
seoul_longitude = 126.9780

# 지도 생성
map = folium.Map(location=[seoul_latitude, seoul_longitude], zoom_start=13)



# 데이터프레임 반복 처리하여 마커 추가
for index, row in life[tmp_df].iterrows():
        popup_content = folium.Popup("<b>시설명:</b> " + row['시설명'] + "<br><b>휴무일:</b> " + str(row['휴무일']) \
            + "<br><b>운영시간:</b> " + row['운영시간'], max_width=200)  # 여러 내용을 팝업에 추가
        folium.Marker([row['위도'], row['경도']], popup=popup_content, \
            icon=folium.Icon(color='pink', icon='paw', prefix='fa')).add_to(map)


st_data = st_folium(map, width=1500)

