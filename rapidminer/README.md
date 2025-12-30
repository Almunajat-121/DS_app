# RapidMiner — Proses dan Data (Sultra)

Repository ini berisi berkas proses RapidMiner dan dataset yang digunakan untuk analisis ketimpangan pembangunan di Sulawesi Tenggara.

Isi folder
- `rapidMiner.rmp` — paket/proses RapidMiner (buka di RapidMiner Studio).
- `data_final_sultra.csv` — dataset utama (gunakan path relatif saat membuka proses).
- `Connections/` — konfigurasi koneksi (jika ada koneksi eksternal, periksa file di dalam folder ini).

Prasyarat
- RapidMiner Studio (disarankan versi terbaru).
- Java yang kompatibel (jika diperlukan oleh RapidMiner).

Menjalankan secara lokal (RapidMiner Studio)
1. Install RapidMiner Studio di mesin Anda.
2. Salin seluruh folder `rapidminer` ke satu lokasi di komputer.
3. Buka RapidMiner Studio → `File` → `Open Project` atau `Open Process` lalu pilih `rapidMiner.rmp`.
4. Pastikan operator yang memuat data menunjuk ke `data_final_sultra.csv` (gunakan path relatif atau update path ke file yang diunggah).
5. Jalankan proses (Run) dari RapidMiner Studio.

Catatan koneksi
- Jika proses memakai koneksi eksternal yang didefinisikan di folder `Connections/`, periksa konfigurasi tersebut dan sesuaikan kredensial atau host bila diperlukan.

Menjalankan/men-deploy di AI Studio (Altair)
Petunjuk ini bersifat umum karena fitur dan UI tiap platform dapat berbeda. Inti langkahnya adalah: upload file-data + proses, sesuaikan path, dan jalankan pada compute yang mendukung RapidMiner.

1. Buat project/experiment baru di AI Studio Altair.
2. Unggah seluruh isi folder `rapidminer/` (termasuk `data_final_sultra.csv` dan `rapidMiner.rmp`).
3. Periksa apakah platform menyediakan runtime yang dapat menjalankan RapidMiner Studio/Server:
   - Jika tersedia RapidMiner Server atau container yang mendukung RapidMiner, pilih resource tersebut dan jalankan proses.
   - Jika platform tidak mendukung RapidMiner langsung, opsi yang umum:
     - Jalankan RapidMiner pada mesin lokal atau VM, lalu gunakan AI Studio hanya untuk menyimpan/menampilkan artefak.
     - Konversi logika proses ke skrip Python/R dan jalankan di AI Studio (butuh pekerjaan manual).
4. Pastikan path data di dalam proses menggunakan path relatif (mis. `./data_final_sultra.csv`) atau perbarui path ke lokasi file hasil upload.
5. Atur resource (CPU/RAM) sesuai ukuran dataset dan kompleksitas proses.

Rekomendasi
- Bila proses memakan waktu, pertimbangkan mengekspor hasil model atau menyimpan model terlatih sehingga tidak perlu melatih ulang setiap kali.
- Simpan salinan `rapidMiner.rmp` yang telah di-adjust (mis. path data diperbarui) sebagai backup.

Troubleshooting
- Error file tidak ditemukan: periksa kembali path dataset pada operator pemuatan data.
- Jika AI Studio tidak mendukung RapidMiner, jalankan proses secara lokal di RapidMiner Studio lalu unggah hasil (CSV/artefak) ke AI Studio untuk analisis lebih lanjut.

Butuh bantuan menyesuaikan `rapidMiner.rmp` agar menggunakan path relatif atau membuat skrip konversi proses ke Python? Beritahu saya, saya bantu modifikasi.