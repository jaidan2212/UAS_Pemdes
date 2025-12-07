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

def insert_transaksi(id_pelanggan, tanggal, jenis_layanan, berat, total_harga, diskon, status):
    conn = koneksi()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transaksi (id_pelanggan, tanggal, jenis_layanan, berat, total_harga, diskon, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (id_pelanggan, tanggal, jenis_layanan, berat, total_harga, diskon, status))
    conn.commit()
    conn.close()

def get_transaksi():
    conn = koneksi()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.id_transaksi, p.nama, t.tanggal, t.jenis_layanan, t.berat, t.total_harga, t.diskon, t.status
        FROM transaksi t
        JOIN pelanggan p ON t.id_pelanggan = p.id_pelanggan
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_pelanggan(id_pelanggan, nama, alamat, no_hp):
    conn = koneksi()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE pelanggan SET nama = ?, alamat = ?, no_hp = ? WHERE id_pelanggan = ?
    """, (nama, alamat, no_hp, id_pelanggan))
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

def delete_pelanggan(id_pelanggan):
    conn = koneksi()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pelanggan WHERE id_pelanggan = ?", (id_pelanggan,))
    conn.commit()
    conn.close()

def delete_transaksi(id_transaksi):
    conn = koneksi()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transaksi WHERE id_transaksi = ?", (id_transaksi,))
    conn.commit()
    conn.close()