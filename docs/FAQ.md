# FAQ Mahasiswa

### Apakah boleh memakai Laravel, React, Vue, atau Next.js?
Tidak. Tugas ini memakai PHP native dan JavaScript vanilla. Bootstrap atau library UI ringan diperbolehkan jika diumumkan pengelola.

### Bagaimana jika ingin proyek dengan tema lain?
Pilih fakultas dengan kuota tersedia, lalu ajukan ide yang sesuai kepada asisten. Tema yang sah adalah yang tercatat di manifest pengelola.

### Kenapa PR merah "belum diberi tema"?
Asisten belum mengisi `config/assignments.json`. **Jangan edit file itu** pada fork; hubungi asisten agar mendaftarkan kelompok.

### Kenapa CI menolak README root?
Mahasiswa hanya boleh mengubah file di `kelompok/kelompok_XX/`. README root merupakan pedoman bersama, bukan README proyek kelompok.

### Bolehkah satu mahasiswa yang commit semua?
Aplikasi dapat berjalan, tetapi kontribusi individu sulit diverifikasi. Semua anggota wajib berkontribusi secara nyata dengan akunnya sendiri dan dapat menjelaskan kode yang dikerjakan.

### Apa yang dilakukan bila CI Failed?
Klik PR → Checks → `validate-submission` → lihat baris error. Perbaiki di branch kelompok dan push lagi. Tidak perlu membuat PR baru.

### Apakah Draft PR harus langsung hijau?
Tidak. Draft PR boleh belum lengkap dan karenanya gagal CI saat pengerjaan. Sebelum tenggat, lengkapkan berkas, pastikan hijau, lalu klik **Ready for review**.

### Mengapa PR pending atau workflow tidak jalan?
Pada fork/kontributor baru, GitHub dapat memerlukan approval maintainer sebelum menjalankan GitHub Actions. Hubungi pengelola, jangan membuat ulang PR secara berulang.

### Kenapa file `.env` tidak boleh dikumpulkan?
Karena dapat mengandung username/password. Simpan konfigurasi asli secara lokal; commit hanya `.env.example` dengan contoh tanpa rahasia.

### Apakah status hijau berarti sudah mendapat nilai penuh?
Tidak. CI hanya memeriksa aturan repository, metadata, berkas dasar, dan sintaks PHP. Fitur, database, keamanan, dan pemahaman tetap dinilai manual.

### Apakah GitHub Actions otomatis deploy semua aplikasi ke internet?
Tidak. Setelah merge, workflow CD mengemas folder menjadi ZIP di GitHub Actions. Pengelola yang menentukan hosting dan pengaturan DB bila memang ingin deployment.

### Apa format lokasi folder dan PR?
Folder: `kelompok/kelompok_XX/`. Judul PR: `TUBES | K12 | FKIP | Judul Aplikasi`. Angka dua digit berlaku pada **folder**; di `project.json` tulis integer `12`.
