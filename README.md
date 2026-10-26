<div align="center">

# 🎓 TUGAS BESAR PRAKTIKUM PEMROGRAMAN WEB 2026

**Laboratorium Komputer — Teknik Informatika, Universitas Lampung**

📚 PHP Native · MySQL/MariaDB · HTML · CSS · JavaScript Vanilla  
🔀 Fork → Branch → Pull Request → GitHub Actions → Review → Merge

</div>

> **Repositori pengumpulan resmi (setelah dipublikasikan oleh pengelola).** Setiap kelompok membuat satu aplikasi berbasis web sesuai **tema fakultas** yang telah didaftarkan. Kode dikumpulkan melalui **Fork dan Pull Request** ke branch `main`. Mahasiswa tidak mempunyai izin untuk merge sendiri.
>
> **PENTING:** Sebelum PR, pastikan kelompok sudah memperoleh alokasi tema dari asisten. Jika belum, CI akan menolak pengumpulan dengan pesan *kelompok belum diberi tema*.

[![Validasi Pull Request](https://img.shields.io/badge/CI-PHP%20lint%20%2B%20struktur-blue)](#-validasi-otomatis-ci) [![Metode](https://img.shields.io/badge/metode-fork%20%26%20pull%20request-0e776f)](#-cara-pengumpulan)

## 📌 Informasi utama

| Komponen | Ketentuan |
|---|---|
| Periode | Praktikum Pemrograman Web 2026 |
| Jumlah kelompok | **27 kelompok** |
| Anggota per kelompok | **5 mahasiswa** |
| Tema | **8 fakultas** |
| Kuota tema | **maks. 4 kelompok / fakultas** |
| Teknologi utama | HTML5, CSS3, JavaScript Vanilla, PHP Native, MySQL/MariaDB |
| Pengumpulan | **1 folder kelompok & 1 PR utama** |
| Repository tujuan | Repository ini, branch **`main`** |
| Deadline | **[AKAN DIUMUMKAN PENGELOLA]** (WIB) |
| Status pengumpulan | **Ready for review** dan pemeriksaan CI lulus |

---

## 🏛️ Pilihan tema fakultas

**Tema adalah ranah masalah, bukan nama aplikasi yang harus sama.** Kelompok boleh memilih contoh di bawah atau membuat ide lain yang tetap sesuai fakultas.

| Fakultas | Contoh kemungkinan website |
|---|---|
| **FEB** | Marketplace UMKM, sistem koperasi, manajemen keuangan, investasi edukatif, katalog bisnis |
| **FH** | Konsultasi hukum, informasi peraturan, pengaduan hukum, database kasus, edukasi hukum |
| **FP** | Marketplace hasil pertanian, manajemen kebun, informasi tanaman, agribisnis, peternakan |
| **FKIP** | E-learning, bank soal, kursus, media pembelajaran, manajemen sekolah |
| **FT** | Manajemen proyek, konstruksi, desain bangunan, inventaris alat, layanan teknik |
| **FISIP** | Portal berita, layanan masyarakat, survei sosial, organisasi, informasi pemerintahan |
| **FMIPA** | Database penelitian, laboratorium, katalog data, simulasi pembelajaran, informasi sains |
| **FK** | Informasi kesehatan, klinik, farmasi, edukasi kesehatan, jadwal layanan |

Setiap kelompok hanya memilih **1 tema**, sesuai daftar pendaftaran resmi. Keputusan tema dicatat admin di [`config/assignments.json`](config/assignments.json); **mahasiswa dilarang mengubah file itu**.

## ⚙️ Persyaratan aplikasi

Aplikasi wajib ditulis menggunakan **native**: HTML5, CSS3, JavaScript tanpa framework aplikasi, PHP tanpa framework backend, dan MySQL/MariaDB. Bootstrap, pustaka ikon, dan pustaka antarmuka ringan boleh digunakan asalkan logika inti tetap native. **Dilarang** menggunakan Laravel, CodeIgniter, React, Vue, Next.js, atau aplikasi/template jadi yang hanya diganti tampilannya.

Fitur minimum yang harus ada:

1. Halaman utama, navigasi jelas, dan responsif.
2. Minimal **dua entitas database berelasi**.
3. CRUD untuk data utama sesuai tema.
4. Minimal satu alur penggunaan khas tema (misalnya pemesanan, peminjaman, pendaftaran, atau pengaduan).
5. Pencarian, filter, atau pengurutan.
6. Validasi input di **server**, dengan pesan kesalahan yang jelas.
7. Autentikasi/session jika aplikasi memiliki peran pengguna khusus.
8. Data disimpan ke MySQL/MariaDB (bukan sekadar tampilan statis).
9. Dapat dijalankan dan didemonstrasikan secara lokal.

**REST API** dapat menjadi nilai tambah atau kewajiban terpisah apabila diumumkan oleh pengelola. Passing CI **tidak** berarti fitur sudah benar atau mendapat nilai penuh.

## 📂 Struktur repository

```text
TUBES_PRK_PEMWEB_2026/
├── .github/
│   ├── workflows/
│   │   ├── validate-pr.yml       # CI saat Pull Request
│   │   ├── main-ci.yml           # periksa konfigurasi main
│   │   └── delivery-on-merge.yml # paket ZIP setelah merge
│   └── PULL_REQUEST_TEMPLATE.md
├── config/
│   ├── themes.json              # 8 tema
│   └── assignments.json         # pengalokasian 27 kelompok (admin)
├── kelompok/
│   ├── .gitkeep
│   ├── kelompok_01/             # dibuat oleh kelompok 01
│   ├── kelompok_02/             # dibuat oleh kelompok 02
│   └── ...
│       └── kelompok_27/
├── templates/project-starter/    # contoh struktur, bukan jawaban jadi
├── scripts/                     # validator/admin tools, tidak boleh diubah mahasiswa
├── tests/                       # unit tests pengelola
├── docs/
│   ├── ATURAN_DAN_PENILAIAN.md
│   ├── PANDUAN_ADMIN.md
│   └── FAQ.md
└── README.md
```

**Contoh folder untuk kelompok 12 (tema FKIP):**

```text
kelompok/kelompok_12/
├── project.json           # identitas kelompok, fakultas, judul, 5 anggota
├── README.md              # dokumentasi aplikasi
├── CONTRIBUTIONS.md       # kontribusi nyata anggota
├── public/
│   ├── index.php
│   └── assets/
├── database/
│   ├── schema.sql
│   └── seed.sql
├── config/
│   └── .env.example       # boleh: contoh variabel tanpa password asli
└── docs/
    └── ERD.md
```

**Nama folder wajib:** `kelompok/kelompok_XX/` dengan **dua digit**: `kelompok_01`, `kelompok_12`, `kelompok_27`. **Jangan buat folder berdasarkan nama fakultas di level luar folder kelompok.** Fakultas sudah dicatat di `project.json` dan diverifikasi melalui manifest.

## 🚀 Cara pengumpulan

### 1. Daftar kelompok dan tema

Periksa daftar resmi dari asisten; pastikan **nomor kelompok dan tema telah terdaftar**. Tidak perlu mengubah file `config/assignments.json` sendiri.

### 2. Fork repo utama

Buka repository resmi 2026 milik [Praktikum-LabKom-TI-Unila](https://github.com/Praktikum-LabKom-TI-Unila) (tautannya diumumkan pengelola), klik **Fork** → *Create a new fork*. Ketua membuat fork lalu mengundang empat anggota menjadi collaborator.

### 3. Clone fork & buat branch

Ganti `<USERNAME>` dengan akun pemilik fork:

```bash
git clone https://github.com/<USERNAME>/TUBES_PRK_PEMWEB_2026.git
cd TUBES_PRK_PEMWEB_2026
git switch -c tubes/kelompok-12
```

Anggota berkontribusi menggunakan akun GitHub masing-masing. Jangan berbagi satu akun/credential GitHub.

### 4. Buat folder kelompok

Gunakan starter di `templates/project-starter/`, **salin** ke folder kelompok, jangan mengubah template di lokasi asalnya.

**Git Bash / macOS / Linux:**

```bash
cp -R templates/project-starter kelompok/kelompok_12
```

**PowerShell:**

```powershell
Copy-Item -Path "templates/project-starter" -Destination "kelompok/kelompok_12" -Recurse
```

Selanjutnya **wajib ubah** `kelompok/kelompok_12/project.json`:

```json
{
  "group": 12,
  "faculty": "FKIP",
  "title": "Bank Soal Interaktif",
  "members": [
    {"name": "Nama Mahasiswa A", "github": "akun-a"},
    {"name": "Nama Mahasiswa B", "github": "akun-b"},
    {"name": "Nama Mahasiswa C", "github": "akun-c"},
    {"name": "Nama Mahasiswa D", "github": "akun-d"},
    {"name": "Nama Mahasiswa E", "github": "akun-e"}
  ]
}
```

Contoh tersebut **bukan identitas asli**: ganti seluruh isinya. Nama dan username GitHub seluruh anggota harus berbeda. Nilai `faculty` wajib identik dengan hasil pendaftaran tema; nomor `group` adalah angka, bukan string.

### 5. Kembangkan aplikasi dan buat commit

Kerjakan **hanya** di `kelompok/kelompok_12/`. Perubahan di `.github/`, `scripts/`, `config/`, `README.md` root, atau folder kelompok lain akan membuat PR **gagal**.

```bash
git add kelompok/kelompok_12
git commit -m "feat: tambah modul CRUD bank soal"
git push -u origin tubes/kelompok-12
```

Lakukan commit secara bertahap dengan pesan bermakna. Kontribusi seluruh anggota dievaluasi dari pekerjaan nyata, bukan hanya banyaknya commit.

### 6. Buka Pull Request

Di GitHub fork, pilih **Contribute → Open pull request**. Periksa target:

- **Base repository:** repo resmi `Praktikum-LabKom-TI-Unila/TUBES_PRK_PEMWEB_2026` setelah diterbitkan.
- **Base branch:** `main`.
- **Head:** branch pada fork kelompok.

**Format judul PR:** `TUBES | K12 | FKIP | Bank Soal Interaktif`

Isi seluruh template PR, lampirkan screenshot, dan mula-mula buat **Draft PR** agar progres bisa dipantau. Setelah siap dan sebelum deadline, ubah menjadi **Ready for review**.

### 7. Pastikan CI hijau

Buka tab **Checks** pada PR. Jika muncul merah (*Failed*), buka log, perbaiki lewat commit di branch yang sama, lalu `git push` lagi. **Tidak perlu membuat PR baru.** `Pending` dapat berarti menunggu izin maintainer untuk menjalankan workflow fork.

### 8. Demonstrasi dan menunggu review

Asisten memeriksa fungsionalitas, keaslian kerja, kontribusi, dan presentasi. Mahasiswa **tidak melakukan merge**; setelah disetujui, maintainer yang menggabungkan PR.

## ✅ Validasi otomatis (CI)

Workflow `.github/workflows/validate-pr.yml` akan memeriksa:

| Pemeriksaan | Kondisi lulus |
|---|---|
| Folder & scope | PR hanya mengubah **1 folder** `kelompok/kelompok_XX/` |
| Nomor kelompok | 01–27 |
| Registrasi tema | Nomor kelompok dan tema terdaftar di manifest pengelola |
| Identitas | `project.json`: nomor, fakultas, judul, **5 anggota** valid |
| File wajib | `README.md`, `CONTRIBUTIONS.md`, `project.json`, `public/index.php`, `database/schema.sql` |
| Sintaks PHP | Seluruh file `.php` lolos `php -l` |
| Kebersihan file | Menolak `.env`, `vendor/`, `node_modules/`, symlink, file database lokal, kunci, arsip, file berukuran berlebihan |
| Isolasi konfigurasi | Mahasiswa tidak boleh mengedit CI, manifest, atau file pengelola |

**Batas CI:** Tidak menguji CRUD secara menyeluruh, kualitas desain, kebenaran SQL, keberadaan kerentanan logika bisnis, atau orisinalitas kode. Itu diperiksa melalui review dan demonstrasi. Validator dari **branch utama tepercaya**, tidak menjalankan program PHP kiriman mahasiswa; hanya memeriksa sintaks.

## 📦 CD setelah merge

Setelah asisten menyetujui dan melakukan merge, workflow `delivery-on-merge.yml` membuat **ZIP dari folder kelompok yang berubah** dan menyimpannya sebagai artifact pada GitHub Actions. Ini adalah **continuous delivery**, **bukan auto-deploy ke hosting publik**. Deployment ke server PHP/MySQL membutuhkan konfigurasi server, kredensial terlindungi, dan persetujuan pengelola.

## 🧑‍🤝‍🧑 Ketentuan kerja tim

- 1 kelompok = 5 mahasiswa = 1 aplikasi = 1 folder = 1 PR utama.
- Gunakan akun GitHub pribadi untuk commit; semua anggota wajib mengetahui bagian kode yang dikerjakan.
- Kelompok bertanggung jawab atas kualitas keseluruhan aplikasi.
- Framework aplikasi yang dilarang, copy-paste proyek utuh, perubahan folder lain, dan manipulasi CI merupakan pelanggaran.
- AI boleh untuk belajar dan membantu pengembangan **apabila kode dipahami dan dapat dijelaskan**.
- **Jangan** menyimpan password/token asli, data pasien asli, informasi pribadi pengguna, atau data sensitif lainnya.
- Commit sesudah deadline tidak dihitung tanpa persetujuan resmi pengelola.

Baca [Aturan lengkap dan rubrik](docs/ATURAN_DAN_PENILAIAN.md) serta [FAQ](docs/FAQ.md).

## 📅 Target enam pertemuan

| Pertemuan | Target |
|---|---|
| 1 | Registrasi tema, Fork, perancangan, Draft PR |
| 2 | ERD, schema SQL, struktur PHP |
| 3 | CRUD dan backend |
| 4 | Integrasi antarmuka dan database |
| 5 | Fitur selesai, debugging, CI lulus |
| 6 | Finalisasi, Ready for review, demonstrasi |

> Jadwal dan tenggat resmi diumumkan oleh asisten. Tabel adalah target kerja, bukan pengganti jadwal resmi.

## 🧮 Ringkasan penilaian

| Aspek | Bobot |
|---|---:|
| Fungsionalitas dan fitur | 30% |
| PHP native dan database | 20% |
| Validasi, keamanan, kualitas kode | 15% |
| UI/UX dan responsivitas | 10% |
| Git workflow dan kolaborasi | 10% |
| Dokumentasi | 5% |
| Presentasi dan pemahaman individu | 10% |
| **Total** | **100%** |

Rubrik ini adalah **usulan awal** sampai disahkan pengelola. Nilai akhir individu dapat berbeda menurut kontribusi dan wawancara.

## ❓ Bantuan

Jika CI gagal, baca log tab **Checks** dan [FAQ](docs/FAQ.md). Jika tidak tahu fakultas yang didaftarkan, hubungi asisten (jangan mengubah manifest). Untuk pertanyaan pengelolaan repository, lihat [Panduan admin](docs/PANDUAN_ADMIN.md).

---

**LabKom TI Unila · Praktikum Pemrograman Web 2026**  
Referensi mekanisme sebelumnya: [Tugas Besar Praktikum Pemweb 2025](https://github.com/Praktikum-LabKom-TI-Unila/TUBES_PRK_PEMWEB_2025).
