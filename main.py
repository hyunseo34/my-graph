import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

# 데이터 로드 함수 (캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # 컬럼 이름 지정 (날짜, 순위, 영화코드, 영화명, 일관객, 누적관객, 스크린수, 상영횟수)
    # 데이터 구조에 맞게 컬럼명 정리
    df.columns = ["날짜", "순위", "영화코드", "영화명", "일관객", "누적관객", "스크린수", "상영횟수"]
    
    # 날짜 열을 진짜 날짜형(datetime)으로 변환 (YYYYMMDD 형식)
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str), format="%Y%m%d")
    
    # 숫자형 데이터 타입 변환
    numeric_cols = ["순위", "일관객", "누적관객", "스크린수", "상영횟수"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    return df

# 앱 타이틀
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("1년치(365일) 일별 박스오피스 데이터를 바탕으로 시간의 흐름에 따른 영화 흥행 추이를 탐색합니다.")

st.divider()

# 데이터 불러오기
try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# ----------------------------------------------------
# 구역 1: 특정 영화의 날짜별 일관객 변화
# ----------------------------------------------------
st.header("📌 구역 1: 영화별 일관객수 변화 추이")

# 영화 선택 드롭다운 (관객수 합계 기준 상위 순 정렬)
top_movies = df.groupby("영화명")["일관객"].sum().sort_values(ascending=False).index.tolist()
selected_movie = st.selectbox("영화를 선택하세요:", top_movies)

if selected_movie:
    movie_df = df[df["영화명"] == selected_movie].sort_values("날짜")
    
    # Plotly 선 그래프 생성
    fig1 = px.line(
        movie_df,
        x="날짜",
        y="일관객",
        title=f"[{selected_movie}] 날짜별 일관객수 변화",
        labels={"날짜": "날짜", "일관객": "일관객수 (명)"},
        markers=True
    )
    
    # Tooltip 및 스타일 설정
    fig1.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객수:</b> %{y:,}명<extra></extra>",
        line=dict(width=2.5)
    )
    fig1.update_layout(
        hovermode="x unified",
        xaxis_title="날짜",
        yaxis_title="일관객수 (명)",
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    
    # '이 그래프로 알 수 있는 것' 문구 영역
    st.info("💡 **이 그래프로 알 수 있는 것:** *(여기에 해석 문구를 작성하세요)*")

st.divider()

# ----------------------------------------------------
# 구역 2: 추후 그래프 추가 영역 (예시/템플릿)
# ----------------------------------------------------
st.header("📌 구역 2: (추가 예정 그래프)")
st.caption("앞으로 시간 차원과 관련된 다양한 시각화 그래프가 이 구역에 추가될 예정입니다.")

# 추가 그래프를 위한 플레이스홀더 예시
# st.plotly_chart(fig2, use_container_width=True)
st.info("💡 **이 그래프로 알 수 있는 것:** *(여기에 해석 문구를 작성하세요)*")

st.divider()
