<?php
declare(strict_types=1);
$title = 'Starter Tugas Besar Pemweb';
?>
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title><?= htmlspecialchars($title, ENT_QUOTES, 'UTF-8') ?></title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <main class="card">
    <p class="eyebrow">Praktikum Pemrograman Web</p>
    <h1><?= htmlspecialchars($title, ENT_QUOTES, 'UTF-8') ?></h1>
    <p>Starter awal. Ganti dengan aplikasi PHP native sesuai fakultas dan fitur tugas besar.</p>
    <a href="https://www.php.net/manual/en/" rel="noopener noreferrer">Dokumentasi PHP</a>
  </main>
</body>
</html>
