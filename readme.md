# Hand Gesture Game Controller

Program ini memungkinkan Anda untuk mengontrol game Subway Surfers (atau game lain yang menggunakan tombol panah) menggunakan gestur tangan melalui webcam.

## Cara Kerja

Program menggunakan komputer vision untuk mendeteksi gestur tangan dan menerjemahkannya menjadi input keyboard sesuai pemetaan berikut:

* Gestur angka 1 (jari telunjuk saja) → tombol panah KIRI
* Gestur angka 2 (jari telunjuk dan tengah) → tombol panah KANAN
* Gestur tangan mengepal → tombol panah BAWAH
* Gestur tangan terbuka (semua jari) → tombol panah ATAS

## Persyaratan Sistem

* Python 3.6 atau lebih baru
* Webcam yang berfungsi
* Koneksi internet (untuk instalasi awal library)

## Persiapan dan Instalasi

1. **Clone atau download** kode program ini ke komputer Anda.

2. **Instal library yang diperlukan** menggunakan pip:
   ```
   pip install opencv-python mediapipe numpy pynput
   ```
   
   Jika Anda menggunakan lingkungan virtual atau kondisional, aktifkan terlebih dahulu:
   ```
   # Conda
   conda activate [nama_environment]
   pip install opencv-python mediapipe numpy pynput
   
   # Virtualenv
   source [path_to_venv]/bin/activate  # Linux/Mac
   [path_to_venv]\Scripts\activate     # Windows
   pip install opencv-python mediapipe numpy pynput
   ```

3. **Simpan kode** ke file bernama `hand_gesture_controller.py` (atau nama lain yang Anda inginkan).

## Cara Menjalankan

1. **Buka terminal atau command prompt**

2. **Navigasi ke direktori** tempat file program berada:
   ```
   cd path/to/program
   ```

3. **Jalankan program**:
   ```
   python hand_gesture_controller.py
   ```

4. **Buka game Subway Surfers** atau game lain yang ingin Anda kontrol dengan gestur tangan.

5. **Posisikan jendela game dan jendela webcam** sehingga keduanya terlihat.

6. **Mulai bermain** menggunakan gestur tangan sesuai pemetaan yang dijelaskan di atas.

## Panduan Gestur

* **Panah KIRI**: Tunjukkan satu jari (jari telunjuk) ke webcam
* **Panah KANAN**: Tunjukkan dua jari (jari telunjuk dan tengah) ke webcam
* **Panah BAWAH**: Kepalkan tangan Anda
* **Panah ATAS**: Buka semua jari tangan Anda

## Tips Penggunaan

* Pastikan tangan Anda terlihat jelas di webcam
* Pencahayaan yang cukup akan meningkatkan akurasi deteksi
* Gunakan latar belakang yang kontras dengan warna kulit Anda
* Sesuaikan posisi webcam untuk mendapatkan sudut terbaik untuk deteksi
* Jaga jarak ±50-60 cm dari webcam untuk hasil terbaik
* Hindari gerakan terlalu cepat untuk deteksi yang lebih akurat

## Cara Keluar Program

Tekan tombol `ESC` pada keyboard saat jendela webcam aktif untuk menutup program.

## Pemecahan Masalah

* **Webcam tidak terdeteksi**: Periksa koneksi webcam dan pastikan tidak digunakan oleh aplikasi lain
* **Gestur tidak dikenali**: Perbaiki pencahayaan dan pastikan tangan terlihat jelas di kamera
* **Program lambat**: Tutup aplikasi lain yang berjalan untuk menghemat sumber daya
* **Program crash**: Pastikan semua library terinstal dengan benar dan versi Python kompatibel

## Penyesuaian

Jika Anda ingin mengubah pemetaan gestur atau sensitivitas deteksi, buka file program dan ubah fungsi `detect_gesture()` atau parameter pada inisialisasi `hands = mp_hands.Hands()`.