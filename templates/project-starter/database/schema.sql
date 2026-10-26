-- Contoh skema sementara. Ganti dengan >= 2 entitas yang memiliki relasi.
CREATE TABLE IF NOT EXISTS kategori (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS item (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    kategori_id INT UNSIGNED NOT NULL,
    nama VARCHAR(150) NOT NULL,
    CONSTRAINT fk_item_kategori FOREIGN KEY (kategori_id) REFERENCES kategori(id)
);
