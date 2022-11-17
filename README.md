# Tugas Besar IF3130 Jaringan Komputer
> TCP-Like Go-Back-N

## Daftar Isi
* [Informasi Umum](#informasi-umum)
* [Teknologi yang Dipakai](#teknologi-yang-dipakai)
* [Fitur](#fitur)
* [Setup](#setup)
* [Daftar File](#daftar-file)
* [Penggunaan](#penggunaan)
* [Status Proyek](#status-proyek)
* [Ruang Perbaikan](#ruang-perbaikan)
* [Apresiasi](#apresiasi)
* [Kontak](#kontak)

## Informasi Umum
Program ini dibuat untuk memenuhi tugas Mata Kuliah IF3130 Jaringan Komputer

*Program Studi Teknik Informatika* <br />
*Sekolah Teknik Elektro dan Informatika* <br />
*Institut Teknologi Bandung* <br />

*Semester I Tahun 2022/2023*

Secara umum kami membuat sebuah sistem program yang terdiri dari server dan client yang berkomunikasi lewat jaringan. Konsepnya adalah TCP-Like Go-Back-N yang dilakukan menggunakan Python.

## Teknologi yang Dipakai
- Python - 3.9.8

## Fitur
Program ini memiliki sebuah fitur, yaitu:
- Melihat respon dari client dan server masing-masing saat mengirim segment

## Setup
- Persyaratan dasar
    - Install [Python](https://www.python.org/downloads/)
    - Unduh repository ini dalam bentuk .zip
    - Ekstrak zip ke lokasi yang diinginkan
- Cara Eksekusi Program
    - Jalankan program dengan wsl atau vm, masing-masing untuk client dan server

## Daftar File
- argparser.py
- client.py
- server.py
- connection.py
- segment.py
- Dan beberapa dokumen testing

## Penggunaan
1. Masuk ke terminal menggunakan wsl (atau bisa menggunakan VM)
2. jalankan pada dua terminal python3 client.py (client port) (server port) (nama file) dan python3 server.py (server port) (nama file)

## Status Proyek
_Proyek Selesai_

## Ruang Perbaikan
Terdapat hal-hal yang dapat dikembangkan dari proyek ini, diantaranya:
- Program yang lebih rapi

## Apresiasi
Kami sangat berterima kasih kepada
- semua orang yang mendukung proses pengerjaan

## Kontak
Dibuat oleh
- Nadia Mareta Putri Leiden 13520007
- Ken Kalang Al Qalyubi 13520010
- Taufan Fajarama Putrawansyah 13520031
