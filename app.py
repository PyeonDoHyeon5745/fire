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

# -------------------------------
# 📊 SHAP 기반 중요도 데이터 입력
# -------------------------------
data = {
    '항목': ['노후도', '화재하중', '층수', '위험물', '자동감지', '업종', '구조', '제연', '자동소화'],
    '가중치': [26.47, 19.61, 12.75, 10.78, 10.78, 9.8, 5.88, 2.94, 0.98]
}

df = pd.DataFrame(data)

# -------------------------------
# 🎨 컬러 설정
# -------------------------------
colors = ['#FF6B6B', '#FFA94D', '#FFD43B', '#69DB7C', '#748FFC', '#5C7CFA', '#9775FA', '#D0BFFF', '#A5D8FF']

# -------------------------------
# 📈 도넛 차트 생성
# -------------------------------
donut_fig = go.Figure(data=[go.Pie(
    labels=df['항목'],
    values=df['가중치'],
    hole=0.6,
    marker_colors=colors,
    textinfo='label+percent',
    insidetextorientation='radial'
)])

donut_fig.update_layout(
    title_text='📊 예측 피처 중요도 (도넛 차트)',
    annotations=[dict(text='Feature 중요도', x=0.5, y=0.5, font_size=15, showarrow=False)],
    showlegend=False,
    margin=dict(t=40, b=10, l=0, r=0)
)

# -------------------------------
# 📊 막대그래프 생성 (가중치 순 정렬)
# -------------------------------
bar_df = df.sort_values(by='가중치', ascending=True)

bar_fig = go.Figure(go.Bar(
    x=bar_df['가중치'],
    y=bar_df['항목'],
    orientation='h',
    marker_color=colors[:len(bar_df)],
    text=bar_df['가중치'].astype(str) + '%',
    textposition='auto'
))

bar_fig.update_layout(
    title='📋 예측 피처 중요도 (막대그래프)',
    xaxis_title='중요도 (%)',
    yaxis_title='',
    margin=dict(t=40, b=20, l=0, r=0)
)

# -------------------------------
# 📌 Streamlit 시각화 영역
# -------------------------------
st.markdown("## 🎯 예측 피처 중요도 시각화")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(donut_fig, use_container_width=True)

with col2:
    st.plotly_chart(bar_fig, use_container_width=True)


