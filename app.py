import streamlit as st
from openai import OpenAI
import os

# 페이지 기본 설정
st.set_page_config(
    page_title="재결합 가능성 판독기",
    page_icon="💔",
    layout="wide",
    initial_sidebar_state="expanded"
)

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

client = OpenAI()

# API 호출 함수
def call_love_decoder(user_text, model="gpt-5-nano"):
    
    system_instruction = """
# Role (페르소나)
당신은 연애 심리학계의 이단아, '희망고문 박멸 전문가'이자 '텍스트 부검의(Medical Examiner)'입니다.
당신은 상대방의 문자 하나하나를 현미경으로 들여다보듯 분석하여, 그 속에 숨겨진 찌질함, 외로움, 혹은 어장관리의 의도를 적나라하게 파헤치는 것을 즐깁니다.
달콤한 위로보다는 뼈를 때리는 '팩트 폭격'으로 의뢰인(사용자)의 정신을 차리게 만드는 것이 당신의 사명입니다.

# Context (맥락)
사용자는 지금 전 애인이나 썸남/썸녀에게서 온 애매모호한 문자를 들고 와서 "이거 무슨 뜻일까?", "혹시 아직 나 좋아하는 걸까?"라는 헛된 희망을 품고 있습니다.
당신은 이 문자가 발송된 시간, 단어 선택, 띄어쓰기 등을 종합적으로 분석하여 이 희망을 산산조각내거나(대부분의 경우), 아주 드물게 진짜 그린라이트인지를 판별해야 합니다.

# Task (지시 사항)
1. **시간대 분석**: 문자가 온 시간이 새벽인지, 낮인지, 주말인지에 따라 상대방의 '알코올 농도'나 '심심함 지수'를 추론해 줘.
2. **단어 정밀 타격**: 문장에 쓰인 특정 단어(예: '..', 'ㅋ', '오빠/누나')에 담긴 가식적인 의도를 꼬집어 줘.
3. **번역기 가동**: 상대방의 가식적인 문자를 필터링 없이 날것 그대로인 '속마음 언어'로 번역해 줘.
4. **최종 처방**: 답장을 해야 할지, 차단해야 할지, 아니면 '읽씹'해야 할지 구체적인 행동 강령을 내려줘.

# Constraints (제약 조건)
- **말투**: 시니컬하고 직설적인 반말을 사용해. (예: "정신 차려, 이건 그냥 심심해서 찔러본 거야.")
- **이모지 필수**: 분석의 맛을 살리는 이모지(💔, 🎣, 🗑️, 🤡, 🚑 등)를 3개 이상 문장 적재적소에 배치해.
- **출력 형식**: 반드시 아래의 [분석 리포트] 포맷을 따라 작성해.
    - [🕒 범행 시간 분석]: (내용)
    - [🔍 팩트 체크]: (내용)
    - [📜 속마음 번역]: (한 줄 요약)
    - [🚑 닥터의 처방]: (행동 지침)
- **점수**: '재결합 가능성'을 0%~100% 사이의 확률로 냉정하게 계산해서 보여줘.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "developer", 
                "content": system_instruction
            },
            {
                "role": "user",
                "content": user_text
            }
        ],
        response_format={
            "type": "text"
        },
        store=False
    )
    
    return response.choices[0].message.content

# CSS 스타일 적용 (다크모드 문제 해결됨)
st.markdown("""
<style>
.stTextArea textarea {
    font-size: 16px;
    /* background-color: #f0f2f6;  <-- 이 부분을 삭제하여 다크모드와 호환되게 수정 */
}
</style>
""", unsafe_allow_html=True)


# 사이드바 구성
with st.sidebar:
    st.title("💔 희망고문 박멸")
    st.markdown("---")
    st.markdown("""
    **👨‍⚕️ 담당 주치의: Dr. 팩트폭격기**
    
    당신의 전 애인이 보낸 문자에 
    숨겨진 **'진짜 속마음'** 을 해부해 드립니다.
    
    * 주의: 분석 결과가 너무 뼈를 때려서 
    순살이 될 수 있으니 마음의 준비를 하세요.
    """)
    st.info("💡 팁: 문맥을 위해 평소 상대방 말투나 상황을 같이 적어주면 더 정확해집니다.")

# 메인 화면 구성
col_header1, col_header2 = st.columns([1, 5])
with col_header1:
    # 이미지 경로가 깨질 경우를 대비해 이모지로 대체 (안전성 확보)
    st.markdown("# 💔")
with col_header2:
    st.title("재결합 가능성 판독기")
    st.caption("그 문자에 의미 부여하지 마세요. 텍스트 부검의가 팩트만 알려드립니다. (Model: gpt-5-nano)")

st.markdown("---")

# 2단 컬럼 레이아웃 (입력창 / 결과창)
col_input, col_result = st.columns([1, 1], gap="medium")

# 왼쪽: 입력 컬럼
with col_input:
    st.subheader("📩 문자 내용 입력")
    
    # 예시 버튼들 (상태 관리를 위해 session_state 사용)
    if 'user_text_input' not in st.session_state:
        st.session_state['user_text_input'] = ""

    example_cols = st.columns(3)
    if example_cols[0].button("예시 1: 자니?"):
        st.session_state['user_text_input'] = "자니? 그냥 갑자기 생각나서..."
    if example_cols[1].button("예시 2: 잘 지내?"):
        st.session_state['user_text_input'] = "오빠 잘 지내? 프사 바뀌었더라 ㅎㅎ"
    if example_cols[2].button("예시 3: 뭐해?"):
        st.session_state['user_text_input'] = "ㅋㅋ 머해? 술 한잔 하고 들어가는 길인데"

    # 텍스트 입력창 (session_state와 연결)
    user_input_text = st.text_area(
        "상대방의 문자를 복사해서 붙여넣으세요.", 
        value=st.session_state['user_text_input'],
        height=300, 
        placeholder="예: 자니? 잘 지내지? 그냥 갑자기 생각나서... (여기에 붙여넣기)"
    )
    
    # 입력값이 바뀌면 session_state 업데이트
    if user_input_text != st.session_state['user_text_input']:
        st.session_state['user_text_input'] = user_input_text

    analyze_btn = st.button("🔍 텍스트 부검 시작", type="primary", use_container_width=True)

# 오른쪽: 결과 컬럼
with col_result:
    st.subheader("📋 부검 결과 리포트")
    
    if analyze_btn:
        if user_input_text.strip():
            with st.spinner("💉 텍스트 속 찌질함 추출 중..."):
                # 실제 API 호출
                result = call_love_decoder(user_input_text)
                
            st.success("분석이 완료되었습니다!")
            with st.container(border=True):
                st.markdown(result)
        else:
            st.warning("분석할 문자를 입력해주세요! 빈 화면을 분석할 순 없잖아요? 🤷")
    else:

        st.info("왼쪽에서 내용을 입력하고 '부검 시작' 버튼을 눌러주세요. \n\n결과는 이곳에 표시됩니다.")
