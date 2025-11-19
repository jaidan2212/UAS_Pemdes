import sqlite3

conn = sqlite3.connect("laundry.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pelanggan (
    id_pelanggan INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    alamat TEXT,
    no_hp TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transaksi (
    id_transaksi INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pelanggan INTEGER,
    tanggal TEXT,
    jenis_layanan TEXT,
    berat REAL,
    total_harga REAL,
    diskon REAL,
    status TEXT,
    FOREIGN KEY(id_pelanggan) REFERENCES pelanggan(id_pelanggan)
)
""")

conn.commit()
conn.close()
print("Database laundry.db berhasil dibuat!")
