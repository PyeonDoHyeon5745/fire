# 📊 분석 시각화 자료 제목
st.markdown("---")
st.markdown("### 📊 분석 시각화 자료")

# 👉 컬럼 두 개로 나누기
col1, col2 = st.columns([1, 1])

# 📊 피처 중요도 시각화 (왼쪽 컬럼)
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

# 📊 서울 재화재 예측 분포 (오른쪽 컬럼)
with col2:
    st.markdown("### 🔥 서울 재화재 예측 분포 🔥")

    # 데이터 로딩
    df_seoul = pd.read_csv("seoul_fire_predict.csv")
    df_seoul['위험도_혼합'] = df_seoul['위험도_혼합'].astype(str).str.extract(r'(\d+\.\d+|\d+)')[0]
    df_seoul['위험도_혼합'] = pd.to_numeric(df_seoul['위험도_혼합'], errors='coerce')
    df_seoul = df_seoul[df_seoul['위험도_혼합'].notnull()]

    # KDE 추정
    sns.set_theme(style="white")
    ax = sns.kdeplot(df_seoul[df_seoul['RLPS_YN'] == 1]['위험도_혼합'], bw_adjust=1)
    x1, y1 = ax.lines[0].get_data()
    plt.close()

    ax = sns.kdeplot(df_seoul[df_seoul['RLPS_YN'] == 0]['위험도_혼합'], bw_adjust=1)
    x2, y2 = ax.lines[0].get_data()
    plt.close()

    # Plotly 그래프
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
        xaxis_title='재화재 점수',
        yaxis_title='밀도',
        legend_title='재발생 여부',
        template='plotly_white',
        height=600,
        margin=dict(t=40, b=40, l=40, r=10)
    )

    st.plotly_chart(fig_density, use_container_width=True)

