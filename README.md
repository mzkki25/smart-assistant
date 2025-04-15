# 🧠 Smart Knowledge Assistant - Setup Instructions

Website ini dirancang sebagai **Smart Knowledge Assistant** yang memiliki dua fitur utama:

1. **Image Captioning**  
   Pengguna dapat mengunggah gambar, dan sistem akan menghasilkan:
   - Deskripsi atau ringkasan (caption) dari isi gambar
   - Tag/kata kunci relevan yang diekstraksi dari caption

2. **Document Retrieval & Summarization (RAG-based)**  
   Dengan mengunggah file PDF, pengguna dapat mengajukan pertanyaan terkait isi dokumen. Sistem akan:
   - Melakukan ekstraksi dan pemrosesan isi PDF
   - Melakukan _retrieval_ konteks yang relevan berdasarkan pertanyaan
   - Memberikan jawaban atau ringkasan yang sesuai dengan isi dokumen, berbasis _prompt_ dari pengguna

Website ini menggabungkan teknologi **Image Captioning** dan **RAG (Retrieval-Augmented Generation)** untuk menyediakan asistensi cerdas berbasis konten visual dan dokumen teks.

----------------------

# Ikuti langkah-langkah di bawah ini untuk menjalankan proyek:

## 📦 Installation Guide

1. Clone repository ini ke dalam perangkat lokal Anda:
   git clone <repository-url>

2. Buat virtual environment (opsional tapi disarankan):
   - `python -m venv env`
   - `source env/bin/activate`        # (Linux/Mac)
   - `env\Scripts\activate`           # (Windows)

3. Install semua dependensi yang dibutuhkan:
   - `pip install -r requirements.txt`

4. Unduh model bahasa Inggris dari spaCy:
   - `python -m spacy download en_core_web_sm`

## 🚀 Menjalankan Aplikasi

5. Jalankan aplikasi menggunakan uvicorn:
   - `uvicorn main:app`

## 📬 (Opsional) Pengujian API

Jika ingin menguji API menggunakan request POST:

1. Masuk ke folder `test`
2. Buka terminal dan jalankan server:
   uvicorn main:app

3. Buka file `api_test.ipynb`, lalu jalankan cell secara berurutan untuk menguji endpoint

   *Pastikan file PDF atau gambar yang akan diuji telah tersedia di direktori yang sesuai.*

4. Alternatif lain:
   Unduh `Smart Assistant API Test.postman_collection.json`. Gunakan Postman dan sesuaikan URL dan route endpoint sesuai konfigurasi lokal Anda:
   - POST /upload_pdf
   - POST /ask
   - POST /upload_image

## 💡 Tips:
- Selalu pastikan server berjalan di `http://localhost:8000`
- Gunakan log dari terminal untuk mengetahui status server atau debug error yang muncul.

## 📂 Struktur Penting

- `main.py`         : Berisi seluruh route FastAPI
- `static/`         : Folder untuk file JS & CSS frontend
- `uploads/`        : Tempat menyimpan file PDF atau gambar yang diunggah
- `test/`           : Folder untuk pengujian API

Selamat menggunakan! 🔍📚