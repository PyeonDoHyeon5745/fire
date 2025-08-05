import streamlit as st
import pandas as pd
import folium
import requests
from streamlit_folium import st_folium
import openai
import math
import os


# ✅ GPT 클라이언트 생성 (OpenAI v1.x 이상 기준)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ✅ 세션 상태 초기화는 GPT 호출보다 위에 있어야 함
if "firechat" not in st.session_state:
    st.session_state.firechat = [
        {"role": "system", "content": "당신은 화재 재발 방지와 안전에 대한 전문가입니다. 친절하고 구체적으로 답변해 주세요."}
    ]


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

# 🔥 제목
st.markdown("""
<div style="text-align: center; padding-top: 2rem;">
    <h1 style="font-size: 2.8rem;"> 🔥 재화재 예측 분석 시스템 🔥</h1>
    <p style="font-size: 1.2rem; color: gray;">종합리포트</p>
</div>
""", unsafe_allow_html=True)

# ✅ 박스 4개 (더미 값)
num_sources = 128
num_detections = 64
num_types = 5
success_rate = 87.5

st.markdown(f"""
<div class="metric-container">
    <div class="metric-box">
        <div class="metric-title">🏭 총 건물 수</div>
        <div class="metric-value">{num_sources}개</div>
    </div>
    <div class="metric-box">
        <div class="metric-title">⚠️ 고위험 건물 예측 수</div>
        <div class="metric-value">{num_detections}건</div>
    </div>
    <div class="metric-box">
        <div class="metric-title">📊 오늘의 날씨</div>
        <div class="metric-value">{num_types}종</div>
    </div>
    <div class="metric-box">
        <div class="metric-title">📈 분석 성공률</div>
        <div class="metric-value">{success_rate:.1f}%</div>
    </div>
</div>
""", unsafe_allow_html=True)

############################## GPT 인터페이스 ##############################
# OpenAI 클라이언트 초기화
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


st.markdown("---")
st.subheader("🧠 GPT 기반 화재 관련 질문 상담")

# 이전 대화 출력
for msg in st.session_state.firechat[1:]:
    if msg["role"] == "user":
        st.markdown(f"<div style='text-align:right; background-color:#dcf8c6; padding:8px; border-radius:10px; margin:5px 0;'>{msg['content']}</div>", unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f"<div style='text-align:left; background-color:#fff; padding:8px; border-radius:10px; margin:5px 0;'>{msg['content']}</div>", unsafe_allow_html=True)

# 입력 폼
with st.form("firechat_form", clear_on_submit=True):
    user_input = st.text_input("🔥 화재 관련 궁금한 점을 입력해 보세요!")
    submitted = st.form_submit_button("보내기")

# GPT 응답 처리
if submitted and user_input:
    st.session_state.firechat.append({"role": "user", "content": user_input})

    with st.spinner("GPT가 답변을 작성 중입니다..."):
        reply = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.firechat
        ).choices[0].message.content

    st.session_state.firechat.append({"role": "assistant", "content": reply})
    st.rerun()
