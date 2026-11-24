# Logbook Tugas CPMK 3

Catatan mingguan kegiatan, kendala, dan keputusan. Tanggal diambil dari EXIF foto, `LOGBOOK.md` hasil
training di Kaggle, riwayat versi notebook Kaggle, dan riwayat commit repositori ini.
Bagian bertanda **[ISI]** belum dilengkapi.

---

## Minggu s.d. 15 November 2026

**Kegiatan**
- [ISI] Memilih 3 model dari 2 keluarga: YOLO11s-seg (one-stage CNN), Mask R-CNN R50-FPN v2 (two-stage CNN), Mask2Former Swin-T (transformer).
- [ISI] Menyusun notebook training (`CPMK3_training.ipynb`) dengan variabel NRP digit 3: fraksi data latih 25/50/100%.
- [ISI] Smoke test (`QUICK_TEST = True`, ±2 menit per run) untuk memastikan tidak ada error sebelum training penuh.

**Kendala / keputusan**
- [ISI] Batas waktu training ±0,66 jam per run supaya 9 run muat di sesi Kaggle.

---

## Minggu 16–22 November 2026

**Kegiatan**
- 18-11: training 9 run di Kaggle (GPU Tesla T4).
- 18-11, 21-11, 22-11: mengambil foto test custom (iPhone 11).

**Hipotesis**
- ± 18-11 (diucapkan lisan ke asisten AI saat training berjalan, **tidak ditulis sebelum training**; baru dicatat tertulis 24-11):
  *YOLO11s-seg akan menjadi model terbaik, karena hasil smoke test-nya paling bagus.*
- Hasil: **keliru**. Mask2Former terbaik, YOLO terendah di test asli. Penjelasan di laporan Bagian 3.1.

**Kendala / keputusan**
- 18-11 05:45, 07:27, 09:32: evaluasi test Mask2Former (fraksi 25/50/100%) gagal karena CUDA out of memory. Training tetap selesai dan bobot tersimpan.
  → Keputusan: post-processing diubah menjadi per 10 mask (output identik), dan test Mask2Former dihitung ulang di notebook evaluasi.

---

## Minggu 23–29 November 2026

**Kegiatan**
- 23-11: foto terakhir diambil, total 41 foto dengan 11 kondisi (`conditions.csv`).
- 23-11: anotasi di Roboflow (Auto-Label + Smart Polygon, lalu koreksi manual) dan export COCO.
- 23-11: pembersihan anotasi dengan `clean_custom.py` → 686 instance, 42 kelas.
- 24-11: notebook evaluasi (`CPMK3_eval_custom.ipynb`): domain shift, recall per kondisi, 5 foto gagal, analisis sensitivitas, eksperimen resolusi.
- 24-11: laporan Hasil & Analisis, notebook demo, repositori Git.

**Kendala / keputusan**
- Auto-label menghasilkan banyak serpihan (1.724 anotasi, contoh: 45 potongan untuk satu tangga).
  → Koreksi manual di Roboflow, lalu serpihan < 0,01% luas foto dibuang otomatis.
- Semua 41 foto tetap dipakai, tidak ada yang dibuang.
- Label kelas permukaan (dinding/lantai/plafon) tidak lengkap, dan namanya beda dengan dataset (`ceiling`, `wall`).
  → Dikeluarkan dari hasil utama, lalu diuji sebagai analisis sensitivitas dengan `ceiling` diganti `ceiling-merged` (Bagian 8).
- Notebook evaluasi awalnya tidak menemukan run Mask2Former, karena run hanya dicari dari file hasil test.
  → Run dicari juga dari file bobot.
- CI bootstrap percentile miring, karena AP pada sampel kecil bias ke atas.
  → Diganti basic bootstrap.
- Eksperimen resolusi run pertama cacat: foto sudah diperkecil ke 800 px, sehingga 1024/1280 hanya memperbesar foto.
  → Diulang dengan foto resolusi asli; versi 800 px dipakai sebagai pembanding.
- Mask R-CNN OOM pada foto resolusi asli di 1024/1280.
  → Dicoba versi per chunk (identik), tetapi tetap gagal di Kaggle. Diputuskan memakai hasil yang ada dan mencatatnya sebagai keterbatasan.
