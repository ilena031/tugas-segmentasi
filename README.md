# Tugas Evaluasi CPMK 3 — Instance Segmentation Indoor

Perbandingan **YOLO11s-seg**, **Mask R-CNN R50-FPN v2**, dan **Mask2Former Swin-T** pada
Roboflow Panoptic Indoor Segmentation v5, dengan variabel NRP **jumlah data latih (25/50/100%)**,
plus test set foto HP sendiri (41 foto, 11 kondisi) untuk analisis domain shift.

## Isi repositori

| File | Isi |
|---|---|
| `CPMK3_training.ipynb` | Training 9 run (3 model × 3 fraksi data), dijalankan di Kaggle (GPU T4) |
| `CPMK3_eval_custom.ipynb` | Evaluasi test custom: domain shift, recall per kondisi, analisis kegagalan, sensitivitas, eksperimen resolusi |
| `CPMK3_eval_custom_hasil_kaggle.ipynb` | Notebook evaluasi lengkap dengan output hasil run di Kaggle |
| `CPMK3_demo.ipynb` | Demo sesi tanya jawab: inferensi foto baru, ganti threshold, AP per kelas |
| `CPMK3_Hasil_dan_Analisis.docx` | Laporan hasil dan analisis |
| `conditions.csv` | Kondisi sulit tiap foto test custom |
| `test_custom_clean.json` | Anotasi test custom (COCO) setelah dibersihkan |
| `test_custom_surface_clean.json` | Varian anotasi dengan kelas dinding/lantai/plafon (analisis sensitivitas) |
| `clean_custom.py` | Skrip pembersihan anotasi export Roboflow |

Foto test custom tidak disertakan karena metadata EXIF-nya memuat lokasi GPS.

## Menjalankan
1. Kaggle: GPU T4, Internet On, Secret `ROBOFLOW_API_KEY`.
2. Jalankan `CPMK3_training.ipynb` (Save Version → Run All).
3. Untuk evaluasi/demo, tambahkan Output notebook training dan dataset test custom sebagai Input, lalu jalankan `CPMK3_eval_custom.ipynb` atau `CPMK3_demo.ipynb`.
