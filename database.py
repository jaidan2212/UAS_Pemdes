import sqlite3

def koneksi():
    conn = sqlite3.connect("laundry.db")
    return conn

def insert_pelanggan(nama, alamat, no_hp):
    conn = koneksi()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pelanggan (nama, alamat, no_hp) VALUES (?, ?, ?)", (nama, alamat, no_hp))
    conn.commit()
    conn.close()

def get_pelanggan():
    conn = koneksi()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pelanggan")
    rows = cursor.fetchall()
    conn.close()
    return rows

def insert_transaksi(id_pelanggan, tanggal, jenis_layanan, berat, total_harga, status):
    conn = koneksi()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transaksi (id_pelanggan, tanggal, jenis_layanan, berat, total_harga, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_pelanggan, tanggal, jenis_layanan, berat, total_harga, status))
    conn.commit()
    conn.close()

def get_transaksi():
    conn = koneksi()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.id_transaksi, p.nama, t.tanggal, t.jenis_layanan, t.berat, t.total_harga, t.status
        FROM transaksi t
        JOIN pelanggan p ON t.id_pelanggan = p.id_pelanggan
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows
