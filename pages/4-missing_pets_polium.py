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
    st.title("최근 서울에서 실종된 강아지😥")
    st.subheader('(2022년 5월 15일 ~ 2023년 5월 15일)')

    # 데이터 불러오기
    missing_pets = pd.read_csv('./missing_pets_2223_xy_2.csv')
    missing_pets['연락처'] = '010-XXXX-XXXX'

    st.subheader('최근 노원구에서 가장 많이 강아지가 사라졌습니다')

    #시각화
    fig = px.histogram(missing_pets, x='지역(구)')
    fig.update_layout(title='실종 강아지 분포', xaxis_title='지역(구)', yaxis_title='강아지 수')
    fig.update_xaxes(tickangle=45)

    st.plotly_chart(fig)
    
    # 상좌: 지역 선택 버튼
    st.subheader("강아지 실종 현황이 궁금한 지역을 설정하세요")
    seoul_gu_list = [
        '강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구',
        '동대문구', '동작구', '마포구', '서대문구', '서초구', '성동구', '성북구', '송파구', '양천구', '영등포구',
        '용산구', '은평구', '종로구', '중구', '중랑구'
    ]
    selected_region = st.selectbox("서울 26개구 중 선택", seoul_gu_list)
    tmp_df = missing_pets['지역(구)'] == selected_region

    # 상우: polium 맵
    st.subheader("궁금한 지역의 강아지 실종현황입니다")
            
    # 데이터프레임 생성 예시
    data = {'주소': list(missing_pets['분실장소2']),
            '분실날짜': list(missing_pets['분실날짜']),
            '품종': list(missing_pets['품종']),
            '성별': list(missing_pets['성별']),
            '색상': list(missing_pets['색상']),
            '지역(구)': list(missing_pets['지역(구)']),
            '연락처' : list(missing_pets['연락처']), 
            '위도': list(missing_pets['y']),
            '경도': list(missing_pets['x'])}
    df = pd.DataFrame(data)

    # 서울 특별시의 위도와 경도
    seoul_latitude = 37.5665
    seoul_longitude = 126.9780

    # 지도 생성
    map = folium.Map(location=[seoul_latitude, seoul_longitude], zoom_start=11)

    # 데이터프레임 반복 처리하여 마커 추가
    for index, row in df[tmp_df].iterrows():
        popup_content = folium.Popup("<b>주소:</b> " + row['주소'] + "<br><b>분실날짜:</b> " + str(row['분실날짜']) + 
                                    "<br><b>품종:</b> " + row['품종'] + "<br><b>성별:</b> " + row['성별'] + 
                                    "<br><b>색상:</b> " + row['색상'] + "<br><b>연락처:</b> " + row['연락처'], max_width=200)  # 여러 내용을 팝업에 추가
        folium.Marker([row['위도'], row['경도']], popup=popup_content, icon=folium.Icon(color='red', icon='paw', prefix='fa')).add_to(map)
    
    st_data = st_folium(map, width = 1500)



if __name__ == "__main__" :
    main()
