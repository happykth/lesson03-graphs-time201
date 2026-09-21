import pandas as pd
import plotly.express as px
import streamlit as st

# ─────────────────────────────────────────────
# 기본 설정
# ─────────────────────────────────────────────
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
WARM_COLOR = "#E4572E"  # 따뜻한 주황빛 붉은색

st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", page_icon="🎬", layout="wide")

# 그래프마다 아래에 보여줄 '이 그래프로 알 수 있는 것' 한 문장
# 새 그래프를 추가하면 여기에 키를 하나 더 만들고 문장을 적으면 됩니다.
INSIGHTS = {
    "graph1": "",  # 예: "개봉 직후 관객이 가장 많고, 이후 서서히 줄어든다."
    "graph2": "",
}


def show_insight(key: str):
    """그래프 아래에 '이 그래프로 알 수 있는 것' 한 문장을 보여주는 자리."""
    text = INSIGHTS.get(key, "").strip()
    if text:
        st.info(f"💡 **이 그래프로 알 수 있는 것** · {text}")
    else:
        st.info("💡 **이 그래프로 알 수 있는 것** · (여기에 한 문장을 적어 주세요)")


# ─────────────────────────────────────────────
# 데이터 불러오기
# ─────────────────────────────────────────────
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_URL)
    # 하이픈 없는 8자리 숫자(예: 20240101) → 진짜 날짜
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str), format="%Y%m%d")
    return df


df = load_data()

# ─────────────────────────────────────────────
# 제목
# ─────────────────────────────────────────────
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.caption("1년치 일별 박스오피스 10위권 기록으로 그려 보는 그래프 모음")

# ═════════════════════════════════════════════
# 구역 1. 영화 한 편의 흐름
# ═════════════════════════════════════════════
st.header("1. 영화 한 편의 날짜별 관객 변화")

# 기간 내 관객이 많았던 영화가 목록 앞쪽에 오도록 정렬
movie_order = (
    df.groupby("영화명")["일관객"].sum().sort_values(ascending=False).index.tolist()
)
movie = st.selectbox("영화를 골라 보세요", movie_order)

movie_df = df[df["영화명"] == movie].sort_values("날짜")

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    color_discrete_sequence=[WARM_COLOR],
)
fig1.update_traces(
    hovertemplate="%{x|%Y-%m-%d}<br>일관객 %{y:,}명<extra></extra>"
)
fig1.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객(명)",
    yaxis_tickformat=",",
    hovermode="x unified",
    margin=dict(l=10, r=10, t=30, b=10),
)
st.plotly_chart(fig1, use_container_width=True)
show_insight("graph1")

# ═════════════════════════════════════════════
# 구역 2. 관객 합계 TOP 5 영화 비교
# ═════════════════════════════════════════════
st.divider()
st.header("2. 관객 합계 TOP 5 영화의 날짜별 관객 비교")
st.caption("범례의 영화 이름을 누르면 그 선을 켜고 끌 수 있어요.")

top5 = movie_order[:5]  # 기간 내 일관객 합계가 큰 순서
top5_df = df[df["영화명"].isin(top5)].sort_values(["영화명", "날짜"])

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    category_orders={"영화명": top5},  # 범례를 합계 순서대로
    color_discrete_sequence=["#E4572E", "#F3A712", "#A8201A", "#6B8F71", "#8C5E58"],
)
fig2.update_traces(
    hovertemplate="%{x|%Y-%m-%d}<br>일관객 %{y:,}명<extra>%{fullData.name}</extra>"
)
fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객(명)",
    yaxis_tickformat=",",
    legend_title_text="영화 (클릭해서 켜고 끄기)",
    margin=dict(l=10, r=10, t=30, b=10),
)
st.plotly_chart(fig2, use_container_width=True)
show_insight("graph2")

# ═════════════════════════════════════════════
# 구역 3. (다음 그래프가 들어갈 자리)
# ═════════════════════════════════════════════
# st.divider()
# st.header("3. 제목")
# ... 그래프 코드 ...
# show_insight("graph3")
