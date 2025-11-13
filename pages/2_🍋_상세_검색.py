# 파일 이름: 2_🍋_상세_검색.py
import streamlit as st
import pandas as pd
import datetime       
# [수정] import 방식 변경 (news_api 임포트 제거)
from backend.search_queries import get_all_keywords_with_desc, get_all_brands, get_models_by_brand, search_recalls
from backend.stats_queries import get_summary_stats
# from backend.news_api import get_naver_news # <-- 삭제

# --- [0] 페이지 기본 설정 ---
st.set_page_config(
    page_title="레몬 스캐너 - 상세 검색",
    page_icon="🍋", 
    layout="wide"
)

# --- [1] 키워드 설명 DB에서 로드 ---
try:
    KEYWORD_DICT_FROM_DB = get_all_keywords_with_desc()
except Exception as e:
    st.error(f"키워드 목록 로딩 중 DB 오류 발생: {e}")
    KEYWORD_DICT_FROM_DB = {}

# --- [2] 제목 ---
st.title("🍋 상세 검색") 
st.markdown("---")

# --- [3] 사이드바 (필터 영역) ---
st.sidebar.header("🔍 상세 검색 필터")
try:
    brand_list = ["전체"] + get_all_brands()
except Exception as e:
    st.sidebar.error(f"브랜드 목록 로딩 실패: {e}")
    brand_list = ["전체"]
selected_brand = st.sidebar.selectbox(
    "1. 브랜드 선택", brand_list, key="tab1_brand", 
    help="브랜드를 선택하면 하단 '차종' 목록이 업데이트됩니다."
)
if selected_brand != "전체":
    try:
        model_list = ["전체"] + get_models_by_brand(selected_brand)
    except Exception as e:
        st.sidebar.error(f"차종 목록 로딩 실패: {e}")
        model_list = ["전체"]
else:
    model_list = ["전체"] 
current_year = datetime.date.today().year
year_list = ["전체"] + list(range(current_year, 2014, -1))
keyword_list = ["전체"] + list(KEYWORD_DICT_FROM_DB.keys())
with st.sidebar.form(key="search_form"):
    selected_model = st.selectbox("2. 차종 선택", model_list, key="tab1_model")
    selected_year = st.selectbox("3. 리콜연도 선택 (리콜개시일 기준)", year_list, key="tab1_year")
    selected_keyword = st.selectbox(
        "4. 리콜사유 키워드 선택", keyword_list, key="tab1_keyword",
        help="리콜 사유에 포함된 핵심 키워드를 선택합니다." 
    )
    if selected_keyword and selected_keyword != "전체":
        description = KEYWORD_DICT_FROM_DB.get(selected_keyword, "상세 설명이 없습니다.")
        st.caption(f"ℹ️ **{selected_keyword}**: {description}")
    submit_pressed = st.form_submit_button(label="상세 리콜 내역 검색")

# --- [4] 메인 화면 (결과 표시) ---
if submit_pressed:
    filter_summary = f"**검색 조건:** [브랜드: {selected_brand}] [차종: {selected_model}] [연도: {selected_year}] [키워드: {selected_keyword}]"
    st.info(filter_summary)
    with st.spinner("데이터베이스에서 리콜 정보를 검색 중입니다..."):
        results_df = search_recalls(
            selected_brand, selected_model, selected_year, selected_keyword
        )
    if results_df.empty:
        st.warning("선택하신 조건에 맞는 리콜 정보를 찾을 수 없습니다.")
    else:
        st.success(f"총 {len(results_df)}건의 리콜 정보를 찾았습니다. (최대 200건)")
        columns_to_show = [
            '브랜드', '차종', '리콜개시일', '생산시작', '생산종료', 
            '리콜대수', '시정대수', '시정률(%)', '리콜사유'
        ]
        available_columns = [col for col in columns_to_show if col in results_df.columns]
        st.dataframe(
            results_df[available_columns], use_container_width=True, height=600,
            column_config={"리콜사유": st.column_config.TextColumn("리콜사유", width="large")}
        )
else:
    st.info("왼쪽 사이드바에서 검색 조건을 선택한 후 검색 버튼을 눌러주세요.")

# --- [5] 데이터 기준 기간 표시 ---
try:
    summary_stats = get_summary_stats()
    min_date, max_date = summary_stats['data_period']
    st.markdown("---")
    if min_date != 'N/A':
        st.caption(f"ℹ️ (데이터 기준 기간: {min_date} ~ {max_date})")
except Exception:
    pass

# --- [6] (삭제) 사이드바 하단 뉴스 ---
# (뉴스 기능이 메인 페이지로 이동되어 삭제)