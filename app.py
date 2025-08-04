{\rtf1\ansi\ansicpg949\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import pandas as pd\
import requests\
import re\
from openai import OpenAI\
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])\
\
\
# \uc0\u54168 \u51060 \u51648  \u49444 \u51221 \
st.set_page_config(page_title="\uc0\u51116 \u54868 \u51116  \u50696 \u52769  \u49884 \u48044 \u47112 \u51060 \u49496 ", layout="wide", page_icon="\u9888 \u65039 ")\
\
# \uc0\u54532 \u47532 \u48120 \u50628  \u49828 \u53440 \u51068  \u51221 \u51032 \
st.markdown("""\
<style>\
    .metric-container \{\
        display: flex;\
        justify-content: space-around;\
        margin-top: 2rem;\
    \}\
\
    .metric-box \{\
        flex: 1;\
        margin: 0 1rem;\
        padding: 2rem;\
        background: #f4f6fa;\
        border-radius: 16px;\
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);\
        text-align: center;\
        transition: transform 0.3s ease;\
    \}\
\
    .metric-box:hover \{\
        transform: translateY(-5px);\
    \}\
\
    .metric-title \{\
        font-size: 1.1rem;\
        font-weight: 600;\
        color: #333;\
        margin-bottom: 1rem;\
    \}\
\
    .metric-value \{\
        font-size: 2.8rem;\
        font-weight: bold;\
        background: linear-gradient(135deg, #667eea, #764ba2);\
        -webkit-background-clip: text;\
        -webkit-text-fill-color: transparent;\
    \}\
</style>\
""", unsafe_allow_html=True)\
\
# \uc0\u49345 \u45800  \u51228 \u47785 \
st.markdown("""\
<div style="text-align: center; padding-top: 2rem;">\
    <h1 style="font-size: 2.8rem;"> \uc0\u55357 \u56613  \u51116 \u54868 \u51116  \u50696 \u52769  \u49884 \u48044 \u47112 \u51060 \u49496 </h1>\
    <p style="font-size: 1.2rem; color: gray;">\uc0\u54532 \u47532 \u48120 \u50628  \u54645 \u49900  \u51648 \u54364 </p>\
</div>\
""", unsafe_allow_html=True)\
\
# \uc0\u45908 \u48120  \u44050 \
num_sources = 128\
num_detections = 64\
num_types = 5\
success_rate = 87.5\
\
# \uc0\u45348 \u47784  \u48149 \u49828  4\u44060  \u52636 \u47141 \
st.markdown(f"""\
<div class="metric-container">\
    <div class="metric-box">\
        <div class="metric-title">\uc0\u55356 \u57325  \u49436 \u50872  \u54868 \u51116  \u48516 \u49437 </div>\
        <div class="metric-value">\{num_sources\}\uc0\u44060 \u49548 </div>\
    </div>\
    <div class="metric-box">\
        <div class="metric-title">\uc0\u9888 \u65039  \u45236  \u44148 \u47932  \u54868 \u51116  \u50948 \u54744 \u46020 </div>\
        <div class="metric-value">\{num_detections\}\uc0\u44148 </div>\
    </div>\
    <div class="metric-box">\
        <div class="metric-title">\uc0\u55357 \u56522  \u50724 \u45720 \u51032  \u45216 \u50472 </div>\
        <div class="metric-value">\{num_types\}\uc0\u51333 </div>\
    </div>\
    <div class="metric-box">\
        <div class="metric-title">\uc0\u55357 \u56520  \u48516 \u49437  \u49457 \u44277 \u47456 </div>\
        <div class="metric-value">\{success_rate:.1f\}%</div>\
    </div>\
</div>\
""", unsafe_allow_html=True)\
\
\
\
# \uc0\u52852 \u54168  \u54252 \u47607  \u54632 \u49688 \
def format_cafes(cafes_df):\
    cafes_df = cafes_df.drop_duplicates(subset=['c_name', 'c_value', 'c_review'])\
    result = []\
