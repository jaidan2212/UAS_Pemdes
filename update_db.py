import sqlite3

conn = sqlite3.connect("laundry.db")
cursor = conn.cursor()

# Tambahkan kolom diskon jika belum ada
try:
    cursor.execute("ALTER TABLE transaksi ADD COLUMN diskon REAL")
    print("Kolom 'diskon' berhasil ditambahkan.")
except sqlite3.OperationalError:
    print("Kolom 'diskon' sudah ada.")

conn.commit()
conn.close()
