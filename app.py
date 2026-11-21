import base64
import random
import streamlit as st

# 1. 웹앱 기본 설정
st.set_page_config(page_title="가위바위보 게임 (3판 2선승제)", page_icon="🎮")

# 목표 승수 설정 (3판 2선승제 = 먼저 2승 달성 시 최종 승리)
# ※ 만약 '3승 선승제'로 바꾸고 싶다면 아래 숫자를 3으로 수정하세요!
TARGET_WINS = 2


# 밈 스타일 그림 생성 함수 (외부 링크 깨짐 없이 바로 작동하는 밈 카드)
def create_meme_card(bg_color, border_color, emoji, top_text, bottom_text):
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="420" height="250" viewBox="0 0 420 250">
        <rect width="420" height="250" rx="18" fill="{bg_color}" stroke="{border_color}" stroke-width="6"/>
        <text x="210" y="48" font-family="sans-serif" font-size="24" font-weight="900" fill="#111111" text-anchor="middle">{top_text}</text>
        <text x="210" y="150" font-size="85" text-anchor="middle">{emoji}</text>
        <text x="210" y="218" font-family="sans-serif" font-size="21" font-weight="800" fill="#222222" text-anchor="middle">{bottom_text}</text>
    </svg>
    """
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{b64}"


# 이겼을 때 & 졌을 때 무작위로 보여줄 밈 그림 리스트
WIN_MEMES = [
    create_meme_card(
        "#E8F8F5", "#1ABC9C", "😎", "폼 미쳤다!!", "이것이 바로 승자의 여유"
    ),
    create_meme_card(
        "#FEF9E7", "#F1C40F", "🥳", "AI 정복 완료!", "컴퓨터 녀석, 한 수 배웠나?"
    ),
    create_meme_card(
        "#EBF5FB", "#3498DB", "🔥", "완벽한 심리전!", "내 머리 꼭대기 위엔 아무도 없지"
    ),
    create_meme_card(
        "#FDEDEC", "#E74C3C", "👑", "운빨도 실력이다!", "오늘 운세 대박 날 징조"
    ),
]

LOSE_MEMES = [
    create_meme_card(
        "#FDEDEC", "#E74C3C", "😭", "억까 멈춰!!", "방금 건 손가락이 미끄러졌음"
    ),
    create_meme_card(
        "#F4ECF7", "#8E44AD", "🤖", "어림도 없지! 컷!", "인간 시대의 끝이 도래했다"
    ),
    create_meme_card(
        "#EAEDED", "#7F8C8D", "💀", "멘탈 바사삭...", "다음 판엔 진짜 봐주지 않는다"
    ),
    create_meme_card(
        "#FEF5E7", "#E67E22", "🫠", "뇌정지 왔습니다", "컴퓨터가 내 마음을 읽었나?"
    ),
]

# 2. 게임 상태(전적 및 진행 상황) 초기화
if "wins" not in st.session_state:
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.ties = 0
    st.session_state.game_over = False
    st.session_state.last_round = None
    st.session_state.show_balloons = False


def reset_game():
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.ties = 0
    st.session_state.game_over = False
    st.session_state.last_round = None
    st.session_state.show_balloons = False


# 상단 제목 및 안내 문구
st.title("🎮 컴퓨터와 대결하는 가위바위보")
st.write(
    f"먼저 **{TARGET_WINS}승**을 거두는 쪽이 최종 승리하는 **3판 2선승제** 대결입니다!"
)

# 3. 실시간 전적판 (승 / 패 / 무승부)
st.subheader("📊 실시간 전적판")
score_col1, score_col2, score_col3 = st.columns(3)
score_col1.metric("🏆 승리", f"{st.session_state.wins} / {TARGET_WINS}승")
score_col2.metric("💀 패배", f"{st.session_state.losses} / {TARGET_WINS}패")
score_col3.metric("🤝 무승부", f"{st.session_state.ties}회")

st.divider()

# 4. 가위, 바위, 보 버튼 3개 나란히 배치
choices = ["✌️ 가위", "✊ 바위", "✋ 보"]
user_choice = None

col1, col2, col3 = st.columns(3)
with col1:
    if st.button(
        "✌️ 가위", use_container_width=True, disabled=st.session_state.game_over
    ):
        user_choice = "✌️ 가위"
with col2:
    if st.button(
        "✊ 바위", use_container_width=True, disabled=st.session_state.game_over
    ):
        user_choice = "✊ 바위"
with col3:
    if st.button(
        "✋ 보", use_container_width=True, disabled=st.session_state.game_over
    ):
        user_choice = "✋ 보"

# 5. 버튼 클릭 시 라운드 진행 및 승패 계산
if user_choice is not None and not st.session_state.game_over:
    computer_choice = random.choice(choices)

    if user_choice == computer_choice:
        st.session_state.ties += 1
        outcome = "tie"
        meme_img = None
    elif (
        (user_choice == "✌️ 가위" and computer_choice == "✋ 보")
        or (user_choice == "✊ 바위" and computer_choice == "✌️ 가위")
        or (user_choice == "✋ 보" and computer_choice == "✊ 바위")
    ):
        st.session_state.wins += 1
        outcome = "win"
        meme_img = random.choice(WIN_MEMES)
        st.session_state.show_balloons = True
    else:
        st.session_state.losses += 1
        outcome = "lose"
        meme_img = random.choice(LOSE_MEMES)

    st.session_state.last_round = {
        "user": user_choice,
        "computer": computer_choice,
        "outcome": outcome,
        "meme": meme_img,
    }

    # 목표 승수 도달 시 게임 종료 처리
    if (
        st.session_state.wins >= TARGET_WINS
        or st.session_state.losses >= TARGET_WINS
    ):
        st.session_state.game_over = True

    st.rerun()

# 6. 현재 라운드 결과 및 밈 그림 출력
if st.session_state.last_round is not None:
    round_data = st.session_state.last_round

    st.subheader("⚔️ 직전 대결 결과")
    view_col1, view_col2 = st.columns(2)
    view_col1.info(f"**나의 선택:** {round_data['user']}")
    view_col2.info(f"**컴퓨터의 선택:** {round_data['computer']}")

    if round_data["outcome"] == "tie":
        st.warning(
            "🤝 **무승부입니다!** 승수가 올라가지 않았습니다. 다시 선택하세요!"
        )
    elif round_data["outcome"] == "win":
        st.success("🎉 **이번 판 승리!** 1승을 추가했습니다!")
        st.image(round_data["meme"], use_container_width=True)
    else:
        st.error("😭 **이번 판 패배...** 컴퓨터가 1승을 가져갔습니다!")
        st.image(round_data["meme"], use_container_width=True)

# 승리 시 풍선 효과 실행 (1회만 재생되도록 초기화)
if st.session_state.show_balloons:
    st.balloons()
    st.session_state.show_balloons = False

# 7. 최종 승패(3판 2선승제) 판정 및 새 게임 버튼
if st.session_state.game_over:
    st.divider()
    if st.session_state.wins >= TARGET_WINS:
        st.success(
            f"🏆 **최종 우승!** {st.session_state.wins}승 {st.session_state.losses}패로 컴퓨터를 완벽히 이겼습니다!"
        )
    else:
        st.error(
            f"💔 **최종 패배...** {st.session_state.wins}승 {st.session_state.losses}패로 컴퓨터에게 패배했습니다."
        )

    if st.button("🔄 새 게임 시작하기", type="primary", use_container_width=True):
        reset_game()
        st.rerun()