\
    if len(cafes_df) == 0:\
        return ("\uc0\u9749  \u54788 \u51116  \u51060  \u44288 \u44305 \u51648  \u51452 \u48320 \u50640  \u46321 \u47197 \u46108  \u52852 \u54168  \u51221 \u48372 \u45716  \u50630 \u50612 \u50836 .  \\n"\
                "\uc0\u54616 \u51648 \u47564  \u44540 \u52376 \u50640  \u49704 \u44200 \u51652  \u48372 \u49437  \u44057 \u51008  \u44277 \u44036 \u51060  \u51080 \u51012  \u49688  \u51080 \u51004 \u45768 ,  \\n"\
                "\uc0\u51648 \u46020 \u47484  \u54876 \u50857 \u54644  \u52380 \u52380 \u55176  \u44152 \u50612 \u48372 \u49884 \u45716  \u44163 \u46020  \u52628 \u52380 \u46300 \u47549 \u45768 \u45796  \u55357 \u56842 ")\
\
    elif len(cafes_df) == 1:\
        row = cafes_df.iloc[0]\
        if all(x not in row["c_review"] for x in ["\uc0\u50630 \u51020 ", "\u50630 \u51021 "]):\
            return f"""\uc0\u9749  **\u51452 \u48320  \u52628 \u52380  \u52852 \u54168 **\\n\\n- **\{row['c_name']\}** (\u11088  \{row['c_value']\})  \\n\'93\{row['c_review']\}\'94"""\
        else:\
            return f"""\uc0\u9749  **\u51452 \u48320  \u52628 \u52380  \u52852 \u54168 **\\n\\n- **\{row['c_name']\}** (\u11088  \{row['c_value']\})"""\
\
    else:\
        grouped = cafes_df.groupby(['c_name', 'c_value'])\
        result.append("\uc0\u9749  **\u51452 \u48320 \u50640  \u51060 \u47088  \u52852 \u54168 \u46308 \u51060  \u51080 \u50612 \u50836 ** \u55356 \u57148 \\n")\
        for (name, value), group in grouped:\
            reviews = group['c_review'].dropna().unique()\
            reviews = [r for r in reviews if all(x not in r for x in ["\uc0\u50630 \u51020 ", "\u50630 \u51021 "])]\
            top_reviews = reviews[:3]\
\
            if top_reviews:\
                review_text = "\\n".join([f"\'93\{r\}\'94" for r in top_reviews])\
                result.append(f"- **\{name\}** (\uc0\u11088  \{value\})  \\n\{review_text\}")\
            else:\
                result.append(f"- **\{name\}** (\uc0\u11088  \{value\})")\
\
        return "\\n\\n".join(result)\
\
# \uc0\u52488 \u44592  \u49464 \u49496  \u49444 \u51221 \
if "messages" not in st.session_state:\
    st.session_state.messages = [\
        \{"role": "system", "content": "\uc0\u45817 \u49888 \u51008  \u52397 \u51452  \u47928 \u54868 \u50976 \u49328 \u51012  \u49548 \u44060 \u54616 \u45716  \u44048 \u49457 \u51201 \u51060 \u44256  \u44277 \u49552 \u54620  \u47568 \u53804 \u51032  \u44288 \u44305  \u44032 \u51060 \u46300  \u52311 \u48391 \u51077 \u45768 \u45796 ."\}\
    ]\
\
st.title("\uc0\u55356 \u57310 \u65039  \u52397 \u51452  \u47928 \u54868  \u44288 \u44305 \u44032 \u51060 \u46300  \u55356 \u57310 \u65039 ")\
\
# \uc0\u51060 \u51204  \u47700 \u49884 \u51648  \u52636 \u47141 \
for msg in st.session_state.messages[1:]:\
    if msg["role"] == "user":\
        st.markdown(f"<div style='text-align: right; background-color: #dcf8c6; border-radius: 10px; padding: 8px; margin: 5px 0;'>\{msg['content']\}</div>", unsafe_allow_html=True)\
    elif msg["role"] == "assistant":\
        st.markdown(f"<div style='text-align: left; background-color: #ffffff; border-radius: 10px; padding: 8px; margin: 5px 0;'>\{msg['content']\}</div>", unsafe_allow_html=True)\
