# streamlit_app.py
import streamlit as st
import math
import pandas as pd
import numpy as np

# Konfigurasi halaman
st.set_page_config(
    page_title="Kalkulator Keuangan & Aktuaria",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS untuk styling premium - Modern Gradient Theme
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Animated Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #fef9e6 0%, #fff5e6 25%, #fff0e0 50%, #fff5e6 75%, #fef9e6 100%);
        background-attachment: fixed;
    }
    
    /* Animated Header */
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    .main-header {
        background: linear-gradient(135deg, #fef9c3 0%, #ffd89b 50%, #feb47b 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px -15px rgba(0,0,0,0.1);
        border: none;
        animation: slideDown 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 3s infinite;
    }
    
    .main-header h1 {
        color: #7b3f00;
        text-align: center;
        margin: 0;
        font-weight: 800;
        font-size: 2.5rem;
        letter-spacing: -0.5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.05);
    }
    
    .main-header p {
        color: #a05a1a;
        text-align: center;
        margin: 0.75rem 0 0 0;
        font-weight: 500;
        font-size: 1.1rem;
    }
    
    /* Premium Card Effect */
    .result-box, .info-box, .warning-box {
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeIn 0.5s ease-out;
    }
    
    .result-box {
        background: linear-gradient(135deg, rgba(255,255,247,0.95) 0%, rgba(255,250,240,0.95) 100%);
        border-left: 5px solid #f39c12;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05), 0 8px 10px -6px rgba(0,0,0,0.02);
    }
    
    .result-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 35px -10px rgba(0,0,0,0.1);
    }
    
    .info-box {
        background: linear-gradient(135deg, rgba(255,255,247,0.9) 0%, rgba(255,248,235,0.9) 100%);
        border-left: 5px solid #3498db;
    }
    
    .warning-box {
        background: linear-gradient(135deg, rgba(255,251,235,0.95) 0%, rgba(255,243,205,0.95) 100%);
        border-left: 5px solid #e67e22;
    }
    
    /* Menu Cards with 3D effect */
    .menu-card {
        background: linear-gradient(135deg, #ffffff 0%, #fffef7 100%);
        padding: 1.8rem 1.2rem;
        border-radius: 20px;
        text-align: center;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255,200,100,0.3);
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        position: relative;
        overflow: hidden;
    }
    
    .menu-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,215,150,0.4), transparent);
        transition: left 0.5s;
    }
    
    .menu-card:hover::before {
        left: 100%;
    }
    
    .menu-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 30px -12px rgba(255,140,0,0.2);
        border-color: #ffb347;
    }
    
    .menu-icon {
        font-size: 3.5rem;
        margin-bottom: 0.75rem;
        display: inline-block;
        animation: fadeIn 0.5s ease-out;
    }
    
    .menu-card:hover .menu-icon {
        animation: pulse 0.5s ease-in-out;
    }
    
    .menu-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #c45c1b;
        margin-bottom: 0.5rem;
        letter-spacing: -0.3px;
    }
    
    .menu-desc {
        font-size: 0.85rem;
        color: #a5643a;
        line-height: 1.4;
    }
    
    /* Enhanced Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #ffd89b 0%, #feb47b 100%);
        color: #7b3f00;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-size: 0.95rem;
        letter-spacing: 0.3px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #feb47b 0%, #ffa559 100%);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -5px rgba(255,140,0,0.3);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    /* Premium Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background-color: rgba(255,250,240,0.5);
        border-radius: 12px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        background: transparent;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        color: #a05a1a;
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab-list"] button:hover {
        background: rgba(255,215,150,0.3);
        transform: translateY(-1px);
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: linear-gradient(135deg, #ffd89b 0%, #ffc285 100%);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] p {
        color: #7b3f00;
        font-weight: 700;
    }
    
    /* Enhanced Input Fields */
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input,
    .stSelectbox > div > div {
        background: rgba(255,254,247,0.95);
        border: 2px solid #ffe0b5;
        border-radius: 12px;
        transition: all 0.3s ease;
        font-size: 1rem;
        padding: 0.5rem 1rem;
    }
    
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus {
        border-color: #ffb347;
        box-shadow: 0 0 0 3px rgba(255,180,80,0.2);
        outline: none;
    }
    
    /* Radio Button Styling */
    .stRadio > div {
        gap: 1.5rem;
        background: rgba(255,250,240,0.5);
        padding: 0.8rem;
        border-radius: 12px;
    }
    
    .stRadio label {
        color: #a5643a;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stRadio label:hover {
        color: #c45c1b;
        transform: translateX(2px);
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #fffaf0 0%, #fff5e6 100%);
        border-radius: 12px;
        color: #c45c1b;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #fff5e6 0%, #fff0e0 100%);
        transform: translateX(5px);
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    .stDataFrame table {
        border-radius: 12px;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fffef7 0%, #fffaf0 100%);
        border-right: 1px solid rgba(255,200,100,0.2);
    }
    
    /* Alert/Info Messages */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid;
        animation: slideDown 0.4s ease-out;
    }
    
    /* Success/Error/Warning Messages */
    .stSuccess, .stError, .stInfo, .stWarning {
        border-radius: 12px;
        animation: fadeIn 0.4s ease-out;
    }
    
    /* Number formatting */
    .result-box h4 {
        color: #c45c1b;
        margin-top: 0;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .result-box p {
        margin: 0.75rem 0;
        font-size: 1.05rem;
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(255,255,247,0.8);
        border-radius: 12px;
        padding: 1rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        background: rgba(255,255,247,0.95);
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #fff5e6;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #ffd89b 0%, #feb47b 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #feb47b 0%, #ffa559 100%);
    }
    
    /* Loading animation */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Footer Styling */
    footer {
        opacity: 0.8;
        transition: opacity 0.3s ease;
    }
    
    footer:hover {
        opacity: 1;
    }
    
    /* Divider Styling */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #ffd89b, #feb47b, #ffd89b, transparent);
    }
    </style>
""", unsafe_allow_html=True)

# Header dengan animasi
def show_header():
    st.markdown("""
    <div class="main-header">
        <h1>💰 KALKULATOR KEUANGAN & AKTUARIA</h1>
        <p>Financial & Actuarial Calculator — Solusi Cerdas untuk Perencanaan Keuangan Anda</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# FUNGSI SEMUA KELOMPOK (dengan sedikit peningkatan UI)
# ============================================================

