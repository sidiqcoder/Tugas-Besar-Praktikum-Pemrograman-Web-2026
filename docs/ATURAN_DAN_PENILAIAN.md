# Ketentuan Tugas Besar dan Penilaian

Dokumen pendamping README. Aturan yang bersifat administrasi (tanggal, penguji, sanksi final) harus ditetapkan melalui pengumuman pengelola.

## 1. Pelaksanaan

- Sebanyak 27 kelompok, setiap kelompok 5 mahasiswa.
- Tema: FEB, FH, FP, FKIP, FT, FISIP, FMIPA, FK; maks. 4 kelompok per tema.
- Pendaftaran tema melalui kanal resmi, bukan klaim pada PR.
- 1 kelompok membuat 1 aplikasi web yang selaras dengan tema, 1 folder repository, dan 1 PR utama.

## 2. Teknologi dan fitur

HTML5, CSS3, JavaScript vanilla, PHP native, dan MySQL/MariaDB. Framework aplikasi frontend/backend tidak diizinkan, sementara library UI ringan boleh. Minimal 2 entitas relasi DB, CRUD utama, proses khas tema, pencarian/filter/sort, validasi server-side, tampilan responsif, dan pengujian lokal. Session/login apabila fitur membutuhkannya.

## 3. Kolaborasi dan Git

- Ketua melakukan fork, mengundang anggota lain sebagai collaborator.
- Branch kelompok: `tubes/kelompok-XX`.
- Semua pekerjaan hanya di `kelompok/kelompok_XX/`.
- Setiap anggota memakai identitas GitHub sendiri, commit deskriptif, dan memahami kontribusinya.
- Target 3 commit bermakna per anggota disarankan, **bukan syarat otomatis untuk lulus CI**.
- Draft PR dibuat sejak awal, diubah menjadi Ready for review saat final.
- GitHub Actions dari PR fork mungkin membutuhkan persetujuan maintainer.
- Mahasiswa dilarang mengedit `.github`, `config`, `scripts`, folder kelompok lain, atau melakukan merge PR sendiri.

## 4. Dokumen wajib

`project.json`, `README.md`, `CONTRIBUTIONS.md`, `database/schema.sql`, `public/index.php`. Dokumentasi ERD, langkah instalasi, skenario demo dan screenshot juga wajib untuk penilaian (meski tidak semua dapat diverifikasi otomatis).

## 5. Deadline dan keterlambatan

**Deadline resmi: [DIISI PENGELOLA, tanggal/jam WIB].** PR harus Ready for review pada waktu tersebut. Pengelola mengarsipkan SHA commit penilaian sebelum tenggat. Perubahan sesudah tenggat dinilai hanya jika ada izin. Kegagalan CI karena infrastruktur milik pengelola tidak otomatis menjadi kesalahan mahasiswa.

## 6. Presentasi

Rekomendasi 15 menit/kelompok: 8 menit demo + 7 menit tanya jawab. Penguji boleh meminta tiap anggota menjelaskan alur data, code, database, validasi, dan hasil pekerjaannya. Mahasiswa sebaiknya menyiapkan dataset dummy yang tidak mengandung data pribadi.

## 7. Rubrik usulan

| Aspek | Bobot | Indikator |
|---|---:|---|
| Fungsionalitas | 30% | fitur utama, alur khas tema, keberhasilan demonstrasi |
| Backend & database | 20% | PHP native, struktur DB, query, relasi, CRUD |
| Kualitas kode & keamanan | 15% | validasi, penanganan error, sanitasi output, query terparameterisasi |
| UI/UX | 10% | navigasi, keterbacaan, responsivitas |
| Git & kolaborasi | 10% | riwayat pengembangan, kontribusi anggota, kepatuhan PR |
| Dokumentasi | 5% | README, ERD, instruksi instalasi, bukti pengerjaan |
| Presentasi & individu | 10% | demo serta pengetahuan setiap anggota |
| **Total** | **100%** | |

Rubrik bersifat rekomendasi dan dapat disahkan atau direvisi pengelola sebelum digunakan. Nilai kelompok dapat disesuaikan untuk individu berdasarkan kontribusi dan hasil wawancara.

## 8. Integritas akademik

Dilarang plagiarisme proyek, pemalsuan kontribusi, penyalahgunaan kode dari kelompok lain, memanipulasi CI, mengunggah kredensial atau data sensitif, atau mengganggu kerja kelompok lain. Penggunaan AI boleh sebagai bantuan jika kode dipahami. Pelanggaran diverifikasi sebelum pemberian sanksi berdasarkan aturan akademik kampus.
