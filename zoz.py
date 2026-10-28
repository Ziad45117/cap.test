import csv
import os
from datetime import datetime

import streamlit as st
import requests
import streamlit as st

if "name" not in st.session_state:
    st.session_state.name = ""

if not st.session_state.name:
    name = st.text_input("اكتب اسمك عشان نبدأ:")
    if st.button("ابدأ") and name.strip():
        st.session_state.name = name.strip()
        st.rerun()
    st.stop()

SCRIPT_URL = "/d/1CRk28pE3n8uZDKxbeGl6uAkFLGmKFY8f1d78PbcyukI/edit"

def save_answer(name, answer):
    try:
        requests.post(SCRIPT_URL, json={"name": name, "answer": answer}, timeout=10)
    except requests.RequestException as e:
        print("مشكلة في الحفظ على الشيت:", e)
st.set_page_config(page_title="cap.interview", page_icon="🌟")

st.markdown("""
<style>
.stApp, .stMarkdown, label, p, h1, h2, h3 { direction: rtl; text-align: right; }
</style>
""", unsafe_allow_html=True)

QUESTIONS = [
    ("عندك كام سنة؟", [
        "من 5 لـ 7 سنين", "من 8 لـ 10 سنين",
        "من 11 لـ 13 سنة", "14 سنة أو أكتر",
    ]),
    ("بتحب تتعلم إزاي؟", [
        "بالألعاب 🎮", "بالفيديوهات 🎬",
        "بالقصص 📖", "بالأسئلة والتحديات 🧩",
    ]),
    ("تحب يكون في شخصية كرتونية تتكلم معاك؟", [
        "أيوه جدًا", "أيوه بس مش دايمًا",
        "لأ", "مش فارق معايا",
    ]),
    ("تفضّل تجاوب إزاي؟", [
        "أكتب ✍️", "أسجّل بصوتي 🎤",
        "أختار من قائمة 📋", "أختار إيموجي 😊",
    ]),
    ("لو حاجة مضايقاك، تحب التطبيق يساعدك تكلم حد كبير بتثق فيه؟", [
        "أيوه", "ساعات", "لأ، أحب أجرّب لوحدي الأول", "مش عارف",
    ]),
    ("إيه اللي يخليك تستخدم التطبيق كل يوم؟", [
        "مكافآت ونجوم ⭐", "ألعاب جديدة",
        "الشخصية الكرتونية", "تحديات مع أصحابي",
    ]),
    ("إيه اللي يخليك تبطّل تستخدم التطبيق؟", [
        "لو بيزهّقني", "لو صعب",
        "لو فيه كلام كتير", "لو بطيء",
    ]),
    ("لو كنت زعلان، تحب التطبيق يقدملك إيه؟", [
        "نصيحة بسيطة", "قصة قصيرة",
        "لعبة هادية", "تمرين تنفس وراحة",
    ]),
    ("تحب المكافآت تكون إزاي؟", [
        "نجوم ونقاط", "شارات وكؤوس",
        "شخصيات أجمعها", "مفيش مكافآت",
    ]),
    ("لو تقدر تضيف ميزة واحدة، هتكون إيه؟", [
        "ألعاب أكتر", "رسم وتلوين",
        "دروس جديدة", "أتكلم مع الشخصية الكرتونية أكتر",
    ]),
]

FILE = "responses.csv"

st.title ("capstone,interview✨")
st.write("مفيش إجابة صح ولا غلط، وتقدر تسيب أي سؤال مش عايز تجاوب عليه.")

answers = []
for i, (q, options) in enumerate(QUESTIONS):
    choice = st.radio(f"{i + 1}. {q}", options, index=None, key=f"q{i}")
    answers.append(choice)

if st.button("خلصت ✅"):
    row = [datetime.now().strftime("%Y-%m-%d %H:%M")] + [a or "" for a in answers]
    new_file = not os.path.exists(FILE)
    with open(FILE, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["الوقت"] + [q for q, _ in QUESTIONS])
        writer.writerow(row)

    st.balloons()
    st.success("شكرًا ليك! إجاباتك هتساعدنا نعمل تطبيق أحلى 💙")
    with st.expander("شوف إجاباتك"):
        for (q, _), a in zip(QUESTIONS, answers):
            st.write(f"**{q}**  \n{a or '— سبته فاضي —'}")
