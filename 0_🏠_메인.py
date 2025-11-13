# 파일 이름: 0_🏠_메인.py
import streamlit as st
# [수정] import 방식 변경
from backend.stats_queries import get_summary_stats
from backend.news_api import get_naver_news

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="레몬 스캐너 - 메인", 
    page_icon="🏠", 
    layout="wide"
)

# --- [1] 제목 ---
st.title("🍋 레몬 스캐너 (Lemon Scanner)")
st.subheader("자동차 리콜 현황 분석 및 비교 대시보드")
st.markdown("---")

# --- [2] 상단 요약 영역 (대시보드) ---
try:
    summary_stats = get_summary_stats() # 함수 직접 호출
    brand_name, brand_count = summary_stats['most_recall_brand']
    min_date, max_date = summary_stats['data_period']
    
    st.markdown("### 📊 리콜 현황 요약") 
    
    cols = st.columns(4)
    cols[0].metric("총 리콜 건수", f"{summary_stats['total_recalls']:,} 건")
    cols[1].metric("리콜 대상 브랜드 수", f"{summary_stats['total_brands']:,} 개")
    cols[2].metric("리콜 대상 총 차종 수", f"{summary_stats['total_models']:,} 종")
    cols[3].metric("최다 리콜 브랜드", brand_name, f"{brand_count:,} 건")
    if min_date != 'N/A':
        st.caption(f"ℹ️ (데이터 기준 기간: {min_date} ~ {max_date})")
except Exception as e:
    st.error(f"요약 통계 로딩 실패: {e}")
st.markdown("---")


# --- [3] (신규) 최신 리콜 뉴스 (메인으로 이동) ---
st.header("📰 최신 리콜 뉴스")

# --- [★ 수정된 부분] ---
# (Naver API 출처를 명시하고, Naver Developers 페이지로 링크)
st.caption("Powered by [Naver Search API](https://developers.naver.com/products/service-api/search/search.md)")
# ------------------------

try:
    news_list = get_naver_news("자동차 리콜")
    for news in news_list:
        st.markdown(f"**[{news['title']}]({news['link']})**")
        st.caption(f"{news['description'][:100]}...") # 메인 화면이므로 100자까지 표시
        st.divider() # 각 뉴스 항목 사이에 구분선
except Exception as e:
    st.error(f"뉴스 로딩 실패: {e}")
st.markdown("---")


# --- [4] (신규) 리콜 정보 & 꿀팁 (요청하신 순서대로) ---

# [4-1] 리콜 절차 & 꿀팁 (텍스트 요약)
st.header("💡 리콜 절차 & 꿀팁")
st.markdown(
    """
    **1. 리콜 대상 확인 방법**
    - [자동차리콜센터(car.go.kr)](https://www.car.go.kr/ri/ntcn/list.do) 공식 사이트 접속
    - 차량번호 또는 차대번호(VIN) 17자리 입력
    - 본인 차량의 리콜 대상 여부 즉시 확인
    
    **2. 리콜 절차**
    - **(통지)** 차량 제조사로부터 리콜 통지서(우편, 문자 등) 수신
    - **(예약)** 해당 차량 제조사의 공식 서비스센터에 정비 예약
    - **(조치)** 예약된 날짜에 방문하여 **무상**으로 점검 및 수리 진행
    
    **3. 리콜 vs 무상수리 차이점**
    - **리콜 (강제/자발적)**: 안전 운행에 **중대한 지장**을 주는 결함 (예: 화재, 시동 꺼짐, 브레이크). 법적 의무이며 시정 기간(1년 6개월)이 정해져 있음.
    - **무상수리**: 안전과 **직접 관련 없는** 결함 (예: 소음, 부품 내구성). 제조사가 고객 만족을 위해 자발적으로 제공.
    """
)
st.markdown("---")

# [4-2] 관련 사이트 링크 (가로 3단 카드)
st.header("🔗 관련 사이트 링크")

tip_col1, tip_col2, tip_col3 = st.columns(3)

with tip_col1:
    # 카드 1: 공식 리콜센터
    with st.container(border=True):
        st.subheader("1. 자동차리콜센터 (공식)")
        st.markdown("내 차의 리콜 대상 여부를 차량번호로 즉시 조회할 수 있는 **공식 사이트**입니다.")
        st.link_button(
            "리콜센터 바로가기", 
            "https://www.car.go.kr/ri/ntcn/list.do", 
            use_container_width=True
        )

with tip_col2:
    # 카드 2: 리콜 절차 가이드
    with st.container(border=True):
        st.subheader("2. 리콜 절차 가이드")
        st.markdown("리콜 대상 확인부터 신청, 수리 절차까지 전 과정을 알기 쉽게 설명한 가이드입니다.")
        st.link_button(
            "절차 가이드 보기 (pro.re.kr)", 
            "https://pro.re.kr/자동차-리콜-대상-확인-방법과-신청-절차-완벽-가이드/", 
            use_container_width=True
        )
        
with tip_col3:
    # 카드 3: 리콜 vs 무상수리
    with st.container(border=True):
        st.subheader("3. 리콜 vs 무상수리")
        st.markdown("리콜과 무상수리의 법적 차이점이 무엇인지 알기 쉽게 설명한 블로그 포스트입니다.")
        st.link_button(
            "차이점 알아보기 (Naver)", 
            "https://blog.naver.com/llllll0987/222384380892", 
            use_container_width=True
        )


# --- [5] 사이드바 설정 (볼드체 수정) ---
st.sidebar.title("환영합니다!")
st.sidebar.markdown(
    """
    **🍋레몬 스캐너**에 오신 것을 환영합니다.
    
    왼쪽 메뉴에서 원하는 페이지를 선택하세요.
    """
) 

# --- [6] (삭제) 사이드바 하단 뉴스 ---
# (뉴스 기능이 메인 페이지로 이동되어 삭제되었습니다.)