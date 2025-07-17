# app.py
import random
import streamlit as st
from transformers import pipeline

st.set_page_config(
    page_title="Auto-Balasan Ulasan ⭐",
    page_icon="🛍️",
    layout="centered"
)

# --- Header ---
st.title("🤖 Auto-Balasan Ulasan Toko")
st.markdown("Balas ulasan otomatis dengan tone & emoji yang bisa dipilih!")

# --- Sidebar konfigurasi ---
with st.sidebar:
    st.header("⚙️ Pengaturan Tone")
    tone = st.selectbox(
        "Pilih tone balasan:",
        ["Ramah", "Fun", "Formal", "Gen-Z", "Sedih", "Ngegas halus"]
    )
    star = st.number_input("Bintang yang diberikan pembeli:", min_value=1, max_value=5, value=5)

# --- Fungsi balasan ---
@st.cache_resource(show_spinner=False)
def load_generator():
    # Model ringan (~250 MB). Untuk kualitas lebih baik ganti ke "google/flan-t5-large"
    return pipeline("text2text-generation", model="google/flan-t5-base")

generator = load_generator()

def build_prompt(star: int, tone: str) -> str:
    emoji_bank = {
        5: ["😍", "🥳", "❤️", "🔥"],
        4: ["🙂", "👍", "✨"],
        3: ["😐", "🤔", "🙏"],
        2: ["😥", "🙁", "💔"],
        1: ["😢", "🙇", "💔"]
    }
    tone_map = {
        "Ramah": "jawab dengan ramah dan hangat",
        "Fun": "tulis dengan gaya fun & playful",
        "Formal": "gunakan bahasa formal dan profesional",
        "Gen-Z": "gunakan gaya bahasa anak muda ala Gen-Z",
        "Sedih": "tampilkan rasa sedih tapi tetap sopan",
        "Ngegas halus": "jawab dengan nada satir halus"
    }

    sample_emoji = " ".join(random.sample(emoji_bank[star], k=min(2, len(emoji_bank[star]))))
    return (
        f"Berikan balasan ulasan singkat untuk pembeli yang memberikan {star} bintang. "
        f"Tone: {tone_map[tone]}. Tambahkan emoji {sample_emoji}. "
        f"Jangan lebih dari 2 kalimat."
    )

# --- Main area ---
st.subheader("🔍 Preview Prompt")
prompt = build_prompt(star, tone)
st.code(prompt, language="text")

if st.button("Generate Balasan"):
    with st.spinner("Sedang mikir..."):
        result = generator(prompt, max_new_tokens=40, do_sample=True, temperature=0.8)
        reply = result[0]["generated_text"].strip()
    st.success("✅ Balasan berhasil dibuat!")
    st.write("**Balasan:**")
    st.info(reply)

# --- Footer ---
st.markdown("---")
st.markdown("by @kimi 🧡")
