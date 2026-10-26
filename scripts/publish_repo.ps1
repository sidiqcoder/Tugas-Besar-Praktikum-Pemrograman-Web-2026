# Jalankan dari root hasil ekstrak ZIP dengan PowerShell (Windows).
# Membutuhkan Git, GitHub CLI (gh), login `gh auth login`, dan izin Create Repository di organisasi.
$ErrorActionPreference = 'Stop'
$repoName = 'Praktikum-LabKom-TI-Unila/TUBES_PRK_PEMWEB_2026'

if (-not (Test-Path 'README.md') -or -not (Test-Path '.github/workflows/validate-pr.yml')) {
    throw 'Jalankan skrip dari root folder hasil ekstrak; README.md/.github belum ditemukan.'
}
if (-not (Get-Command git -ErrorAction SilentlyContinue) -or -not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw 'Git dan gh CLI wajib terpasang. Lihat docs/PANDUAN_ADMIN.md untuk cara manual.'
}
gh auth status
if ($LASTEXITCODE -ne 0) { throw 'Silakan jalankan: gh auth login' }

if (-not (Test-Path '.git')) {
    git init
    git switch -c main
    git add .
    git commit -m 'chore: initial repository template tugas besar pemweb 2026'
    if ($LASTEXITCODE -ne 0) { throw 'git commit gagal. Periksa git config user.name/user.email.' }
}
$existing = (gh repo view $repoName --json name --jq '.name' 2>$null)
if ($LASTEXITCODE -eq 0) {
    throw "Repository '$repoName' sudah ada; hentikan agar tidak menimpa repo existente. Gunakan panduan admin untuk push manual."
}
Write-Host "Membuat repository PUBLIC: $repoName"
gh repo create $repoName --public --source . --remote origin --push
if ($LASTEXITCODE -ne 0) { throw 'Gagal membuat repository. Pastikan punya izin pada organisasi.' }
Write-Host "Repository dibuat. Lanjutkan konfigurasi Rulesets/branch protection dan daftar tema sesuai docs/PANDUAN_ADMIN.md"