\
st.markdown("---")\
\
# \uc0\u51077 \u47141  \u54268  \u52376 \u47532 \
with st.form("chat_form"):\
    user_input = st.text_input("\uc0\u51648 \u46020 \u50640 \u49436  \u49440 \u53469 \u54620  \u44288 \u44305 \u51648 \u46308 \u51012  \u50668 \u44592 \u50640  \u51077 \u47141 \u54644 \u51452 \u49464 \u50836 ! ( \u49788 \u54364 (,)\u47196  \u44396 \u48516 \u54644  \u51452 \u49464 \u50836 . \u50696 : \u52397 \u51452  \u49888 \u49440 \u51452 , \u52397 \u51452  \u52397 \u45397 \u44033 )")\
    submitted = st.form_submit_button("\uc0\u48372 \u45236 \u44592 ")\
\
if submitted and user_input:\
    st.session_state.messages.append(\{"role": "user", "content": user_input\})\
\
    with st.spinner("\uc0\u52397 \u51452 \u51032  \u50500 \u47492 \u45796 \u50880 \u51012  \u51221 \u47532  \u51473 \u51077 \u45768 \u45796 ..."):\
        places = [p.strip() for p in user_input.split(',') if p.strip()]\
        response_blocks = []\
\
        # GPT \uc0\u49436 \u47200  \u49373 \u49457 \
        weather_intro = client.chat.completions.create(\
            model="gpt-3.5-turbo",\
            messages=[\
                \{"role": "system", "content": "\uc0\u45817 \u49888 \u51008  \u52397 \u51452  \u44288 \u44305 \u51012  \u49548 \u44060 \u54616 \u45716  \u44048 \u49457 \u51201 \u51060 \u44256  \u44277 \u49552 \u54620  \u50668 \u54665  \u44032 \u51060 \u46300 \u51077 \u45768 \u45796 ."\},\
                \{"role": "user", "content": "\uc0\u50724 \u45720  \u52397 \u51452 \u51032  \u45216 \u50472 , \u52628 \u52380  \u48373 \u51109 , \u44151 \u44592  \u51339 \u51008  \u49884 \u44036 \u45824 , \u49548 \u49548 \u54620  \u50668 \u54665  \u54017 , \u44228 \u51208  \u48516 \u50948 \u44592  \u46321 \u51012  \u51060 \u47784 \u51648 \u50752  \u54632 \u44760  \u46384 \u46907 \u54620  \u47568 \u53804 \u47196  \u49548 \u44060 \u54644  \u51452 \u49464 \u50836 . \u44288 \u44305 \u51648  \u49548 \u44060  \u51204  \u49436 \u47200 \u51004 \u47196  \u50424  \u45236 \u50857 \u51077 \u45768 \u45796 ."\}\
            ]\
        ).choices[0].message.content\
        response_blocks.append(f"\\U0001F324\uc0\u65039  \{weather_intro\}")\
\
        for place in places:\
            matched = data[data['t_name'].str.contains(place, na=False)]\
\
            gpt_place_response = client.chat.completions.create(\
                model="gpt-3.5-turbo",\
                messages=[\
                    \{"role": "system", "content": "\uc0\u45817 \u49888 \u51008  \u52397 \u51452  \u47928 \u54868 \u50976 \u49328 \u51012  \u49548 \u44060 \u54616 \u45716  \u44048 \u49457 \u51201 \u51060 \u44256  \u46384 \u46907 \u54620  \u47568 \u53804 \u51032  \u44277 \u49552 \u54620  \u44288 \u44305  \u44032 \u51060 \u46300 \u51077 \u45768 \u45796 . \u51060 \u47784 \u51648 \u46020  \u54413 \u48512 \u54616 \u44172  \u49324 \u50857 \u54616 \u49464 \u50836 ."\},\
                    \{"role": "user", "content": f"""\
\uc0\u50668 \u54665 \u51088 \u50640 \u44172  \u49444 \u47128 \u51060  \u45712 \u44788 \u51648 \u46020 \u47197 , \u46384 \u46907 \u54616 \u44256  \u44277 \u49552 \u54620  \u47568 \u53804 \u47196  \{place\}\u47484  \u49548 \u44060 \u54644  \u51452 \u49464 \u50836  \u10024   \
\uc0\u10004 \u65039  \u50669 \u49324 \u51201 \u51064  \u48176 \u44221 ,  \
\uc0\u10004 \u65039  \u48169 \u47928  \u49884 \u51032  \u48516 \u50948 \u44592 \u50752  \u44228 \u51208 \u51032  \u50612 \u50872 \u47548  \u55356 \u57155 \u55356 \u57144   \
\uc0\u10004 \u65039  \u51064 \u44540  \u54252 \u53664 \u49828 \u54047  \u55357 \u56568   \
\uc0\u10004 \u65039  \u50668 \u54665 \u51088 \u50640 \u44172  \u52628 \u52380 \u54616 \u45716  \u44048 \u49457 \u51201 \u51064  \u53076 \u47704 \u53944  \u55356 \u57151   \
\uc0\u47928 \u45800 \u47560 \u45796  \u51060 \u47784 \u51648 \u47484  \u54876 \u50857 \u54644  \u49373 \u46041 \u44048  \u51080 \u44172  \u51089 \u49457 \u54644  \u51452 \u49464 \u50836 . \u51460 \u48148 \u45000 \u46020  \u51201 \u51208 \u55176  \u54644  \u51452 \u49464 \u50836 .\
"""\}\
                ]\
            ).choices[0].message.content\
