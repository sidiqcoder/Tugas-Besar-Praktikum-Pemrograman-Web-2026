# Panduan Admin / Asisten Praktikum

## A. Buat repository utama di organisasi GitHub

1. Buat repo baru **`TUBES_PRK_PEMWEB_2026`** milik organisasi `Praktikum-LabKom-TI-Unila` (membutuhkan hak Create repository). Pilih **Public** supaya mahasiswa dapat Fork.
2. Upload seluruh **isi folder repository** ini termasuk direktori `.github/` dan dotfiles, dengan branch default **`main`**. Jangan meng-upload file ZIP sebagai satu berkas ke GitHub: ekstrak terlebih dahulu.
3. Aktifkan **Settings → Actions → General**: izinkan workflow yang diperlukan sesuai kebijakan organisasi. Pastikan permission workflow `read` cukup (semua workflow sudah memakai `contents: read`).
4. Pastikan **Forking** diperbolehkan oleh pengaturan repository/organisasi.
5. **Jangan** memasukkan password atau secret deploy ke workflow yang menangani `pull_request` dari fork.

### CLI untuk upload dari folder hasil ekstrak

```bash
cd TUBES_PRK_PEMWEB_2026
git init
git switch -c main
git add .
git commit -m "chore: initial template repository tugas besar 2026"
git remote add origin https://github.com/Praktikum-LabKom-TI-Unila/TUBES_PRK_PEMWEB_2026.git
git push -u origin main
```

**Alternatif PowerShell jika GitHub CLI sudah login:** jalankan `powershell -ExecutionPolicy Bypass -File scripts/publish_repo.ps1` dari root folder hasil ekstrak. Script ini akan membuat repo publik di organisasi, lalu push branch `main` (butuh izin membuat repository). Verifikasi isi script sebelum dijalankan.

Repository kosong **jangan** diinisialisasi dengan README baru di GitHub bila memakai `git push` di atas (hindari riwayat commit ganda). Bila akun/organisasi berbeda, ubah URL sesuai repository aktual.

## B. Registrasi 27 kelompok (WAJIB sebelum mahasiswa submit PR)

File `config/assignments.json` memuat 27 kelompok `01..27` dan fakultas `null` pada awalnya. Tentukan fakultas setiap kelompok **berdasarkan spreadsheet pendaftaran resmi** (tidak diasumsikan urut dari nomor kelompok). Kuota maksimal 4 kelompok/fakultas.

Contoh untuk memberi tema FKIP kepada kelompok 12:

```bash
python3 scripts/assign_group.py 12 FKIP
python3 scripts/validate_manifest.py
git add config/assignments.json
git commit -m "chore: assign kelompok 12 to FKIP"
git push origin main
```

Untuk mengganti tema yang sudah tercatat (setelah verifikasi administratif):

```bash
python3 scripts/assign_group.py 12 FH --force
```

Untuk mengosongkan tema: `python3 scripts/assign_group.py 12 NONE --force`.

File ini harus diedit oleh **admin di main**, bukan melalui PR mahasiswa. CI memeriksa alokasi tema dari **main yang tepercaya**. Jika belum ditetapkan, PR kelompok ditolak dengan pesan yang jelas.

## C. Pengaturan branch protection/ruleset

Setelah workflow dijalankan setidaknya sekali (agar status check tersedia):

- Settings → Rules → Rulesets atau Settings → Branches → Add branch protection.
- Target: branch `main`.
- Require a pull request before merging.
- Require status checks to pass: pilih job **`validate-submission`** dari workflow `Validate student PR`.
- Require approval (disarankan minimal 1 maintainer/asisten yang memiliki izin review).
- Block force pushes dan branch deletion.
- Batasi siapa yang boleh merge dan mengubah file kontrol.
- Jika tersedia, aktifkan opsi untuk mencegah bypass ruleset oleh pemilik akses non-admin.

**Catatan:** Nama konteks status check yang diwajibkan adalah `validate-submission` (job PR), **bukan** `config-check` (job push). Periksa nama yang ditampilkan pada PR pertama di repository aktual sebelum menyimpan ruleset. Ketersediaan dan penegakan fitur ruleset dapat bergantung paket/organisasi GitHub.

## D. Alur review

1. Verifikasi draft PR milik kelompok dan nomor foldernya.
2. Jika PR dari fork menunggu persetujuan Actions, **setujui hanya workflow yang memang boleh berjalan**.
3. Tunggu job `validate-submission` hijau. Jika gagal, arahkan mahasiswa membuka log dan memperbaiki PR yang sama.
4. Uji CRUD, hubungan database, validasi backend, desain, keaslian, dan kontribusi individu.
5. Arsipkan SHA commit saat deadline untuk bukti penilaian; tetapkan kebijakan keterlambatan secara resmi.
6. Setelah verifikasi, reviewer menyetujui dan **maintainer** melakukan merge.
7. Pada `main`, workflow `delivery-on-merge.yml` akan membuat `kelompok_XX.zip` sebagai GitHub Actions artifact (retensi 90 hari).

## E. Keamanan GitHub Actions

Workflow PR dengan sengaja **tidak** memakai `pull_request_target`, token write, atau secret deployment. Kode validator/unit test diambil dari `main` dan **bukan** dari PR. Checkout PR dianggap tidak tepercaya. Script PHP mahasiswa **tidak dijalankan**, hanya `php -l` untuk pemeriksaan sintaks. Ini tidak menggantikan review keamanan, pemindai secret, atau review manual sebelum deployment.

Jangan menambahkan perintah `composer install`, `npm install`, `php index.php`, SQL import, atau script mahasiswa pada runner PR kecuali sistemnya telah diisolasi dan ditinjau dari sisi keamanan.

## F. Pengujian lokal

```bash
python3 scripts/validate_manifest.py
python3 -m unittest discover -s tests -v
```

Test suite membuat git repo sementara dan mencakup tes validasi PR positif/negatif, batas 4 slot per fakultas, konfigurasi, larangan file rahasia/symlink, dan pemeriksaan sintaks PHP. Untuk menjalankan semua tes lokal, pasang Git, Python 3.10+, dan PHP CLI.

## G. Deployment opsional

Workflow CD saat ini hanya mengemas artefak; tidak deploy ke server sungguhan karena alamat server, akses SSH, PHP runtime, database tiap kelompok, domain/subdomain, dan kebijakan backup belum tersedia. Jika di masa depan ingin deploy, implementasikan **workflow baru yang berjalan setelah merge dan membutuhkan environment approval**, dengan isolasi proyek dan database per kelompok, penyimpanan secret di environment GitHub, serta pemeriksaan keamanan khusus. Jangan men-deploy program dari PR mahasiswa langsung ke server bersama.

## H. Hal wajib disesuaikan sebelum publikasi

- [ ] Repository telah diterbitkan, URL nyata sudah bisa diakses.
- [ ] Semua 27 kelompok dan pilihan tema valid menurut pendaftaran.
- [ ] Deadline tanggal/jam WIB sudah diumumkan di README dan dokumen aturan.
- [ ] Rubrik penilaian sudah disahkan / direvisi.
- [ ] Ketua kelompok mengetahui akun yang dipakai untuk Fork.
- [ ] Ruleset `main` dan status check valid setelah PR uji coba.
- [ ] Maintainer telah menguji satu PR positif dan satu PR negatif di GitHub.
- [ ] Kebijakan approval Actions untuk fork telah diuji.
- [ ] Tidak ada kredensial nyata di history repo.
