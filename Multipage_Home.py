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
from PIL import Image

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>🐶서울특별시 반려동물 종합 플랫폼🐶</h1>", unsafe_allow_html=True)

# 이미지 표시
image_local = Image.open('main_banner.png')
st.image(image_local, width=1050, use_column_width=True, caption='Image')

# 배경 이미지 설정
background_image = "main_banner.png"

# CSS 스타일로 배경 이미지 적용
css = f"""
<style>
body {{
    background-image: url("{background_image}");
    background-size: cover;
}}
</style>
"""

st.markdown(css, unsafe_allow_html=True)