\
            if not matched.empty:\
                cafes = matched[['c_name', 'c_value', 'c_review']].drop_duplicates()\
                cafe_info = format_cafes(cafes)\
\
                t_value = matched['t_value'].dropna().unique()\
                score_text = f"\\n\\n\uc0\u55357 \u56522  **\u44288 \u44305 \u51648  \u54217 \u51216 **: \u11088  \{t_value[0]\}" if len(t_value) > 0 else ""\
\
                reviews = matched['t_review'].dropna().unique()\
                reviews = [r for r in reviews if all(x not in r for x in ["\uc0\u50630 \u51020 ", "\u50630 \u51021 "])]\
                if len(reviews) > 0:\
                    top_reviews = list(reviews)[:3]\
                    review_text = "\\n".join([f"\'93\{r\}\'94" for r in top_reviews])\
                    review_block = f"\\n\\n\uc0\u55357 \u56492  **\u48169 \u47928 \u51088  \u47532 \u48624  \u51473  \u51068 \u48512 **\\n\{review_text\}"\
                else:\
                    review_block = ""\
            else:\
                score_text = ""\
                review_block = ""\
                cafe_info = client.chat.completions.create(\
                    model="gpt-3.5-turbo",\
                    messages=[\
                        \{"role": "system", "content": "\uc0\u45817 \u49888 \u51008  \u52397 \u51452  \u51648 \u50669 \u51032  \u44048 \u49457 \u51201 \u51064  \u44288 \u44305  \u44032 \u51060 \u46300 \u51077 \u45768 \u45796 . \u44277 \u49552 \u54616 \u44256  \u46384 \u46907 \u54620  \u47568 \u53804 \u47196  \u51452 \u48320  \u52852 \u54168 \u47484  \u52628 \u52380 \u54616 \u49464 \u50836 ."\},\
                        \{"role": "user", "content": f"\{place\} \uc0\u51452 \u48320 \u50640  \u50612 \u50872 \u47532 \u45716  \u52852 \u54168 \u47484  2~3\u44275  \u52628 \u52380 \u54644  \u51452 \u49464 \u50836 . \u51060 \u47492 , \u48516 \u50948 \u44592 , \u50612 \u46500  \u49324 \u46988 \u50640 \u44172  \u51096  \u50612 \u50872 \u47532 \u45716 \u51648  \u46321 \u51012  \u44048 \u49457 \u51201 \u51004 \u47196  \u49444 \u47749 \u54644  \u51452 \u49464 \u50836 . \u51060 \u47784 \u51648 \u50752  \u51460 \u48148 \u45000 \u46020  \u49324 \u50857 \u54644  \u51452 \u49464 \u50836 ."\}\
                    ]\
                ).choices[0].message.content\
\
            full_block = f"---\\n\\n<h2 style='font-size: 24px; font-weight: bold;'>\uc0\u55356 \u57307 \u65039  \{place\}</h2>\{score_text\}\\n\\n\{gpt_place_response\}\{review_block\}\\n\\n\{cafe_info\}"\
            response_blocks.append(full_block)\
\
        final_response = "\\n\\n".join(response_blocks)\
        st.session_state.messages.append(\{"role": "assistant", "content": final_response\})}