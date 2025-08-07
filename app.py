import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import math
import os
import plotly.graph_objects as go
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

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

# 📌 핵심지표 요약 제목
st.markdown("""
<div style="text-align: left; margin-top: 3rem; margin-bottom: 1rem;">
    <h2 style="font-weight: 700; font-size: 1.5rem;">📌 핵심지표 요약</h2>
</div>
""", unsafe_allow_html=True)

# ✅ 핵심지표 값
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
        <div class="metric-title">📈 상위 10% 화재 위험도</div>
        <div class="metric-value">{success_rate:.1f}점</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 📊 시각화 구간 시작
st.markdown("---")
st.markdown("### 📊 분석 시각화 자료")

# ▶ 두 개 컬럼으로 나눔
col1, col2 = st.columns(2)

# 📊 피처 중요도 그래프 (왼쪽)
with col1:
    st.markdown("### 재화재 예측 중요 변수")

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

    df_feat = pd.DataFrame({'항목': labels, '중요도': values})
    df_feat_sorted = df_feat.sort_values(by='중요도', ascending=True)

    colors = ['#CED4DA'] * 3 + [
        '#4D96FF', '#38BDF8', '#16A34A', '#FACC15', '#F97316',
        '#EF4444', '#E11D48', '#A855F7', '#0EA5E9', '#FF6B6B'
    ]

    fig_bar = go.Figure(go.Bar(
        x=df_feat_sorted['중요도'],
        y=df_feat_sorted['항목'],
        orientation='h',
        marker_color=colors[:len(df_feat_sorted)],
        text=[f"{v:.2f}%" for v in df_feat_sorted['중요도']],
        textposition='auto'
    ))

    fig_bar.update_layout(
        xaxis_title='중요도 (%)',
        yaxis_title='',
        height=600,
        margin=dict(t=40, b=40, l=60, r=10)
    )

    st.plotly_chart(fig_bar, use_container_width=True)

# 📈 서울 KDE 분포 그래프 (오른쪽)
with col2:
    st.markdown("### 🔥 서울 재화재 예측 분포 🔥")

    df_seoul = pd.read_csv("seoul_fire_predict.csv")
    df_seoul['위험도_혼합'] = df_seoul['위험도_혼합'].astype(str).str.extract(r'(\d+\.\d+|\d+)')[0]
    df_seoul['위험도_혼합'] = pd.to_numeric(df_seoul['위험도_혼합'], errors='coerce')
    df_seoul = df_seoul[df_seoul['위험도_혼합'].notnull()]

    sns.set_theme(style="white")
    ax = sns.kdeplot(df_seoul[df_seoul['RLPS_YN'] == 1]['위험도_혼합'], bw_adjust=1)
    x1, y1 = ax.lines[0].get_data()
    plt.close()

    ax = sns.kdeplot(df_seoul[df_seoul['RLPS_YN'] == 0]['위험도_혼합'], bw_adjust=1)
    x2, y2 = ax.lines[0].get_data()
    plt.close()

    fig_density = go.Figure()
    fig_density.add_trace(go.Scatter(
        x=x1, y=y1,
        mode='lines',
        fill='tozeroy',
        name='재발생 O',
        line=dict(color='skyblue')
    ))
    fig_density.add_trace(go.Scatter(
        x=x2, y=y2,
        mode='lines',
        fill='tozeroy',
        name='재발생 X',
        line=dict(color='orange')
    ))

    fig_density.update_layout(
        title='서울 재화재 예측 분포',
        xaxis_title='재화재 점수',
        yaxis_title='밀도',
        legend_title='재발생 여부',
        template='plotly_white',
        height=600,
        margin=dict(t=40, b=40, l=40, r=10)
    )

    st.plotly_chart(fig_density, use_container_width=True)

