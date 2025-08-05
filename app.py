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
st.markdown("### 📊 시각화 자료")
# (여기에 그래프나 표 삽입)

