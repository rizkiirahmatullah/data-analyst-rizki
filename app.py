import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# --- 1. KONFIGURASI HALAMAN (Wajib di baris pertama) ---
st.set_page_config(page_title="AI Data Analyst Ultimate", layout="wide")

# Judul Keren
st.title("🚀 AI Data Analyst: Ultimate Edition")
st.caption("Mode Full Power: Visualisasi Interaktif + Otak Gemini 3")
st.markdown("---")

# --- 2. SISTEM KUNCI OTOMATIS (AUTO-KEY) ---
# Cek apakah kunci ada di Brankas (Secrets)
try:
    if "GEMINI_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_KEY"]
        status_kunci = "✅ Terhubung (Otomatis)"
    else:
        # Kalau di laptop lokal belum ada secrets
        status_kunci = "⚠️ Mode Manual"
        api_key = None
except:
    status_kunci = "⚠️ Mode Manual"
    api_key = None

# --- 3. SIDEBAR (PANEL KIRI) ---
with st.sidebar:
    st.header("🎛️ Panel Kontrol")
    
    # Status API
    if "Terhubung" in status_kunci:
        st.success(status_kunci)
    else:
        st.warning(status_kunci)
        api_key = st.text_input("Masukkan API Key:", type="password")
    
    st.markdown("---")
    
    # Upload File
    st.subheader("📂 1. Upload Data")
    uploaded_file = st.file_uploader("Format: CSV atau Excel", type=["csv", "xlsx"])

# --- 4. LOGIKA UTAMA APLIKASI ---
if uploaded_file is not None:
    # A. BACA DATA
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # B. TAMPILKAN DATASET
        with st.expander("👀 Lihat Data Mentah (Klik untuk buka/tutup)", expanded=True):
            st.dataframe(df)
            st.info(f"Total Data: {df.shape[0]} baris, {df.shape[1]} kolom")

        st.markdown("---")

        # C. VISUALISASI INTERAKTIF (FITUR V1 YANG HILANG KEMBALI LAGI!) 📊
        st.header("📊 2. Visualisasi Data (Otak-Atik Sendiri)")
        
        # Kolom untuk setting grafik
        col_set1, col_set2, col_set3 = st.columns(3)
        
        with col_set1:
            # Plih Sumbu X
            x_axis = st.selectbox("Pilih Sumbu X (Mendatar):", df.columns, index=0)
        with col_set2:
            # Pilih Sumbu Y
            # Coba cari kolom angka otomatis untuk default
            kolom_angka = df.select_dtypes(include=['float64', 'int64']).columns
            default_y = 0 if len(kolom_angka) > 0 else 0
            y_axis = st.selectbox("Pilih Sumbu Y (Tegak/Angka):", df.columns, index=default_y)
        with col_set3:
            # Pilih Tipe Grafik
            tipe_grafik = st.selectbox("Pilih Tipe Grafik:", ["Bar Chart (Batang)", "Line Chart (Garis)", "Scatter Plot (Titik)", "Pie Chart (Bulat)"])

        # Render Grafik sesuai pilihan
        st.subheader(f"Grafik: {tipe_grafik}")
        
        if tipe_grafik == "Bar Chart (Batang)":
            fig = px.bar(df, x=x_axis, y=y_axis, color=x_axis, title=f"{x_axis} vs {y_axis}")
        elif tipe_grafik == "Line Chart (Garis)":
            fig = px.line(df, x=x_axis, y=y_axis, title=f"Tren {x_axis} vs {y_axis}")
        elif tipe_grafik == "Scatter Plot (Titik)":
            fig = px.scatter(df, x=x_axis, y=y_axis, color=x_axis, size=y_axis, title=f"Sebaran {x_axis} vs {y_axis}")
        elif tipe_grafik == "Pie Chart (Bulat)":
            fig = px.pie(df, names=x_axis, values=y_axis, title=f"Persentase {x_axis}")
        
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # D. ANALISIS AI (FULL POWER GEMINI 3) 🤖
        st.header("🤖 3. Tanya AI (Analisis Mendalam)")
        
        pertanyaan_user = st.text_input("Tanya apa saja tentang data di atas:", placeholder="Contoh: Produk apa yang paling laku? Kenapa?")
        
        if st.button("🚀 Jawab dengan Full Power!"):
            if not api_key:
                st.error("⛔ Kunci API belum dimasukkan! Cek Sidebar.")
            else:
                with st.spinner("Sedang menghubungkan ke Otak Gemini 3..."):
                    try:
                        # 1. Konfigurasi
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel('gemini-3-flash-preview') # Model Terbaru
                        
                        # 2. Siapkan Data (Ambil 50 baris pertama biar cepat)
                        data_sample = df.head(50).to_string()
                        
                        # 3. Prompt Engineering
                        prompt = f"""
                        Kamu adalah Senior Data Analyst yang cerdas dan teliti.
                        Berikut adalah data sampel dari user:
                        
                        {data_sample}
                        
                        Pertanyaan User: {pertanyaan_user}
                        
                        Tugas:
                        1. Jawab pertanyaan berdasarkan data tersebut.
                        2. Berikan insight/wawasan tersembunyi.
                        3. Gunakan bahasa Indonesia yang profesional tapi mudah dimengerti.
                        4. Jika ada angka penting, sebutkan.
                        """
                        
                        # 4. Eksekusi
                        response = model.generate_content(prompt)
                        
                        # 5. Tampilkan
                        st.success("✅ Analisis Selesai:")
                        st.write(response.text)
                        
                    except Exception as e:
                        st.error(f"❌ Terjadi Kesalahan: {e}")
                        st.warning("Tips: Pastikan API Key benar dan data tidak terlalu besar.")

    except Exception as e:
        st.error(f"Gagal membaca file: {e}")
else:
    # Tampilan Awal (Belum Upload)
    st.info("👈 Silakan upload file Excel atau CSV di menu sebelah kiri untuk memulai.")
    st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)