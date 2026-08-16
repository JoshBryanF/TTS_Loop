import asyncio
import edge_tts
import streamlit as st

st.set_page_config(page_title="Mandarin Audio Loop", page_icon="🎧")

st.title("🎧 Mandarin TTS Audio Looper")
st.write("Masukkan teks Mandarin untuk diputar berulang-ulang saat latihan menulis.")

# Input Teks & Pengaturan
text = st.text_area("Teks Mandarin (Hanzi):", "不断地练习才能写出漂亮的汉字。")
speed = st.slider("Kecepatan Suara:", min_value=-50, max_value=20, value=-15, step=5)
voice = st.selectbox(
    "Pilihan Suara:",
    ["zh-CN-XiaoxiaoNeural (Wanita)", "zh-CN-YunjianNeural (Pria)"]
)

voice_code = voice.split(" ")[0]
rate_str = f"{speed}%"

async def generate_audio(text_input, voice_name, rate_val):
    communicate = edge_tts.Communicate(text_input, voice_name, rate=rate_val)
    await communicate.save("output.mp3")

if st.button("Generate Audio"):
    if text.strip():
        with st.spinner("Memproses audio Mandarin..."):
            asyncio.run(generate_audio(text, voice_code, rate_str))
            st.success("Audio berhasil dibuat!")
            
            # Membaca file mp3 untuk ditampilkan di player
            with open("output.mp3", "rb") as audio_file:
                audio_bytes = audio_file.read()
            
            st.audio(audio_bytes, format="audio/mp3", loop=True)
            st.info("💡 **Tips:** Pemutar audio di atas sudah di-set **LOOP secara otomatis**. Kamu juga bisa klik kanan pada player lalu pastikan opsi 'Loop' aktif.")
    else:
        st.warning("Silakan masukkan teks Mandarin terlebih dahulu.")
