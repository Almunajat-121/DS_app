import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# --- CONFIGURATION & STYLE ---
st.set_page_config(
    page_title="Sultra Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS: Tampilan bersih, font profesional, margin rapi
st.markdown("""
    <style>
        .block-container {padding-top: 1rem; padding-bottom: 1rem;}
        h1, h2, h3 {font-family: 'Segoe UI', sans-serif; color: #2c3e50;}
        .stMetric {background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
        .stButton>button {width: 100%; background-color: #2c3e50; color: white;}
        div[data-testid="stExpander"] div[role="button"] p {font-size: 1.1rem; font-weight: 600;}
    </style>
""", unsafe_allow_html=True)

# --- 1. GLOBAL DATA LOADING & MODEL TRAINING ---
@st.cache_data
def load_and_prep_model():
    try:
        df = pd.read_csv('data_final_sultra.csv')
    except:
        return None, None, None, None, None

    if 'ipm_total' not in df.columns:
        df['ipm_total'] = (df['ipm_l'] + df['ipm_p']) / 2
    
    # --- TRAINING MODEL (GLOBAL) ---
    features_model = ['pdrb_perkapita_jt', 'persen_miskin_pct', 'ipm_total', 'akses_internet_pct']
    df_clean = df.dropna(subset=features_model).copy()
    
    # Scaling & Modeling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_clean[features_model])
    
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df_clean['Cluster'] = kmeans.fit_predict(X_scaled)
    
    # Smart Labeling
    clus_profile = df_clean.groupby('Cluster')[['pdrb_perkapita_jt', 'ipm_total']].mean()
    cluster_kota = clus_profile['ipm_total'].idxmax()
    cluster_tambang = clus_profile['pdrb_perkapita_jt'].idxmax()
    
    if cluster_tambang == cluster_kota:
         clus_profile_temp = clus_profile.drop(cluster_kota)
         cluster_tambang = clus_profile_temp['pdrb_perkapita_jt'].idxmax()

    all_clusters = set(df_clean['Cluster'].unique())
    cluster_tertinggal = list(all_clusters - {cluster_kota, cluster_tambang})[0]
    
    mapping = {
        cluster_kota: 'Maju (Kota/Jasa)',
        cluster_tambang: 'Kaya SDA (Tambang)',
        cluster_tertinggal: 'Tertinggal (Kepulauan)'
    }
    
    df_clean['Label_Cluster'] = df_clean['Cluster'].map(mapping)
    
    return df_clean, scaler, kmeans, mapping, features_model

# Load Model
df, scaler, kmeans, mapping_labels, features_list = load_and_prep_model()

if df is None:
    st.error("ERROR: File 'data_final_sultra.csv' tidak ditemukan. Pastikan file ada di folder yang sama.")
    st.stop()

# --- 2. SIDEBAR ---
with st.sidebar:
    st.header("Kontrol Panel")
    
    # Fitur Prediksi
    with st.expander("🤖 Prediksi Wilayah Baru", expanded=True):
        st.write("Simulasi klaster untuk data baru:")
        in_pdrb = st.number_input("PDRB (Juta Rp)", min_value=0.0, value=35.0)
        in_miskin = st.number_input("Kemiskinan (%)", min_value=0.0, value=12.0)
        in_ipm = st.number_input("IPM Total", min_value=0.0, value=70.0)
        in_internet = st.number_input("Akses Internet (%)", min_value=0.0, value=60.0)
        
        if st.button("Cek Klaster"):
            input_data = np.array([[in_pdrb, in_miskin, in_ipm, in_internet]])
            input_scaled = scaler.transform(input_data)
            pred_cluster = kmeans.predict(input_scaled)[0]
            pred_label = mapping_labels[pred_cluster]
            
            st.markdown(f"**Hasil:** {pred_label}")
            if "Maju" in pred_label:
                st.success("Tipologi: Pusat Pertumbuhan")
            elif "Tambang" in pred_label:
                st.warning("Tipologi: Industri Ekstraktif")
            else:
                st.error("Tipologi: Prioritas Pembangunan")

    st.markdown("---")
    
    # Filter Wilayah
    st.subheader("Filter Data")
    selected_regions = st.multiselect(
        "Pilih Kabupaten/Kota:",
        options=df['Kabupaten/Kota'].unique(),
        default=df['Kabupaten/Kota'].unique()
    )

df_filtered = df[df['Kabupaten/Kota'].isin(selected_regions)]

# --- 3. MAIN DASHBOARD ---

st.title("Dashboard Ketimpangan Pembangunan (SDGs 10)")
st.markdown("##### Provinsi Sulawesi Tenggara")

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Wilayah Data", f"{len(df_filtered)}")
col2.metric("Rata-rata Kemiskinan", f"{df_filtered['persen_miskin_pct'].mean():.2f}%")
col3.metric("Rata-rata IPM", f"{df_filtered['ipm_total'].mean():.2f}")
col4.metric("Rata-rata PDRB", f"Rp {df_filtered['pdrb_perkapita_jt'].mean():.1f} Juta")

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Ketimpangan Multidimensi", 
    "Infrastruktur",
    "Ekonomi & Daya Beli",
    "Gender Gap",
    "Modeling (Clustering)"
])

