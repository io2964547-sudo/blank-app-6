import streamlit as st
import random
from supabase import create_client

# ======================
# Supabase 設定
# ======================
SUPABASE_URL = "https://vnwmogrefmcgpjdgtirr.supabase.co"
SUPABASE_KEY = "sb_publishable_dMkyQWbS2SZ7uWl2ufkHNQ_NsiXhWCp"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ======================
# アプリ設定
# ======================
st.set_page_config(page_title="ラッキー音楽占い", page_icon="🔮")
st.title("🔮 今日のあなた、だいたいこんな感じ")
st.write("占った結果は記録として保存されます。")

name = st.text_input("あなたの名前")

# ======================
# 占いデータ
# ======================
data = {
    "fortune": ["大吉", "中吉", "小吉", "吉", "凶", "大凶"],
    "comment": [
        "今日は何もしなくてもOKな日。",
        "無理しないのが一番えらい。",
        "思ったよりちゃんとやれてる。",
        "変な選択肢を選ぶと逆にうまくいく。",
        "とりあえず寝ると解決する。",
        "なぜか笑われる日。悪い意味ではない。"
    ],
    "music": [
        ("YOASOBI / アイドル", "https://www.youtube.com/watch?v=ZRtdQ81jPUQ"),
        ("Vaundy / 怪獣の花唄", "https://www.youtube.com/watch?v=UM9XNpgrqVk"),
        ("初音ミク / 千本桜", "https://www.youtube.com/watch?v=shs0rAiwsGQ"),
        ("DECO*27 / ゴーストルール", "https://www.youtube.com/watch?v=KushW6zvazM"),
        ("wowaka / ローリンガール", "https://www.youtube.com/watch?v=NIqm73xsias"),
    ]
}

# ======================
# 占う処理
# ======================
if st.button("占ってもらう"):
    if not name:
        st.warning("名前を入力してください")
    else:
        fortune = random.choice(data["fortune"])
        comment = random.choice(data["comment"])
        music_title, music_url = random.choice(data["music"])

        # 結果表示
        st.subheader(f"🌟 {name} さんの今日の運勢")
        st.markdown(f"## **{fortune}**")
        st.write(comment)

        st.markdown("---")
        st.subheader("🎵 本日のラッキー音楽")
        st.write(f"🎧 **{music_title}**")
        st.video(music_url)

        # ======================
        # Supabase に保存
        # ======================
        supabase.table("fortune_logs").insert({
            "user_name": name,
            "fortune": fortune,
            "music_title": music_title
        }).execute()

        st.success("結果をデータベースに保存しました！")

# ======================
# 履歴表示
# ======================
st.markdown("---")
st.subheader("📜 過去の占い履歴")

logs = (
    supabase
    .table("fortune_logs")
    .select("*")
    .order("created_at", desc=True)
    .limit(10)
    .execute()
    .data
)

if logs:
    for log in logs:
        st.write(
            f"🕒 {log['created_at']} | "
            f"{log['user_name']} | "
            f"{log['fortune']} | "
            f"{log['music_title']}"
        )
else:
    st.write("まだ履歴がありません。")
