import sqlite3

def koneksi():
    conn = sqlite3.connect("laundry.db")
    return conn

def init_db():
    conn = koneksi()
    cursor = conn.cursor()

    #[NOMOR 1 & 2] PEMBUATAN TABEL DENGAN RELASI
    # Tabel Pelanggan (Primary Key)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pelanggan (
            id_pelanggan INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            alamat TEXT,
            no_hp TEXT
        )
    """)
    
    # Tabel Transaksi (Memiliki Foreign Key ke Pelanggan -> Relasi RDB)
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
    # ^^^ Perhatikan baris FOREIGN KEY di atas (Syarat Relasi RDB)

    # [NOMOR 1] PENGISIAN DATA OTOMATIS 
    cursor.execute("SELECT count(*) FROM pelanggan")
    if cursor.fetchone()[0] == 0:
        print("Mengisi data dummy pelanggan...")
        data_pelanggan = [
            ("Riel", "Kamal", "0819"),
            ("Idang", "Perum", "0812"),
            ("Harana", "Bangkalan", "0813"),
            ("Jeki", "Warga telang", "0814"),
            ("Perdi", "Warga telang", "0815"),
            ("Ijungg", "Penghuni talon", "0816"),
            ("Yoga animal", "Gg. UTM", "0817")
        ]
        cursor.executemany("INSERT INTO pelanggan (nama, alamat, no_hp) VALUES (?, ?, ?)", data_pelanggan)

    # Cek jika kosong, isi data dummy Transaksi
    cursor.execute("SELECT count(*) FROM transaksi")
    if cursor.fetchone()[0] == 0:
        print("Mengisi data dummy transaksi...")
        from datetime import datetime
        tgl = datetime.now().strftime("%Y-%m-%d")
        data_transaksi = [
            (1, tgl, "Cuci Kering", 2.5, 17500, 0, "Selesai"),
            (2, tgl, "Cuci Basah", 5.0, 30000, 0.1, "Proses"),
            (3, tgl, "Setrika", 1.0, 5000, 0, "Diambil"),
            (4, tgl, "Cuci & Setrika", 8.0, 64000, 0.15, "Baru"),
            (5, tgl, "Cuci Kering", 3.5, 24500, 0.1, "Selesai"),
            (6, tgl, "Setrika", 2.0, 10000, 0, "Baru"),
            (1, tgl, "Cuci Basah", 4.0, 24000, 0, "Proses")
        ]
        cursor.executemany("""
            INSERT INTO transaksi (id_pelanggan, tanggal, jenis_layanan, berat, total_harga, diskon, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, data_transaksi)

    conn.commit()
    conn.close()

# --- FUNGSI CRUD STANDAR ---
def insert_pelanggan(nama, alamat, no_hp):
    conn = koneksi()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pelanggan (nama, alamat, no_hp) VALUES (?, ?, ?)", (nama, alamat, no_hp))
    conn.commit()
    conn.close()

def update_pelanggan(id_pelanggan, nama, alamat, no_hp):
    conn = koneksi()
    cursor = conn.cursor()
    cursor.execute("UPDATE pelanggan SET nama = ?, alamat = ?, no_hp = ? WHERE id_pelanggan = ?", (nama, alamat, no_hp, id_pelanggan))
    conn.commit()
    conn.close()

def insert_transaksi(id_pelanggan, tanggal, jenis_layanan, berat, total_harga, diskon, status):
    conn = koneksi()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transaksi (id_pelanggan, tanggal, jenis_layanan, berat, total_harga, diskon, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (id_pelanggan, tanggal, jenis_layanan, berat, total_harga, diskon, status))
    conn.commit()
    conn.close()

def update_transaksi(id_transaksi, id_pelanggan, jenis_layanan, berat, total_harga, diskon, status):
    conn = koneksi()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE transaksi SET id_pelanggan = ?, jenis_layanan = ?, berat = ?, total_harga = ?, diskon = ?, status = ?
        WHERE id_transaksi = ?
    """, (id_pelanggan, jenis_layanan, berat, total_harga, diskon, status, id_transaksi))
    conn.commit()
    conn.close()

# --- FUNGSI PENDUKUNG FILTER & PAGINATION ---
def get_pelanggan_page(limit, offset, keyword_nama="", keyword_alamat=""):
    conn = koneksi()
    cursor = conn.cursor()
    query = "SELECT * FROM pelanggan WHERE nama LIKE ? AND alamat LIKE ? LIMIT ? OFFSET ?"
    cursor.execute(query, (f"%{keyword_nama}%", f"%{keyword_alamat}%", limit, offset))
    rows = cursor.fetchall()
    conn.close()
    return rows

def count_pelanggan(keyword_nama="", keyword_alamat=""):
    conn = koneksi()
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM pelanggan WHERE nama LIKE ? AND alamat LIKE ?"
    cursor.execute(query, (f"%{keyword_nama}%", f"%{keyword_alamat}%"))
    jumlah = cursor.fetchone()[0]
    conn.close()
    return jumlah

def get_transaksi_page(limit, offset, keyword_nama="", keyword_status=""):
    conn = koneksi()
    cursor = conn.cursor()
    # Join untuk mengambil Nama Pelanggan berdasarkan ID
    query = """
        SELECT t.id_transaksi, p.nama, t.tanggal, t.jenis_layanan, t.berat, t.total_harga, t.diskon, t.status
        FROM transaksi t
        JOIN pelanggan p ON t.id_pelanggan = p.id_pelanggan
        WHERE p.nama LIKE ? AND t.status LIKE ?
        LIMIT ? OFFSET ?
    """
    cursor.execute(query, (f"%{keyword_nama}%", f"%{keyword_status}%", limit, offset))
    rows = cursor.fetchall()
    conn.close()
    return rows

def count_transaksi(keyword_nama="", keyword_status=""):
    conn = koneksi()
    cursor = conn.cursor()
    query = """
        SELECT COUNT(*)
        FROM transaksi t
        JOIN pelanggan p ON t.id_pelanggan = p.id_pelanggan
        WHERE p.nama LIKE ? AND t.status LIKE ?
    """
    cursor.execute(query, (f"%{keyword_nama}%", f"%{keyword_status}%"))
    jumlah = cursor.fetchone()[0]
    conn.close()
    return jumlah