# --- TAB 1: HEATMAP (REVISI: ANGKA DITAMPILKAN) ---
with tab1:
    st.subheader("Peta Ketimpangan Multidimensional")
    col_viz, col_txt = st.columns([3, 1])
    
    with col_viz:
        cols_dimensi = ['pdrb_perkapita_jt', 'ipm_l', 'ipm_p', 'akses_internet_pct', 'persen_miskin_pct']
        scaler_viz = MinMaxScaler()
        df_norm = df_filtered.copy()
        df_norm[cols_dimensi] = scaler_viz.fit_transform(df_filtered[cols_dimensi])
        df_norm['persen_miskin_pct'] = 1 - df_norm['persen_miskin_pct'] 

        fig, ax = plt.subplots(figsize=(10, 8)) # Ukuran sedikit diperbesar agar angka muat
        sns.heatmap(
            df_norm.set_index('Kabupaten/Kota')[cols_dimensi],
            annot=df_filtered.set_index('Kabupaten/Kota')[cols_dimensi], # INI DATA ASLINYA (ANGKA)
            fmt=".1f",       # Format 1 angka desimal
            cmap='RdYlGn',   # Warna Merah-Kuning-Hijau
            linewidths=0.5, 
            ax=ax,
            cbar_kws={'label': 'Skala Ternormalisasi (Warna)'}
        )
        plt.xlabel("")
        plt.ylabel("")
        st.pyplot(fig)
    
    with col_txt:
        st.info("**Panduan Membaca:**\n\n- **Angka:** Menunjukkan nilai asli indikator.\n- **Warna:** Menunjukkan performa relatif (Hijau=Baik, Merah=Buruk).\n\nPerhatikan bahwa IPM Kota Kendari (Hijau) jauh lebih tinggi dibanding Buton Selatan (Merah).")

# --- TAB 2: INFRASTRUKTUR ---
with tab2:
    st.subheader("Korelasi Layanan Publik & Kemiskinan")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Akses Internet vs Kemiskinan**")
        fig2a = plt.figure(figsize=(6, 4))
        sns.regplot(data=df_filtered, x='akses_internet_pct', y='persen_miskin_pct', 
                    scatter_kws={'color':'#27ae60'}, line_kws={'color':'#c0392b'})
        plt.xlabel("Akses Internet (%)")
        plt.ylabel("Kemiskinan (%)")
        st.pyplot(fig2a)
    with col_b:
        st.markdown("**Sanitasi Layak vs Kemiskinan**")
        fig2b = plt.figure(figsize=(6, 4))
        sns.regplot(data=df_filtered, x='akses_sanitasi_pct', y='persen_miskin_pct', 
                    scatter_kws={'color':'#2980b9'}, line_kws={'color':'#e67e22'})
        plt.xlabel("Sanitasi Layak (%)")
        plt.ylabel("")
        st.pyplot(fig2b)

