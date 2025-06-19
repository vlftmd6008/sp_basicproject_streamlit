import streamlit as st
import os

st.title("안녕하세요👋")
st.markdown("## 저희는 <span style='color:blue; font-weight:bold;'>부동산플랜</span>😈입니다.", unsafe_allow_html=True)
st.write("### 이 페이지에서 당신은 2018년부터 2024년까지의 서울시 부동산 실거래가 정보를 통해 데이터 기반의 매물 추천🏠📊을 받으실 수 있습니다.")

name = st.text_input("먼저 이름을 입력하세요", value='김바다')
if name:
    st.success(f"{name}님, 반가워요!🙌")
st.write("저희에겐 2018년부터 2024년까지의 서울시 부동산 실거래가 정보가 주어져있습니다. \
같은 주소의 매물이 시간에 따라 거래된 가격을 기준으로, 모든 거래를 2024년 수준의 가격으로 환산하겠습니다. \
이 작업은 부동산 가격의 시간에 따른 변화율을 활용하여 가격을 보정하는 작업입니다. \
가격 보정의 전체 흐름을 요약해드리자면")
st.write("""#### ✅ 전체 흐름 요약
1. 같은 건물 용도(컬럼명: BLDG_USG, 예: 아파트, 오피스텔 등)별로 연도별 평균 거래금액을 구함
2. 연도별 상승률을 계산 (예: 2020→2021 가격 변화율 등)
3. 각 연도별 거래건에 대해 누적 상승률을 계산해서 2024년 가격으로 보정
4. 모든 거래 데이터에 보정된 가격(컬럼명: THING_AMT_2024) 추가""")

st.write("또한, 방 개수와 신축 여부의 기준을 알려드리겠습니다.")
st.write("""#### 🏠 방 개수 구하기_건축 면적(컬럼명: ARCH_AREA) 기준
- 30㎡ 이하 **→** 방 1개
- 30㎡ 초과 ~ 70㎡ 이하 **→** 방 2개
- 70㎡ 초과 ~ 100㎡ 이하 **→** 방 3개
- 100㎡ 초과 **→** 방 4개 이상
#### 🆕 신축 여부 구하기_건축 연도(컬럼명: ARCH_YR) 기준
- 2019년부터 2024년까지에 지어진 건물 **→** 신축
- 그 외 **→** 구축""")

st.write(f"이제 {name}님이 원하시는 매물 가격, 방 개수, 건물 종류, 신축 여부를 선택해주세요.")
y = st.number_input("💰예산을 숫자로 선택해주세요 (예: 400000000)", value=400000000, step = 100000000)
rooms = st.number_input("🔢방 개수를 숫자로 선택해주세요 (예: 2, 3)", value=3)
usg = st.selectbox("🏘️건물 종류를 선택해주세요",
    ['아파트', '연립다세대', '단독다가구', '오피스텔'],
    index=0)
new_old = st.selectbox("🆕신축 여부를 선택해주세요",
    ['신축', '구축'],
    index=0)

import pandas as pd

# 사용자 정의 컬럼 이름 및 데이터 타입
COLUMN_NAMES = [
    'RCPT_YR', 'CGG_CD', 'CGG_NM', 'STDG_CD', 'STDG_NM', 
    'LOTNO_SE', 'LOTNO_SE_NM', 'MNO', 'SNO', 'BLDG_NM', 
    'CTRT_DAY', 'THING_AMT', 'ARCH_AREA', 'LAND_AREA', 'FLR', 
    'RGHT_SE', 'RTRCN_DAY', 'ARCH_YR', 'BLDG_USG', 'DCLR_SE', 
    'OPBIZ_RESTAGNT_SGG_NM'
]

DTYPE_DICT = {
    'RCPT_YR': 'int64',
    'CGG_CD': 'string',
    'CGG_NM': 'string',
    'STDG_CD': 'string',
    'STDG_NM': 'string',
    'LOTNO_SE': 'string',
    'LOTNO_SE_NM': 'string',
    'MNO': 'string',
    'SNO': 'string',
    'BLDG_NM': 'string',
    'CTRT_DAY': 'string',
    'THING_AMT': 'int64',
    'ARCH_AREA': 'float64',
    'LAND_AREA': 'float64',
    'FLR': 'string', 
    'RGHT_SE': 'string',
    'RTRCN_DAY': 'string', 
    'ARCH_YR': 'string', 
    'BLDG_USG': 'string',
    'DCLR_SE': 'string',
    'OPBIZ_RESTAGNT_SGG_NM': 'string'
}

@st.cache_data(show_spinner=True)
def load_real_estate_data(years=range(2018, 2025)):
    dfs = []
    for y in years:
        file = f"{y}.csv"
        try:
            df = pd.read_csv(
                file,
                encoding='euc-kr',
                names=COLUMN_NAMES,
                dtype=DTYPE_DICT,
                skiprows=1
            )
            dfs.append(df)
        except FileNotFoundError:
            st.warning(f"{file} 파일이 없습니다.")
    if dfs:
        real_estate_df = pd.concat(dfs, ignore_index=True)
        return real_estate_df
    else:
        return pd.DataFrame(columns=COLUMN_NAMES)

# Streamlit 앱 시작
def main():
    st.title("부동산 데이터 분석")

    real_estate = load_real_estate_data()

    st.write("데이터 샘플")
    st.dataframe(real_estate.head())

    # 추가 필터링, 분석 UI 및 로직을 여기 추가 가능

if __name__ == "__main__":
    main()





if __name__ == "__main__":
    st.write("다음은 선택하신 기준에 맞는 매물들을 필터링한 결과입니다.")
