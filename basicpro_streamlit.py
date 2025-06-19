import streamlit as st
import os

st.title("안녕하세요👋")
st.markdown("## 저희는 <span style='color:blue; font-weight:bold;'>부동산플랜</span>🏠📊입니다.", unsafe_allow_html=True)
st.write("### 이 페이지에서 당신은 2018년부터 2024년까지의 서울시 부동산 실거래가 정보를 통해 데이터 기반의 매물 추천을 받으실 수 있습니다.")

name = st.text_input("먼저 이름을 입력하세요:")
if name:
    st.success(f"{name}님, 반가워요!🙌")