# --- TAB 3: BUBBLE CHART ---
with tab3:
    st.subheader("Peta Variasi Pembangunan")
    fig3 = plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=df_filtered,
        x='pdrb_perkapita_jt', y='persen_miskin_pct',
        size=df_filtered['pengeluaran_rp']/1000, sizes=(50, 600),
        hue='Kabupaten/Kota', palette='tab20', legend=False, alpha=0.8
    )
    for i in range(len(df_filtered)):
         plt.text(
             df_filtered.iloc[i]['pdrb_perkapita_jt']+0.5,
             df_filtered.iloc[i]['persen_miskin_pct'], 
             df_filtered.iloc[i]['Kabupaten/Kota'], 
             fontsize=8, alpha=0.9
         )
    plt.axvline(x=df_filtered['pdrb_perkapita_jt'].mean(), color='red', linestyle='--', alpha=0.5)
    plt.axhline(y=df_filtered['persen_miskin_pct'].mean(), color='blue', linestyle='--', alpha=0.5)
    plt.xlabel("PDRB per Kapita (Juta Rp)")
    plt.ylabel("Kemiskinan (%)")
    plt.grid(True, linestyle='--', alpha=0.3)
    st.pyplot(fig3)

# --- TAB 4: GENDER ---
with tab4:
    st.subheader("Disparitas Gender (IPM)")
    df_sort = df_filtered.sort_values('ipm_l', ascending=False)
    fig4 = plt.figure(figsize=(10, 8))
    plt.hlines(y=df_sort['Kabupaten/Kota'], xmin=df_sort['ipm_p'], xmax=df_sort['ipm_l'], color='grey', alpha=0.4, linewidth=3)
    plt.scatter(df_sort['ipm_p'], df_sort['Kabupaten/Kota'], color='#e74c3c', label='Perempuan', s=80)
    plt.scatter(df_sort['ipm_l'], df_sort['Kabupaten/Kota'], color='#2c3e50', label='Laki-laki', s=80)
    plt.legend()
    plt.grid(axis='x', linestyle='--', alpha=0.3)
    plt.xlabel("Indeks Pembangunan Manusia")
    st.pyplot(fig4)

# --- TAB 5: CLUSTERING ---
with tab5:
    st.subheader("Hasil Pemodelan Klaster (K-Means)")
    col_chart, col_info = st.columns([3, 1])
    
    with col_chart:
        fig5 = plt.figure(figsize=(10, 6))
        sns.scatterplot(
            data=df_filtered, 
            x='pdrb_perkapita_jt', y='persen_miskin_pct', 
            hue='Label_Cluster', palette='viridis', 
            s=200, style='Label_Cluster', edgecolor='black'
        )
        for i in range(len(df_filtered)):
            plt.text(
                x=df_filtered.iloc[i]['pdrb_perkapita_jt'] + 1,
                y=df_filtered.iloc[i]['persen_miskin_pct'] + 0.2,
                s=df_filtered.iloc[i]['Kabupaten/Kota'],
                fontsize=9, weight='bold'
            )
        plt.xlabel("PDRB per Kapita (Juta Rp)")
        plt.ylabel("Kemiskinan (%)")
        plt.grid(True, linestyle='--', alpha=0.3)
        st.pyplot(fig5)
        
    with col_info:
        st.markdown("#### Legenda Klaster")
        st.info("""
        **1. Maju (Kota/Jasa)**
        IPM Tinggi, Kemiskinan Rendah.
        
        **2. Kaya SDA (Tambang)**
        PDRB Tinggi, Kemiskinan Sedang.
        
        **3. Tertinggal (Kepulauan)**
        PDRB Rendah, Kemiskinan Tinggi.
        """)

    st.markdown("---")
    st.subheader("Statistik Karakteristik Klaster")
    
    # GROUPBY TANPA RESET INDEX (Supaya Label jadi Index & tidak error saat format)
    profil = df_filtered.groupby('Label_Cluster')[features_list].mean()
    
    st.dataframe(
        profil.style.format("{:.2f}").background_gradient(cmap="Greens"),
        use_container_width=True
    )