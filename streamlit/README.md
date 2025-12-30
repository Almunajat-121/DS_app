# Sultra Analytics - Dashboard Ketimpangan Pembangunan

Proyek ini adalah sebuah aplikasi dashboard interaktif berbasis Streamlit yang menampilkan peta ketimpangan pembangunan dan tipologi wilayah di Provinsi Sulawesi Tenggara. Aplikasi melakukan pra-pemrosesan data, pemodelan klastering (K-Means), dan menyajikan visualisasi untuk analisis multidimensi (IPM, PDRB, kemiskinan, akses internet, dll.).

## Isi Repository
- `app.py` - Kode utama aplikasi Streamlit untuk visualisasi dan pemodelan.
- `data_final_sultra.csv` - Dataset yang digunakan (harus ditempatkan di folder yang sama).
- `rapidMiner.rmp` - Proses RapidMiner (opsional).
- `README.md` - (Anda melihat ini)
- `requirements.txt` - Daftar dependensi Python.

## Prasyarat
- Python 3.8+ direkomendasikan
- File `data_final_sultra.csv` harus ada di direktori proyek (satu folder dengan `app.py`).

## Instalasi
1. (Opsional) Buat dan aktifkan virtual environment:

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate
```

2. Install dependensi:

```bash
pip install -r requirements.txt
```

## Menjalankan Aplikasi
Jalankan perintah berikut di root proyek:

```bash
streamlit run app.py
```

Akses aplikasi pada alamat yang diberikan oleh Streamlit (biasanya `http://localhost:8501`).

## Cara Menggunakan Aplikasi
- Sidebar:
	- `Prediksi Wilayah Baru`: Masukkan nilai PDRB, persentase kemiskinan, IPM, dan akses internet untuk memprediksi klaster tipologi wilayah.
	- `Filter Data`: Pilih Kabupaten/Kota untuk memfilter visualisasi.
- Tab Utama:
	1. Ketimpangan Multidimensi: Heatmap yang menampilkan nilai asli indikator (angka) dan warna untuk performa relatif.
	2. Infrastruktur: Korelasi antara layanan publik (mis. akses internet, sanitasi) dan kemiskinan.
	3. Ekonomi & Daya Beli: Bubble chart PDRB vs Kemiskinan.
	4. Gender Gap: Visualisasi perbandingan IPM laki-laki vs perempuan.
	5. Modeling (Clustering): Hasil K-Means dan ringkasan statistik klaster.

## Catatan
- Jika aplikasi menampilkan error terkait file `data_final_sultra.csv`, pastikan file tersebut berada di direktori yang sama dengan `app.py`.
- Model K-Means dilatih saat aplikasi dijalankan; jika dataset besar, proses dapat memakan waktu.

## Kontak
Jika butuh bantuan atau ingin mengembangkan fitur tambahan, beri tahu saya.