def kelompok_bunga():
    st.subheader("📘 BUNGA & NILAI WAKTU UANG")
    st.markdown("### *✨ Tabungan bank, deposito, pinjaman sederhana*")
    
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("← Kembali ke Menu", key="back_bunga", use_container_width=True):
            st.session_state.page = "menu"
            st.rerun()
    with col2:
        st.markdown("")
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Bunga Sederhana", "📊 Bunga Majemuk (Tahunan)", "🔄 Bunga Majemuk (m-kali)", "🔍 Mencari P/i/t"
    ])
    
    with tab1:
        st.markdown("### 💰 Bunga Sederhana")
        st.info("💡 **Rumus:** I = P × i × t, A = P + I")
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            P = st.number_input("💵 Pokok (P) - Rp", min_value=0.0, value=1000000.0, step=100000.0, key="simple_P")
            i = st.number_input("📈 Tingkat bunga per tahun (%)", min_value=0.0, value=10.0, step=0.5, key="simple_i") / 100
        with col2:
            t = st.number_input("⏰ Waktu (tahun)", min_value=0.0, value=1.0, step=0.5, key="simple_t")
        
        if st.button("🧮 Hitung Bunga Sederhana", key="btn_simple", use_container_width=True):
            I = P * i * t
            A = P + I
            st.markdown(f"""
            <div class="result-box">
                <h4>✅ Hasil Perhitungan:</h4>
                <p>📌 <b>Bunga (I):</b> Rp {I:,.0f}</p>
                <p>📌 <b>Nilai Akumulasi (A):</b> Rp {A:,.0f}</p>
                <hr style="margin: 10px 0;">
                <p style="font-size: 0.9em; color: #666;">📝 <i>Total yang akan diterima setelah {t} tahun</i></p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📈 Bunga Majemuk (Tahunan)")
        st.info("💡 **Rumus:** A = P(1 + i)^n")
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            P = st.number_input("💵 Pokok (P) - Rp", min_value=0.0, value=1000000.0, step=100000.0, key="comp_P")
            i = st.number_input("📈 Tingkat bunga (% per tahun)", min_value=0.0, value=10.0, step=0.5, key="comp_i") / 100
        with col2:
            n = st.number_input("⏰ Jumlah tahun", min_value=1, value=5, step=1, key="comp_n")
        
        if st.button("🧮 Hitung Bunga Majemuk", key="btn_comp", use_container_width=True):
            A = P * (1 + i) ** n
            pertumbuhan = ((A - P) / P) * 100
            st.markdown(f"""
            <div class="result-box">
                <h4>✅ Hasil Perhitungan:</h4>
                <p>📌 <b>Nilai Akumulasi:</b> Rp {A:,.0f}</p>
                <p>📌 <b>Total Pertumbuhan:</b> {pertumbuhan:.1f}%</p>
                <p style="font-size: 0.9em; color: #666;">📝 <i>Nilai investasi setelah {n} tahun dengan bunga majemuk</i></p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🔄 Bunga Majemuk (m-kali setahun)")
        st.info("💡 **Rumus:** A = P(1 + i(m)/m)^(m×t)")
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            P = st.number_input("💵 Pokok (P) - Rp", min_value=0.0, value=1000000.0, step=100000.0, key="compm_P")
            i_nom = st.number_input("📈 Bunga nominal (% per tahun)", min_value=0.0, value=12.0, step=0.5, key="compm_i") / 100
        with col2:
            m_map = {"📅 Tahunan (m=1)": 1, "📆 Semesteran (m=2)": 2, "📊 Triwulanan (m=4)": 4, "📈 Bulanan (m=12)": 12}
            m_choice = st.selectbox("🔄 Frekuensi konversi", list(m_map.keys()), key="compm_m")
            m = m_map[m_choice]
            t = st.number_input("⏰ Waktu (tahun)", min_value=0.0, value=1.0, step=0.5, key="compm_t")
        
        if st.button("🧮 Hitung Bunga Majemuk (m-kali)", key="btn_compm", use_container_width=True):
            A = P * (1 + i_nom / m) ** (m * t)
            i_eff = ((1 + i_nom / m) ** m - 1) * 100
            st.markdown(f"""
            <div class="result-box">
                <h4>✅ Hasil Perhitungan:</h4>
                <p>📌 <b>Nilai Akumulasi:</b> Rp {A:,.0f}</p>
                <p>📌 <b>Bunga Efektif Tahunan:</b> {i_eff:.2f}%</p>
                <p style="font-size: 0.9em; color: #666;">📝 <i>Dengan konversi {m_choice.split()[0]} ({m}x/tahun)</i></p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 🔍 Mencari P / i / t (Bunga Sederhana)")
        st.info("💡 **Rumus:** P = A/(1+i×t), i = (A-P)/(P×t), t = (A-P)/(P×i)")
        
        search_type = st.selectbox("🎯 Pilih yang dicari", ["💰 Pokok (P)", "📈 Tingkat bunga (i)", "⏰ Waktu (t)"], key="search_type")
        
        if search_type == "💰 Pokok (P)":
            A = st.number_input("💵 Nilai Akumulasi (A) - Rp", min_value=0.0, value=1100000.0, step=100000.0, key="search_A")
            i = st.number_input("📈 Tingkat bunga (%)", min_value=0.0, value=10.0, step=0.5, key="search_i") / 100
            t = st.number_input("⏰ Waktu (tahun)", min_value=0.0, value=1.0, step=0.5, key="search_t")
            if st.button("🧮 Hitung Pokok", key="btn_search_P", use_container_width=True):
                P = A / (1 + i * t)
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Perhitungan:</h4>
                    <p>📌 <b>Pokok Awal (P):</b> Rp {P:,.0f}</p>
                    <p style="font-size: 0.9em; color: #666;">📝 <i>Modal awal yang diperlukan untuk mencapai Rp {A:,.0f} dalam {t} tahun</i></p>
                </div>
                """, unsafe_allow_html=True)
        
        elif search_type == "📈 Tingkat bunga (i)":
            P = st.number_input("💰 Pokok (P) - Rp", min_value=0.0, value=1000000.0, step=100000.0, key="search_P")
            A = st.number_input("💵 Nilai Akumulasi (A) - Rp", min_value=0.0, value=1100000.0, step=100000.0, key="search_A2")
            t = st.number_input("⏰ Waktu (tahun)", min_value=0.0, value=1.0, step=0.5, key="search_t2")
            if st.button("🧮 Hitung Tingkat Bunga", key="btn_search_i", use_container_width=True):
                i = (A - P) / (P * t) * 100
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Perhitungan:</h4>
                    <p>📌 <b>Tingkat bunga (i):</b> {i:.2f}% per tahun</p>
                    <p style="font-size: 0.9em; color: #666;">📝 <i>Dibutuhkan tingkat bunga {i:.2f}% agar Rp {P:,.0f} menjadi Rp {A:,.0f} dalam {t} tahun</i></p>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            P = st.number_input("💰 Pokok (P) - Rp", min_value=0.0, value=1000000.0, step=100000.0, key="search_P3")
            A = st.number_input("💵 Nilai Akumulasi (A) - Rp", min_value=0.0, value=1100000.0, step=100000.0, key="search_A3")
            i = st.number_input("📈 Tingkat bunga (%)", min_value=0.0, value=10.0, step=0.5, key="search_i3") / 100
            if st.button("🧮 Hitung Waktu", key="btn_search_t", use_container_width=True):
                t = (A - P) / (P * i)
                tahun = int(t)
                bulan = (t - tahun) * 12
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Perhitungan:</h4>
                    <p>📌 <b>Waktu (t):</b> {t:.2f} tahun</p>
                    <p>📌 <b>Atau:</b> {tahun} tahun {bulan:.0f} bulan</p>
                    <p style="font-size: 0.9em; color: #666;">📝 <i>Dibutuhkan waktu {t:.2f} tahun agar Rp {P:,.0f} menjadi Rp {A:,.0f}</i></p>
                </div>
                """, unsafe_allow_html=True)


def kelompok_nilai_sekarang():
    st.subheader("📙 NILAI SEKARANG & DISKONTO")
    st.markdown("### *✨ Valuasi aset & instrumen diskonto*")
    
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("← Kembali ke Menu", key="back_nilai", use_container_width=True):
            st.session_state.page = "menu"
            st.rerun()
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["💰 Nilai Sekarang (PV)", "🔄 Konversi i ↔ d", "📄 Diskonto Wesel/SBI"])
    
    with tab1:
        st.markdown("### 💰 Nilai Sekarang (PV) dari FV")
        st.info("💡 **Rumus:** PV = FV / (1 + i)^n")
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            FV = st.number_input("💵 Nilai masa depan (FV) - Rp", min_value=0.0, value=1000000.0, step=100000.0, key="pv_FV")
            i = st.number_input("📈 Tingkat bunga (% per tahun)", min_value=0.0, value=10.0, step=0.5, key="pv_i") / 100
        with col2:
            n = st.number_input("⏰ Jumlah tahun", min_value=1, value=5, step=1, key="pv_n")
        
        if st.button("🧮 Hitung Nilai Sekarang", key="btn_pv", use_container_width=True):
            PV = FV / (1 + i) ** n
            diskon = ((FV - PV) / FV) * 100
            st.markdown(f"""
            <div class="result-box">
                <h4>✅ Hasil Perhitungan:</h4>
                <p>📌 <b>Nilai Sekarang (PV):</b> Rp {PV:,.0f}</p>
                <p>📌 <b>Total Diskonto:</b> {diskon:.1f}% dari FV</p>
                <p style="font-size: 0.9em; color: #666;">📝 <i>Nilai saat ini dari Rp {FV:,.0f} yang akan diterima {n} tahun mendatang</i></p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🔄 Konversi i ↔ d")
        st.info("💡 **Rumus:** d = i/(1+i), i = d/(1-d)")
        
        conv_type = st.radio("🎯 Pilih konversi", ["📈 i → d (tingkat diskonto)", "📉 d → i (tingkat bunga)"], horizontal=True)
        
        if conv_type == "📈 i → d (tingkat diskonto)":
            i = st.number_input("📈 Tingkat bunga i (%)", min_value=0.0, value=10.0, step=0.5, key="conv_i") / 100
            if st.button("🔄 Konversi i → d", key="btn_id", use_container_width=True):
                d = i / (1 + i) * 100
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Konversi:</h4>
                    <p>📌 <b>Tingkat diskonto d:</b> {d:.4f}%</p>
                    <p style="font-size: 0.9em; color: #666;">📝 <i>Tingkat diskonto setara dengan bunga {i*100:.2f}%</i></p>
                </div>
                """, unsafe_allow_html=True)
        else:
            d = st.number_input("📉 Tingkat diskonto d (%)", min_value=0.0, value=9.09, step=0.1, key="conv_d") / 100
            if st.button("🔄 Konversi d → i", key="btn_di", use_container_width=True):
                i = d / (1 - d) * 100
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Konversi:</h4>
                    <p>📌 <b>Tingkat bunga i:</b> {i:.4f}%</p>
                    <p style="font-size: 0.9em; color: #666;">📝 <i>Tingkat bunga setara dengan diskonto {d*100:.2f}%</i></p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 📄 Diskonto Wesel / SBI")
        st.info("💡 **Rumus:** Harga = Nominal × (1 - d × t), Yield = (Nominal - Harga)/(Harga × t) × 100%")
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            nominal = st.number_input("💵 Nilai nominal wesel - Rp", min_value=0.0, value=10000000.0, step=1000000.0, key="disc_nominal")
            d = st.number_input("📉 Tingkat diskonto (% per tahun)", min_value=0.0, value=8.0, step=0.5, key="disc_d") / 100
        with col2:
            t_hari = st.number_input("📅 Jatuh tempo (hari)", min_value=1, value=90, step=30, key="disc_t")
            t = t_hari / 360
        
        if st.button("🧮 Hitung Diskonto", key="btn_disc", use_container_width=True):
            harga = nominal * (1 - d * t)
            yield_rate = (nominal - harga) / (harga * t) * 100
            diskon_amount = nominal - harga
            st.markdown(f"""
            <div class="result-box">
                <h4>✅ Hasil Perhitungan:</h4>
                <p>📌 <b>Harga wesel:</b> Rp {harga:,.0f}</p>
                <p>📌 <b>Nilai Diskonto:</b> Rp {diskon_amount:,.0f}</p>
                <p>📌 <b>Tingkat bunga efektif (yield):</b> {yield_rate:.2f}%</p>
                <p style="font-size: 0.9em; color: #666;">📝 <i>Dengan diskonto {d*100:.1f}% untuk {t_hari} hari</i></p>
            </div>
            """, unsafe_allow_html=True)


def kelompok_bunga_nominal():
    st.subheader("📗 BUNGA NOMINAL & KONTINYU")
    st.markdown("### *✨ Analisis bunga frekuensi tinggi & continuous compounding*")
    
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("← Kembali ke Menu", key="back_nominal", use_container_width=True):
            st.session_state.page = "menu"
            st.rerun()
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📊 i(m) → i efektif", "📉 d(m) → i efektif", "⚡ Kekuatan Bunga (δ)"])
    
    with tab1:
        st.markdown("### 📊 Konversi i(m) → i Efektif")
        st.info("💡 **Rumus:** i_eff = (1 + i(m)/m)^m - 1")
        
        i_nom = st.number_input("📈 Bunga nominal i(m) (%)", min_value=0.0, value=12.0, step=0.5, key="nom_i") / 100
        m_map = {"📅 Tahunan (m=1)": 1, "📆 Semesteran (m=2)": 2, "📊 Triwulanan (m=4)": 4, "📈 Bulanan (m=12)": 12}
        m_choice = st.selectbox("🔄 Frekuensi konversi (m)", list(m_map.keys()), key="nom_m")
        m = m_map[m_choice]
        
        if st.button("🔄 Konversi ke i Efektif", key="btn_nom2eff", use_container_width=True):
            i_eff = ((1 + i_nom / m) ** m - 1) * 100
            selisih = i_eff - (i_nom * 100)
            st.markdown(f"""
            <div class="result-box">
                <h4>✅ Hasil Konversi:</h4>
                <p>📌 <b>Tingkat bunga efektif:</b> {i_eff:.4f}% per tahun</p>
                <p>📌 <b>Selisih dengan nominal:</b> {selisih:+.4f}%</p>
                <p style="font-size: 0.9em; color: #666;">📝 <i>Bunga nominal {i_nom*100:.2f}% dengan konversi {m_choice.split()[0]} menghasilkan bunga efektif {i_eff:.4f}%</i></p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📉 Konversi d(m) → i Efektif")
        st.info("💡 **Rumus:** i_eff = (1 - d(m)/m)^(-m) - 1")
        
        d_nom = st.number_input("📉 Tingkat diskonto nominal d(m) (%)", min_value=0.0, value=10.0, step=0.5, key="nom_d") / 100
        m_map2 = {"📅 Tahunan (m=1)": 1, "📆 Semesteran (m=2)": 2, "📊 Triwulanan (m=4)": 4, "📈 Bulanan (m=12)": 12}
        m_choice2 = st.selectbox("🔄 Frekuensi konversi (m)", list(m_map2.keys()), key="nom_m2")
        m2 = m_map2[m_choice2]
        
        if st.button("🔄 Konversi ke i Efektif (d(m))", key="btn_d2eff", use_container_width=True):
            i_eff = ((1 - d_nom / m2) ** (-m2) - 1) * 100
            st.markdown(f"""
            <div class="result-box">
                <h4>✅ Hasil Konversi:</h4>
                <p>📌 <b>Tingkat bunga efektif:</b> {i_eff:.4f}% per tahun</p>
                <p style="font-size: 0.9em; color: #666;">📝 <i>Diskonto nominal {d_nom*100:.2f}% dengan konversi {m_choice2.split()[0]} setara dengan bunga efektif {i_eff:.4f}%</i></p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### ⚡ Kekuatan Bunga (δ) & Kontinyu")
        st.info("💡 **Rumus:** δ = ln(1+i), A = P·e^(δt)")
        
        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["📈 i → δ", "📉 δ → i", "💰 Nilai Akumulasi Kontinyu"])
        
        with sub_tab1:
            i = st.number_input("📈 Tingkat bunga i (%)", min_value=0.0, value=10.0, step=0.5, key="delta_i") / 100
            if st.button("⚡ Hitung δ", key="btn_i2delta", use_container_width=True):
                delta = math.log(1 + i) * 100
                st.markdown(f"""
                <div class="result-box">
                    <p>📌 <b>Kekuatan bunga δ:</b> {delta:.4f}%</p>
                    <p style="font-size: 0.9em; color: #666;">📝 <i>Tingkat pertumbuhan kontinyu setara dengan bunga {i*100:.2f}%</i></p>
                </div>
                """, unsafe_allow_html=True)
        
        with sub_tab2:
            delta = st.number_input("⚡ Kekuatan bunga δ (%)", min_value=0.0, value=9.53, step=0.5, key="delta_val") / 100
            if st.button("📈 Hitung i", key="btn_delta2i", use_container_width=True):
                i = (math.exp(delta) - 1) * 100
                st.markdown(f"""
                <div class="result-box">
                    <p>📌 <b>Tingkat bunga i:</b> {i:.4f}%</p>
                    <p style="font-size: 0.9em; color: #666;">📝 <i>Tingkat bunga diskrit setara dengan kekuatan bunga {delta*100:.2f}%</i></p>
                </div>
                """, unsafe_allow_html=True)
        
        with sub_tab3:
            col1, col2 = st.columns(2)
            with col1:
                P = st.number_input("💰 Pokok (P) - Rp", min_value=0.0, value=1000000.0, step=100000.0, key="cont_P")
                delta = st.number_input("⚡ Kekuatan bunga δ (%)", min_value=0.0, value=9.53, step=0.5, key="cont_delta") / 100
            with col2:
                t = st.number_input("⏰ Waktu (tahun)", min_value=0.0, value=5.0, step=0.5, key="cont_t")
            if st.button("🧮 Hitung Akumulasi Kontinyu", key="btn_cont", use_container_width=True):
                A = P * math.exp(delta * t)
                i_eff = (math.exp(delta) - 1) * 100
                st.markdown(f"""
                <div class="result-box">
                    <p>📌 <b>Nilai akumulasi:</b> Rp {A:,.0f}</p>
                    <p>📌 <b>Bunga efektif setara:</b> {i_eff:.2f}%</p>
                    <p style="font-size: 0.9em; color: #666;">📝 <i>Dengan pemajemukan kontinyu (bunga dihitung terus-menerus)</i></p>
                </div>
                """, unsafe_allow_html=True)


def kelompok_persamaan_nilai():
    st.subheader("📕 PERSAMAAN NILAI & NPV")
    st.markdown("### *✨ Analisis kelayakan proyek & investasi*")
    
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("← Kembali ke Menu", key="back_persamaan", use_container_width=True):
            st.session_state.page = "menu"
            st.rerun()
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["💰 NPV", "📈 IRR", "🔄 Pembayaran Tunggal Pengganti Utang"])
    
    with tab1:
        st.markdown("### 💰 NPV (Net Present Value)")
        st.info("💡 **Rumus:** NPV = Σ CFt / (1+i)^t")
        
        cf0 = st.number_input("💵 Investasi awal (negatif) - Rp", min_value=-1e12, value=-10000000.0, step=1000000.0, key="npv_cf0")
        n = st.number_input("📊 Jumlah periode arus kas", min_value=1, max_value=20, value=5, step=1, key="npv_n")
        
        st.markdown("**📋 Arus Kas per Tahun:**")
        cf = []
        cols = st.columns(min(n, 5))
        for i in range(n):
            with cols[i % len(cols)]:
                cf.append(st.number_input(f"Tahun ke-{i+1}", min_value=0.0, value=3000000.0, step=1000000.0, key=f"npv_cf_{i}"))
        
        i = st.number_input("📉 Tingkat diskonto (%)", min_value=0.0, value=10.0, step=0.5, key="npv_i") / 100
        
        if st.button("🧮 Hitung NPV", key="btn_npv", use_container_width=True):
            npv_val = cf0
            for t, cash in enumerate(cf, start=1):
                npv_val += cash / (1 + i) ** t
            
            pi = -npv_val / cf0 if cf0 != 0 else 0
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Perhitungan:</h4>
                    <p>📌 <b>NPV:</b> Rp {npv_val:,.0f}</p>
                    <p>📌 <b>Profitability Index:</b> {pi:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if npv_val > 0:
                    st.success("✅ **KESIMPULAN:** Proyek LAYAK (NPV positif)")
                    st.metric("Potensi Keuntungan", f"Rp {npv_val:,.0f}", delta="Positif")
                elif npv_val < 0:
                    st.error("❌ **KESIMPULAN:** Proyek TIDAK LAYAK (NPV negatif)")
                    st.metric("Potensi Kerugian", f"Rp {abs(npv_val):,.0f}", delta="Negatif")
                else:
                    st.info("ℹ️ **KESIMPULAN:** Proyek impas (NPV = 0)")
    
    with tab2:
        st.markdown("### 📈 IRR (Internal Rate of Return)")
        st.warning("⚠️ **Metode:** Trial & error (estimasi)")
        
        cf0 = st.number_input("💵 Investasi awal (negatif) - Rp", min_value=-1e12, value=-10000000.0, step=1000000.0, key="irr_cf0")
        n = st.number_input("📊 Jumlah periode", min_value=1, max_value=20, value=5, step=1, key="irr_n")
        
        st.markdown("**📋 Arus Kas per Tahun:**")
        cf = []
        cols = st.columns(min(n, 5))
        for i in range(n):
            with cols[i % len(cols)]:
                cf.append(st.number_input(f"Tahun ke-{i+1}", min_value=0.0, value=3000000.0, step=1000000.0, key=f"irr_cf_{i}"))
        
        def npv_func(rate):
            result = cf0
            for t, cash in enumerate(cf, start=1):
                result += cash / (1 + rate) ** t
            return result
        
        if st.button("🧮 Hitung IRR", key="btn_irr", use_container_width=True):
            guess = 0.1
            for _ in range(50):
                if npv_func(guess) > 0:
                    guess += 0.01
                else:
                    guess -= 0.001
            
            npv_at_irr = npv_func(guess)
            st.markdown(f"""
            <div class="result-box">
                <h4>✅ Hasil Perhitungan:</h4>
                <p>📌 <b>Estimasi IRR:</b> {guess * 100:.2f}%</p>
                <p>📌 <b>NPV pada IRR:</b> Rp {npv_at_irr:,.0f}</p>
                <p style="font-size: 0.9em; color: #666;">📝 <i>Tingkat pengembalian internal proyek</i></p>
            </div>
            """, unsafe_allow_html=True)
            
            if guess * 100 > 15:
                st.success(f"✨ Proyek menarik dengan IRR {guess*100:.1f}%")
            elif guess * 100 > 10:
                st.info(f"📊 Proyek cukup baik dengan IRR {guess*100:.1f}%")
            else:
                st.warning(f"⚠️ Proyek kurang menarik dengan IRR {guess*100:.1f}%")
    
    with tab3:
        st.markdown("### 🔄 Pembayaran Tunggal Pengganti Utang")
        st.info("💡 **Prinsip:** Nilai utang = Nilai pembayaran baru pada tanggal fokus")
        
        n_utang = st.number_input("📋 Jumlah utang", min_value=1, max_value=10, value=2, step=1, key="utang_n")
        
        utang = []
        tahun = []
        for i in range(n_utang):
            st.markdown(f"**📌 Utang ke-{i+1}:**")
            col1, col2 = st.columns(2)
            with col1:
                u = st.number_input(f"Nilai utang", min_value=0.0, value=5000000.0, step=1000000.0, key=f"utang_{i}")
            with col2:
                t = st.number_input(f"Jatuh tempo (tahun)", min_value=0.0, value=i+1.0, step=0.5, key=f"tahun_{i}")
            utang.append(u)
            tahun.append(t)
        
        i = st.number_input("📈 Tingkat bunga (%)", min_value=0.0, value=10.0, step=0.5, key="utang_i") / 100
        t_fokus = st.number_input("🎯 Tanggal fokus (tahun)", min_value=0.0, value=2.0, step=0.5, key="t_fokus")
        
        if st.button("🧮 Hitung Pembayaran", key="btn_utang", use_container_width=True):
            total = 0
            detail = []
            for u, t in zip(utang, tahun):
                nilai = u * (1 + i) ** (t_fokus - t)
                total += nilai
                detail.append(f"Utang Rp {u:,.0f} (jatuh tempo {t} tahun) → Rp {nilai:,.0f}")
            
            st.markdown(f"""
            <div class="result-box">
                <h4>✅ Hasil Perhitungan:</h4>
                <p>📌 <b>Pembayaran tunggal pada tahun ke-{t_fokus}:</b> Rp {total:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📋 Detail Perhitungan"):
                for d in detail:
                    st.write(f"• {d}")
                st.write(f"**Total:** Rp {total:,.0f}")


def kelompok_anuitas():
    st.subheader("📔 ANUITAS")
    st.markdown("### *✨ KPR, kredit, dana pensiun*")
    
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("← Kembali ke Menu", key="back_anuitas", use_container_width=True):
            st.session_state.page = "menu"
            st.rerun()
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Anuitas Immediate", "📈 Anuitas Due", "🔍 Mencari R/n", "📋 Amortisasi", "♾️ Perpetuitas"
    ])
    
    with tab1:
        st.markdown("### 📊 Anuitas Immediate")
        st.info("💡 **Pembayaran di AKHIR periode**")
        
        pv_fv = st.radio("🎯 Pilih perhitungan", ["💰 Nilai Sekarang (PV)", "💵 Nilai Akumulasi (FV)"], horizontal=True, key="imm_choice")
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            R = st.number_input("💵 Pembayaran periodik (R) - Rp", min_value=0.0, value=1000000.0, step=100000.0, key="imm_R")
            i = st.number_input("📈 Tingkat bunga per periode (%)", min_value=0.0, value=10.0, step=0.5, key="imm_i") / 100
        with col2:
            n = st.number_input("⏰ Jumlah periode", min_value=1, value=5, step=1, key="imm_n")
        
        if st.button("🧮 Hitung Anuitas Immediate", key="btn_imm", use_container_width=True):
            if pv_fv == "💰 Nilai Sekarang (PV)":
                PV = R * (1 - (1 + i) ** -n) / i
                st.markdown(f"""
                <div class="result-box">
                    <p>📌 <b>Nilai Sekarang:</b> Rp {PV:,.0f}</p>
                    <p style="font-size: 0.9em; color: #666;">📝 <i>Total nilai sekarang dari {n} kali pembayaran Rp {R:,.0f} di akhir periode</i></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                FV = R * ((1 + i) ** n - 1) / i
                st.markdown(f"""
                <div class="result-box">
                    <p>📌 <b>Nilai Akumulasi:</b> Rp {FV:,.0f}</p>
                    <p style="font-size: 0.9em; color: #666;">📝 <i>Total nilai setelah {n} periode dari {n} kali pembayaran Rp {R:,.0f}</i></p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📈 Anuitas Due")
        st.info("💡 **Pembayaran di AWAL periode**")
        
        pv_fv2 = st.radio("🎯 Pilih perhitungan", ["💰 Nilai Sekarang (PV)", "💵 Nilai Akumulasi (FV)"], horizontal=True, key="due_choice")
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            R = st.number_input("💵 Pembayaran periodik (R) - Rp", min_value=0.0, value=1000000.0, step=100000.0, key="due_R")
            i = st.number_input("📈 Tingkat bunga per periode (%)", min_value=0.0, value=10.0, step=0.5, key="due_i") / 100
        with col2:
            n = st.number_input("⏰ Jumlah periode", min_value=1, value=5, step=1, key="due_n")
        
        d = i / (1 + i)
        
        if st.button("🧮 Hitung Anuitas Due", key="btn_due", use_container_width=True):
            if pv_fv2 == "💰 Nilai Sekarang (PV)":
                PV = R * (1 - (1 + i) ** -n) / d
                st.markdown(f"""
                <div class="result-box">
                    <p>📌 <b>Nilai Sekarang:</b> Rp {PV:,.0f}</p>
                    <p style="font-size: 0.9em; color: #666;">📝 <i>Nilai sekarang dari {n} kali pembayaran di awal periode (lebih mahal dari immediate)</i></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                FV = R * ((1 + i) ** n - 1) / d
                st.markdown(f"""
                <div class="result-box">
                    <p>📌 <b>Nilai Akumulasi:</b> Rp {FV:,.0f}</p>
                    <p style="font-size: 0.9em; color: #666;">📝 <i>Nilai akhir dari {n} kali pembayaran di awal periode</i></p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🔍 Mencari R atau n")
        
        search_choice = st.radio("🎯 Pilih", ["🔍 Mencari R dari PV", "🔍 Mencari n dari PV"], horizontal=True, key="search_choice")
        
        i = st.number_input("📈 Tingkat bunga per periode (%)", min_value=0.0, value=10.0, step=0.5, key="search_i") / 100
        
        if search_choice == "🔍 Mencari R dari PV":
            PV = st.number_input("💰 Nilai Sekarang (PV) - Rp", min_value=0.0, value=3790786.0, step=100000.0, key="search_PV")
            n = st.number_input("⏰ Jumlah periode", min_value=1, value=5, step=1, key="search_n")
            if st.button("🧮 Hitung R", key="btn_R", use_container_width=True):
                R = PV * i / (1 - (1 + i) ** -n)
                total_pembayaran = R * n
                st.markdown(f"""
                <div class="result-box">
                    <p>📌 <b>Pembayaran periodik (R):</b> Rp {R:,.0f}</p>
                    <p>📌 <b>Total pembayaran:</b> Rp {total_pembayaran:,.0f}</p>
                    <p>📌 <b>Total bunga:</b> Rp {total_pembayaran - PV:,.0f}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            PV = st.number_input("💰 Nilai Sekarang (PV) - Rp", min_value=0.0, value=3790786.0, step=100000.0, key="search_PV2")
            R = st.number_input("💵 Pembayaran periodik (R) - Rp", min_value=0.0, value=1000000.0, step=100000.0, key="search_R")
            if st.button("🧮 Hitung n", key="btn_n", use_container_width=True):
                a_n = PV / R
                n = -math.log(1 - a_n * i) / math.log(1 + i)
                st.markdown(f"""
                <div class="result-box">
                    <p>📌 <b>Jumlah periode (n):</b> {n:.2f} periode</p>
                    <p style="font-size: 0.9em; color: #666;">📝 <i>Dibutuhkan {n:.1f} periode untuk melunasi pinjaman</i></p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 📋 Tabel Amortisasi Pinjaman")
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            P = st.number_input("💰 Pokok pinjaman - Rp", min_value=0.0, value=10000000.0, step=1000000.0, key="amort_P")
            i = st.number_input("📈 Tingkat bunga per periode (%)", min_value=0.0, value=10.0, step=0.5, key="amort_i") / 100
        with col2:
            n = st.number_input("⏰ Jumlah periode", min_value=1, max_value=60, value=5, step=1, key="amort_n")
        
        if st.button("📊 Buat Tabel Amortisasi", key="btn_amort", use_container_width=True):
            R = P * i / (1 - (1 + i) ** -n)
            st.success(f"📌 **Angsuran per periode = Rp {R:,.0f}**")
            
            data = []
            sisa = P
            for t in range(1, n + 1):
                bunga = sisa * i
                pokok = R - bunga
                sisa -= pokok
                data.append({
                    "Periode": t,
                    "Pembayaran": f"Rp {R:,.0f}",
                    "Bunga": f"Rp {bunga:,.0f}",
                    "Pokok": f"Rp {pokok:,.0f}",
                    "Sisa Utang": f"Rp {max(sisa, 0):,.0f}"
                })
            
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Ringkasan
            total_bunga = sum([float(d["Bunga"].replace("Rp ", "").replace(",", "")) for d in data])
            st.info(f"📊 **Ringkasan:** Total bunga yang dibayarkan = Rp {total_bunga:,.0f}")
    
    with tab5:
        st.markdown("### ♾️ Perpetuitas")
        st.info("💡 **Anuitas tak hingga**")
        
        perp_type = st.selectbox("🎯 Jenis Perpetuitas", ["♾️ Perpetuitas biasa", "⏰ Perpetuitas ditunda", "📈 Perpetuitas dengan pertumbuhan"])
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            R = st.number_input("💵 Pembayaran periodik - Rp", min_value=0.0, value=1000000.0, step=100000.0, key="perp_R")
            i = st.number_input("📈 Tingkat bunga (%)", min_value=0.0, value=10.0, step=0.5, key="perp_i") / 100
        
        if perp_type == "♾️ Perpetuitas biasa":
            if st.button("🧮 Hitung Perpetuitas Biasa", key="btn_perp1", use_container_width=True):
                PV = R / i
                st.markdown(f"""
                <div class="result-box">
                    <p>📌 <b>Nilai Sekarang:</b> Rp {PV:,.0f}</p>
                    <p style="font-size: 0.9em; color: #666;">📝 <i>Nilai sekarang dari aliran dana Rp {R:,.0f} per periode selamanya</i></p>
                </div>
                """, unsafe_allow_html=True)
        
        elif perp_type == "⏰ Perpetuitas ditunda":
            with col2:
                t_tunda = st.number_input("⏰ Penundaan (periode)", min_value=1, value=3, step=1, key="t_tunda")
            if st.button("🧮 Hitung Perpetuitas Ditunda", key="btn_perp2", use_container_width=True):
                PV = (R / i) / (1 + i) ** t_tunda
                st.markdown(f"""
                <div class="result-box">
                    <p>📌 <b>Nilai Sekarang (ditunda {t_tunda} periode):</b> Rp {PV:,.0f}</p>
                    <p style="font-size: 0.9em; color: #666;">📝 <i>Nilai sekarang dari perpetuitas yang mulai {t_tunda} periode lagi</i></p>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            with col2:
                g = st.number_input("📈 Tingkat pertumbuhan (%)", min_value=0.0, value=5.0, step=0.5, key="g") / 100
            if st.button("🧮 Hitung Growing Perpetuity", key="btn_perp3", use_container_width=True):
                if i <= g:
                    st.error("❌ Error: Tingkat bunga (i) harus LEBIH BESAR dari tingkat pertumbuhan (g)")
                else:
                    PV = R / (i - g)
                    st.markdown(f"""
                    <div class="result-box">
                        <p>📌 <b>Nilai Sekarang (growing perpetuity):</b> Rp {PV:,.0f}</p>
                        <p style="font-size: 0.9em; color: #666;">📝 <i>Nilai sekarang dengan pertumbuhan {g*100:.1f}% per periode</i></p>
                    </div>
                    """, unsafe_allow_html=True)


def kelompok_anuitas_khusus():
    st.subheader("📒 ANUITAS KHUSUS")
    st.markdown("### *✨ Valuasi dengan inflasi atau arus kas meningkat*")
    
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("← Kembali ke Menu", key="back_khusus", use_container_width=True):
            st.session_state.page = "menu"
            st.rerun()
    
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["📈 Anuitas dengan Pertumbuhan", "♾️ Anuitas Kontinyu"])
    
    with tab1:
        st.markdown("### 📈 Anuitas dengan Pertumbuhan")
        st.info("💡 **Rumus:** PV = R1 × (1 - ((1+g)/(1+i))^n) / (i - g)")
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            R1 = st.number_input("💵 Pembayaran pertama - Rp", min_value=0.0, value=1000000.0, step=100000.0, key="grow_R")
            i = st.number_input("📈 Tingkat bunga per periode (%)", min_value=0.0, value=10.0, step=0.5, key="grow_i") / 100
        with col2:
            g = st.number_input("📊 Tingkat pertumbuhan (%)", min_value=0.0, value=5.0, step=0.5, key="grow_g") / 100
            n = st.number_input("⏰ Jumlah periode", min_value=1, value=5, step=1, key="grow_n")
        
        if st.button("🧮 Hitung Growing Annuity", key="btn_grow", use_container_width=True):
            if i == g:
                PV = R1 * n / (1 + i)
            else:
                PV = R1 * (1 - ((1 + g) / (1 + i)) ** n) / (i - g)
            
            total_pembayaran = sum([R1 * (1 + g) ** k for k in range(n)])
            
            st.markdown(f"""
            <div class="result-box">
                <p>📌 <b>Nilai Sekarang:</b> Rp {PV:,.0f}</p>
                <p>📌 <b>Total pembayaran (nominal):</b> Rp {total_pembayaran:,.0f}</p>
                <p>📌 <b>Selisih (bunga tersimpan):</b> Rp {total_pembayaran - PV:,.0f}</p>
                <p style="font-size: 0.9em; color: #666;">📝 <i>Pembayaran naik {g*100:.1f}% setiap periode</i></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Tampilkan skema pembayaran
            with st.expander("📋 Detail Skema Pembayaran"):
                for k in range(min(n, 10)):
                    pembayaran = R1 * (1 + g) ** k
                    st.write(f"Periode {k+1}: Rp {pembayaran:,.0f}")
                if n > 10:
                    st.write(f"... dan seterusnya hingga periode ke-{n}")
    
    with tab2:
        st.markdown("### ♾️ Anuitas Kontinyu")
        st.info("💡 **Rumus:** PV = R × (1 - e^(-δn)) / δ, dengan δ = ln(1+i)")
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            R = st.number_input("💰 Total pembayaran per tahun - Rp", min_value=0.0, value=1000000.0, step=100000.0, key="cont_R")
            i = st.number_input("📈 Tingkat bunga (%)", min_value=0.0, value=10.0, step=0.5, key="cont_i") / 100
        with col2:
            n = st.number_input("⏰ Jumlah tahun", min_value=1, value=5, step=1, key="cont_n")
        
        if st.button("🧮 Hitung Anuitas Kontinyu", key="btn_cont_ann", use_container_width=True):
            delta = math.log(1 + i)
            PV = R * (1 - math.exp(-delta * n)) / delta
            total_pembayaran = R * n
            
            st.markdown(f"""
            <div class="result-box">
                <p>📌 <b>Nilai Sekarang:</b> Rp {PV:,.0f}</p>
                <p>📌 <b>Total pembayaran (nominal):</b> Rp {total_pembayaran:,.0f}</p>
                <p>📌 <b>Selisih (bunga tersimpan):</b> Rp {total_pembayaran - PV:,.0f}</p>
                <p style="font-size: 0.9em; color: #666;">📝 <i>Pembayaran dilakukan secara kontinyu (setiap saat)</i></p>
            </div>
            """, unsafe_allow_html=True)


def kelompok_probabilitas():
    st.subheader("📊 PROBABILITAS AKTUARIA")
    st.markdown("### *✨ Perusahaan asuransi jiwa, dana pensiun, perencanaan keuangan pribadi*")
    
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("← Kembali ke Menu", key="back_prob", use_container_width=True):
            st.session_state.page = "menu"
            st.rerun()
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📊 Survival & Force of Mortality", "🎲 Probabilitas Hidup/Mati", "💚 Harapan Hidup"])
    
    with tab1:
        st.markdown("### 📊 Survival & Force of Mortality")
        st.info("💡 **Model:** S(x) = e^(-0.01x) (constant force)")
        
        x = st.number_input("🎂 Masukkan usia x", min_value=0.0, max_value=100.0, value=30.0, step=1.0, key="surv_x")
        
        if st.button("🧮 Hitung", key="btn_surv", use_container_width=True):
            S = math.exp(-0.01 * x)
            mu = 0.01
            st.markdown(f"""
            <div class="result-box">
                <p>📌 <b>S({x:.0f})</b> (Probabilitas hidup sampai usia {x:.0f}): <b>{S:.4f}</b> ({S*100:.2f}%)</p>
                <p>📌 <b>μ({x:.0f})</b> (Force of Mortality): <b>{mu:.4f}</b> ({mu*100:.2f}% per tahun)</p>
                <p style="font-size: 0.9em; color: #666;">📝 <i>Model dengan tingkat kematian konstan 1% per tahun</i></p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🎲 Probabilitas Hidup/Mati")
        st.info("💡 **Asumsi:** lx = 100000 - 1000×x (model linear sederhana)")
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            x = st.number_input("🎂 Usia sekarang", min_value=0, max_value=100, value=30, step=1, key="prob_x")
        with col2:
            t = st.number_input("⏰ Jangka waktu t tahun", min_value=1, max_value=70, value=10, step=1, key="prob_t")
        
        if st.button("🧮 Hitung Probabilitas", key="btn_prob", use_container_width=True):
            lx = max(0, 100000 - 1000 * x)
            lx_t = max(0, 100000 - 1000 * (x + t))
            tpx = lx_t / lx if lx > 0 else 0
            tqx = 1 - tpx
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="result-box">
                    <p>📌 <b>{t}p{x}</b> (hidup {t} tahun):</p>
                    <p style="font-size: 1.5rem; font-weight: bold;">{tpx:.4f}</p>
                    <p>({tpx*100:.2f}%)</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="result-box">
                    <p>📌 <b>{t}q{x}</b> (mati dalam {t} tahun):</p>
                    <p style="font-size: 1.5rem; font-weight: bold;">{tqx:.4f}</p>
                    <p>({tqx*100:.2f}%)</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Jumlah orang yang diperkirakan hidup
            if lx > 0:
                st.info(f"📊 **Interpretasi:** Dari {lx:,.0f} orang berusia {x} tahun, diperkirakan {lx_t:,.0f} orang akan hidup mencapai usia {x+t} tahun")
    
    with tab3:
        st.markdown("### 💚 Harapan Hidup")
        st.info("💡 **Asumsi:** lx = 100000 - 1000×x, maks usia 100")
        
        x = st.number_input("🎂 Usia sekarang", min_value=0, max_value=99, value=30, step=1, key="ex_x")
        
        if st.button("🧮 Hitung Harapan Hidup", key="btn_ex", use_container_width=True):
            ex = (100 - x) / 2
            sisa_tahun = 100 - x
            st.markdown(f"""
            <div class="result-box">
                <p>📌 <b>Harapan hidup e{x}:</b> {ex:.2f} tahun</p>
                <p>📌 <b>Sisa usia maksimal:</b> {sisa_tahun:.0f} tahun</p>
                <p style="font-size: 0.9em; color: #666;">📝 <i>Seseorang berusia {x} tahun diperkirakan akan hidup {ex:.1f} tahun lagi (hingga usia {x + ex:.1f} tahun)</i></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Progress bar visual
            st.progress(x / 100)
            st.caption(f"📊 Usia {x} tahun dari maksimal 100 tahun")


def kelompok_asuransi():
    st.subheader("🛡️ ASURANSI JIWA")
    st.markdown("### *✨ Perhitungan premi asuransi jiwa*")
    
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("← Kembali ke Menu", key="back_asuransi", use_container_width=True):
            st.session_state.page = "menu"
            st.rerun()
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Premi Berjangka", "♾️ Premi Seumur Hidup", "🎯 Premi Dwiguna", "⚡ Premi Kontinyu", "💰 Premi Tahunan"
    ])
    
    with tab1:
        st.markdown("### 📋 Premi Asuransi Berjangka")
        st.info("💡 **Asumsi:** qx = 0.01 (1% per tahun), bunga = 6%")
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            x = st.number_input("🎂 Usia tertanggung", min_value=0, max_value=90, value=30, step=1, key="term_x")
            n = st.number_input("📅 Jangka waktu (tahun)", min_value=1, max_value=50, value=10, step=1, key="term_n")
        with col2:
            manfaat = st.number_input("💰 Manfaat asuransi - Rp", min_value=0.0, value=100000000.0, step=10000000.0, key="term_manfaat")
        
        if st.button("🧮 Hitung Premi Berjangka", key="btn_term", use_container_width=True):
            i = 0.06
            q = 0.01
            v = 1 / (1 + i)
            A = 0
            for k in range(n):
                A += v ** (k + 1) * q * (1 - q) ** k
            premi = manfaat * A
            
            st.markdown(f"""
            <div class="result-box">
                <p>📌 <b>Premi bersih tunggal:</b> Rp {premi:,.0f}</p>
                <p>📌 <b>Persentase terhadap manfaat:</b> {(premi/manfaat)*100:.2f}%</p>
                <p style="font-size: 0.9em; color: #666;">📝 <i>Premi yang harus dibayar sekali untuk perlindungan {n} tahun</i></p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### ♾️ Premi Asuransi Seumur Hidup")
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            x = st.number_input("🎂 Usia tertanggung", min_value=0, max_value=90, value=30, step=1, key="whole_x")
        with col2:
            manfaat = st.number_input("💰 Manfaat asuransi - Rp", min_value=0.0, value=100000000.0, step=10000000.0, key="whole_manfaat")
        
        if st.button("🧮 Hitung Premi Seumur Hidup", key="btn_whole", use_container_width=True):
            i = 0.06
            q = 0.01
            v = 1 / (1 + i)
            A = 0
            for k in range(100 - x):
                A += v ** (k + 1) * q * (1 - q) ** k
            premi = manfaat * A
            
            st.markdown(f"""
            <div class="result-box">
                <p>📌 <b>Premi bersih tunggal:</b> Rp {premi:,.0f}</p>
                <p>📌 <b>Persentase terhadap manfaat:</b> {(premi/manfaat)*100:.2f}%</p>
                <p style="font-size: 0.9em; color: #666;">📝 <i>Premi yang dibayarkan sekali untuk perlindungan seumur hidup</i></p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🎯 Premi Asuransi Dwiguna (Endowment)")
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            x = st.number_input("🎂 Usia tertanggung", min_value=0, max_value=90, value=30, step=1, key="endow_x")
            n = st.number_input("📅 Jangka waktu (tahun)", min_value=1, max_value=50, value=10, step=1, key="endow_n")
        with col2:
            manfaat = st.number_input("💰 Manfaat asuransi - Rp", min_value=0.0, value=100000000.0, step=10000000.0, key="endow_manfaat")
        
        if st.button("🧮 Hitung Premi Dwiguna", key="btn_endow", use_container_width=True):
            i = 0.06
            q = 0.01
            v = 1 / (1 + i)
            A_term = 0
            for k in range(n):
                A_term += v ** (k + 1) * q * (1 - q) ** k
            npx = (1 - q) ** n
            A_endow = v ** n * npx
            A_total = A_term + A_endow
            premi = manfaat * A_total
            
            st.markdown(f"""
            <div class="result-box">
                <p>📌 <b>Premi bersih tunggal:</b> Rp {premi:,.0f}</p>
                <p>📌 <b>Komponen risiko:</b> Rp {manfaat * A_term:,.0f}</p>
                <p>📌 <b>Komponen tabungan:</b> Rp {manfaat * A_endow:,.0f}</p>
                <p style="font-size: 0.9em; color: #666;">📝 <i>Premi untuk asuransi yang membayar jika meninggal ATAU hidup sampai {n} tahun</i></p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### ⚡ Premi Asuransi Kontinyu")
        st.info("💡 **Asumsi:** μ = 0.01 (constant force), δ = ln(1.06)")
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            manfaat = st.number_input("💰 Manfaat asuransi - Rp", min_value=0.0, value=100000000.0, step=10000000.0, key="cont_manfaat")
        with col2:
            n = st.number_input("📅 Jangka waktu (0 = seumur hidup)", min_value=0, value=10, step=1, key="cont_n")
        
        if st.button("🧮 Hitung Premi Kontinyu", key="btn_cont_prem", use_container_width=True):
            delta = math.log(1.06)
            mu = 0.01
            if n == 0:
                A_bar = mu / (mu + delta)
                periode = "seumur hidup"
            else:
                A_bar = mu / (mu + delta) * (1 - math.exp(-(mu + delta) * n))
                periode = f"{n} tahun"
            premi = manfaat * A_bar
            
            st.markdown(f"""
            <div class="result-box">
                <p>📌 <b>Premi bersih tunggal:</b> Rp {premi:,.0f}</p>
                <p>📌 <b>Persentase terhadap manfaat:</b> {(premi/manfaat)*100:.2f}%</p>
                <p style="font-size: 0.9em; color: #666;">📝 <i>Premi untuk perlindungan {periode} dengan pembayaran kontinyu</i></p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab5:
        st.markdown("### 💰 Premi Tahunan dari Premi Tunggal")
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            A = st.number_input("💰 Premi bersih tunggal - Rp", min_value=0.0, value=40000000.0, step=1000000.0, key="annual_A")
        with col2:
            a_double_dot = st.number_input("📊 Anuitas hidup due (ä)", min_value=1.0, value=10.0, step=0.5, key="annual_a")
        
        if st.button("🧮 Hitung Premi Tahunan", key="btn_annual", use_container_width=True):
            P = A / a_double_dot
            total_tahunan = P * a_double_dot
            
            st.markdown(f"""
            <div class="result-box">
                <p>📌 <b>Premi tahunan:</b> Rp {P:,.0f}</p>
                <p>📌 <b>Total pembayaran (selama ä tahun):</b> Rp {total_tahunan:,.0f}</p>
                <p style="font-size: 0.9em; color: #666;">📝 <i>Premi yang dibayarkan setiap tahun selama {a_double_dot:.1f} tahun</i></p>
            </div>
            """, unsafe_allow_html=True)


# ============================================================
# MENU UTAMA (DASHBOARD)
# ============================================================
def show_menu_utama():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #b85c1a;">📋 SILAHKAN PILIH MENU</h2>
        <p style="color: #d4752e;">Klik salah satu menu di bawah untuk memulai perhitungan</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Menampilkan menu dalam grid yang lebih menarik
    menus = [
        ("1", "📘", "Bunga & Nilai Waktu Uang", "Menghitung bunga sederhana, bunga majemuk, nilai akumulasi", "#"),
        ("2", "📙", "Nilai Sekarang & Diskonto", "Menghitung nilai uang masa depan jika dinilai sekarang", "#"),
        ("3", "📗", "Bunga Nominal & Kontinyu", "Menghitung bunga yang dihitung harian, bulanan, atau terus-menerus", "#"),
        ("4", "📕", "Persamaan Nilai & NPV", "NPV, IRR, pembayaran tunggal pengganti utang", "#"),
        ("5", "📔", "Anuitas", "Menghitung cicilan bulanan/tahunan yang sama besar", "#"),
        ("6", "📒", "Anuitas Khusus", "Menghitung cicilan yang naik tiap tahun (inflasi) atau terus-menerus", "#"),
        ("7", "📊", "Probabilitas Aktuaria", "Menghitung peluang hidup/mati seseorang dan harapan hidup", "#"),
        ("8", "🛡️", "Asuransi Jiwa", "Menghitung premi (iuran) asuransi jiwa yang harus dibayar", "#"),
    ]
    
    # Membuat grid 2x4
    for i in range(0, len(menus), 2):
        col1, col2 = st.columns(2, gap="large")
        
        # Kolom kiri
        with col1:
            menu_id, icon, title, desc, _ = menus[i]
            with st.container():
                st.markdown(f"""
                <div class="menu-card">
                    <div class="menu-icon">{icon}</div>
                    <div class="menu-title">{title}</div>
                    <div class="menu-desc">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"✨ {title}", key=f"menu_{menu_id}", use_container_width=True):
                    st.session_state.page = f"menu_{menu_id}"
                    st.rerun()
        
        # Kolom kanan
        if i + 1 < len(menus):
            with col2:
                menu_id, icon, title, desc, _ = menus[i + 1]
                with st.container():
                    st.markdown(f"""
                    <div class="menu-card">
                        <div class="menu-icon">{icon}</div>
                        <div class="menu-title">{title}</div>
                        <div class="menu-desc">{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"✨ {title}", key=f"menu_{menu_id}", use_container_width=True):
                        st.session_state.page = f"menu_{menu_id}"
                        st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Footer dengan informasi dan tips
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("""
        💡 **Tips Penggunaan:**
        - Klik menu di atas untuk memulai kalkulator
        - Gunakan tombol "← Kembali ke Menu" untuk kembali ke halaman utama
        - Setiap menu memiliki beberapa tab untuk berbagai jenis perhitungan
        """)
    
    st.markdown("---")
    
    # Animated footer
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <p style="color: #c45c1b; font-size: 0.9rem;">
            © 2026 Kalkulator Keuangan & Aktuaria | Made with ❤️ by Bunga_2310432026
        </p>
        <p style="color: #d4752e; font-size: 0.8rem; opacity: 0.8;">
            Solusi Cerdas untuk Perencanaan Keuangan Anda
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# MAIN PROGRAM
# ============================================================
def main():
    show_header()
    
    # Inisialisasi session state
    if "page" not in st.session_state:
        st.session_state.page = "menu"
    
    # Routing halaman
    if st.session_state.page == "menu":
        show_menu_utama()
    elif st.session_state.page == "menu_1":
        kelompok_bunga()
    elif st.session_state.page == "menu_2":
        kelompok_nilai_sekarang()
    elif st.session_state.page == "menu_3":
        kelompok_bunga_nominal()
    elif st.session_state.page == "menu_4":
        kelompok_persamaan_nilai()
    elif st.session_state.page == "menu_5":
        kelompok_anuitas()
    elif st.session_state.page == "menu_6":
        kelompok_anuitas_khusus()
    elif st.session_state.page == "menu_7":
        kelompok_probabilitas()
    elif st.session_state.page == "menu_8":
        kelompok_asuransi()


if __name__ == "__main__":
    main()
