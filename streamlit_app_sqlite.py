import streamlit as st
import random
import sqlite3
from datetime import datetime, timezone

# ======================
# SQLite3 設定
# ======================
DB_FILE = "fortune.db"

# データベースとテーブルを初期化
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS fortune_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    fortune TEXT NOT NULL,
    music_title TEXT NOT NULL,
    created_at TEXT NOT NULL
)
""")

conn.commit()
conn.close()

# ======================
# アプリ設定
# ======================
st.set_page_config(page_title="ラッキー音楽占い", page_icon="🔮")
st.title("🔮 今日のあなた、だいたいこんな感じ")
st.write("占った結果は記録として保存されます。")

name = st.text_input("あなたの名前")
created_at = datetime.now(timezone.utc).isoformat()

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
        # SQLite3 に保存
        # ======================
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO fortune_logs
            (user_name, fortune, music_title, created_at)
            VALUES (?, ?, ?, ?)
        """, (name, fortune, music_title, created_at))

        conn.commit()
        conn.close()

        st.success("結果をデータベースに保存しました！")

# ======================
# 履歴表示
# ======================
st.markdown("---")
st.subheader("📜 過去の占い履歴")

conn = sqlite3.connect(DB_FILE)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("""
    SELECT user_name, fortune, music_title, created_at
    FROM fortune_logs
    ORDER BY created_at DESC
    LIMIT 10
""")

logs = cursor.fetchall()
conn.close()

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
