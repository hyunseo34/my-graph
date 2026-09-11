import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    layout="wide",
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("---")


# 데이터 로드 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)

    # 날짜 열을 YYYYMMDD 형식을 고려하여 datetime 객체로 변환
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str), format="%Y%m%d")

    return df


df = load_data()

# -------------------------------------------------------------------
# 구역 1: 영화별 일관객 변화
# -------------------------------------------------------------------
st.header("1. 영화별 일관객 변화 추이")

# 영화 목록 추출 (관객수 기준 정렬 또는 가나다 순)
movie_list = sorted(df["영화명"].unique())

# 영화 선택 드롭다운
selected_movie = st.selectbox(
    "조회할 영화를 선택하세요:",
    options=movie_list,
    index=0,
)

# 선택된 영화의 데이터 필터링
movie_df = df[df["영화명"] == selected_movie].sort_values("날짜")

# Plotly 선 그래프 생성
fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    title=f"[{selected_movie}] 날짜별 일관객 수 변화",
    labels={"날짜": "날짜", "일관객": "일관객 수(명)"},
    markers=True,
)

# 마우스 오버(Hover) 툴팁 상세 설정
fig1.update_traces(
    hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객 수:</b> %{y:,}명<extra></extra>"
)

fig1.update_layout(hovermode="x unified")

# Streamlit에 그래프 출력
st.plotly_chart(fig1, use_container_width=True)

# 인사이트 기록란
st.info("💡 **이 그래프로 알 수 있는 것:** 여기에 작성할 내용을 입력하세요.")

st.markdown("---")

# -------------------------------------------------------------------
# 구역 2: (추가 예정 구역 예시)
# -------------------------------------------------------------------
# st.header("2. 다음 분석 주제")
# ... 추후 그래프 및 인사이트 추가 ...
