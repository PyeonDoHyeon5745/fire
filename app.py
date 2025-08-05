import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import math
import os

##############################  🖥️ 페이지 설정 ##############################

# 🖥️ 페이지 설정
st.set_page_config(page_title="재화재 예측 분석 시스템", layout="wide", page_icon="⚠️") 

# 🎨 스타일 정의
st.markdown("""
<style>
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin-top: 2rem;
    }

    .metric-box {
        flex: 1;
        margin: 0 1rem;
        padding: 2rem;
        background: #f4f6fa;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        text-align: center;
        transition: transform 0.3s ease;
    }

    .metric-box:hover {
        transform: translateY(-5px);
    }

    .metric-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 1rem;
    }

    .metric-value {
        font-size: 2.8rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# 🔥 메인 제목
st.markdown("""
<div style="text-align: center; padding-top: 2rem;">
    <h1 style="font-size: 2.8rem;"> 🔥 재화재 예측 분석 시스템 🔥</h1>
    <p style="font-size: 1.2rem; color: gray;">종합리포트</p>
</div>
""", unsafe_allow_html=True)

# 📌 핵심지표 요약 제목 추가
st.markdown("""
<div style="text-align: left; margin-top: 3rem; margin-bottom: 1rem;">
    <h2 style="font-weight: 700; font-size: 1.5rem;">📌 핵심지표 요약</h2>
</div>
""", unsafe_allow_html=True)

# ✅ 박스 4개 (더미 값)
num_sources = 4362
num_detections = 75
num_types = 97.2
success_rate = 87.9

st.markdown(f"""
<div class="metric-container">
    <div class="metric-box">
        <div class="metric-title">🏭 총 건물 수</div>
        <div class="metric-value">{num_sources}개</div>
    </div>
    <div class="metric-box">
        <div class="metric-title">⚠️ 고위험 건물 수 (90점 기준)</div>
        <div class="metric-value">{num_detections}건</div>
    </div>
    <div class="metric-box">
        <div class="metric-title">📊 고위험 건물 재화재 비율</div>
        <div class="metric-value">{num_types}%</div>
    </div>
    <div class="metric-box">
        <div class="metric-title">📈 상위 10% 화재 위험도 </div>
        <div class="metric-value">{success_rate:.1f}점</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 🔽 아래에 시각화 삽입 예정
st.markdown("---")
st.markdown("### 📊 분석 시각화 자료")
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# 📊 전체 피처 중요도 데이터
labels = [
    '노후도', '화재하중', '업종', '위험물', '자동감지',
    '층수', '구조', '제연', '자동소화', '피난',
    '소방접근성', '위험지역'
]
values = [
    26.47, 19.61, 9.8, 10.78, 10.78,
    12.75, 5.88, 2.94, 0.98, 0.0,
    0.0, 0.0
]

# 정렬된 데이터프레임 생성
df = pd.DataFrame({'항목': labels, '중요도': values})
df_sorted = df.sort_values(by='중요도', ascending=True)

# 눈에 잘 띄는 색상 팔레트 (0%도 강조됨)
colors = ['#CED4DA', '#CED4DA', '#CED4DA'] + [  # 0%는 회색
    '#4D96FF', '#38BDF8', '#16A34A', '#FACC15', '#F97316',
    '#EF4444', '#E11D48', '#A855F7', '#0EA5E9', '#FF6B6B'
]

# 🎯 수평 막대그래프 출력
st.markdown("### 📊 예측 피처 중요도 (전체 변수 포함)")

fig_bar = go.Figure(go.Bar(
    x=df_sorted['중요도'],
    y=df_sorted['항목'],
    orientation='h',
    marker_color=colors[:len(df_sorted)],
    text=[f"{v:.2f}%" for v in df_sorted['중요도']],
    textposition='auto'
))

fig_bar.update_layout(
    xaxis_title='중요도 (%)',
    yaxis_title='',
    height=600,
    margin=dict(t=40, b=40, l=60, r=10)
)

st.plotly_chart(fig_bar, use_container_width=True)


import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import io

# 📁 서울 화재 분석용 CSV 불러오기
df = pd.read_csv("seoul_fire_predict.csv")

# 🔍 위험도_혼합 컬럼 숫자로 정제
df['위험도_혼합'] = df['위험도_혼합'].astype(str).str.extract(r'(\d+\.\d+|\d+)')[0]
df['위험도_혼합'] = pd.to_numeric(df['위험도_혼합'], errors='coerce')
df = df[df['위험도_혼합'].notnull() & df['위험도_혼합'].apply(lambda x: isinstance(x, float))]

# 🎨 Streamlit용 Seaborn 시각화 -> 이미지로 출력
fig, ax = plt.subplots(figsize=(8, 6))

# KDE plot
sns.kdeplot(data=df[df['재발생'] == 1], x='위험도_혼합', fill=True, label='재발생 O', color='skyblue')
sns.kdeplot(data=df[df['재발생'] == 0], x='위험도_혼합', fill=True, label='재발생 X', color='orange')

# 레이아웃 및 제목
plt.title('XGBoost 기반 혼합 위험도 분포', fontsize=16)
plt.xlabel('혼합 위험도 점수', fontsize=13)
plt.ylabel('밀도', fontsize=13)
plt.legend()

# 📊 Streamlit에 표시
st.markdown("### 🔥 XGBoost 기반 혼합 위험도 분포")
st.pyplot(fig)
