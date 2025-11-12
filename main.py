import tkinter as tk
from tkinter import ttk, messagebox
import database
from datetime import datetime

root = tk.Tk()
root.title("Aplikasi Laundry")
root.geometry("700x500")

frame_pelanggan = tk.LabelFrame(root, text="Data Pelanggan", padx=10, pady=10)
frame_pelanggan.pack(fill="x", padx=10, pady=5)

tk.Label(frame_pelanggan, text="Nama:").grid(row=0, column=0)
tk.Label(frame_pelanggan, text="Alamat:").grid(row=1, column=0)
tk.Label(frame_pelanggan, text="No HP:").grid(row=2, column=0)

entry_nama = tk.Entry(frame_pelanggan)
entry_alamat = tk.Entry(frame_pelanggan)
entry_hp = tk.Entry(frame_pelanggan)

entry_nama.grid(row=0, column=1)
entry_alamat.grid(row=1, column=1)
entry_hp.grid(row=2, column=1)

def simpan_pelanggan():
    nama = entry_nama.get()
    alamat = entry_alamat.get()
    hp = entry_hp.get()
    if nama:
        database.insert_pelanggan(nama, alamat, hp)
        messagebox.showinfo("Berhasil", "Data pelanggan disimpan!")
        tampil_pelanggan()
    else:
        messagebox.showwarning("Peringatan", "Nama harus diisi!")

tk.Button(frame_pelanggan, text="Simpan", command=simpan_pelanggan).grid(row=3, column=1, pady=5)

# === Tabel Pelanggan ===
tree_pelanggan = ttk.Treeview(root, columns=("ID", "Nama", "Alamat", "No HP"), show="headings")
tree_pelanggan.heading("ID", text="ID")
tree_pelanggan.heading("Nama", text="Nama")
tree_pelanggan.heading("Alamat", text="Alamat")
tree_pelanggan.heading("No HP", text="No HP")
tree_pelanggan.pack(fill="x", padx=10, pady=5)

def tampil_pelanggan():
    for row in tree_pelanggan.get_children():
        tree_pelanggan.delete(row)
    for row in database.get_pelanggan():
        tree_pelanggan.insert("", "end", values=row)

tampil_pelanggan()

frame_transaksi = tk.LabelFrame(root, text="Transaksi Laundry", padx=10, pady=10)
frame_transaksi.pack(fill="x", padx=10, pady=5)

tk.Label(frame_transaksi, text="ID Pelanggan:").grid(row=0, column=0)
tk.Label(frame_transaksi, text="Jenis Layanan:").grid(row=1, column=0)
tk.Label(frame_transaksi, text="Berat (kg):").grid(row=2, column=0)
tk.Label(frame_transaksi, text="Status:").grid(row=3, column=0)

entry_id_pelanggan = tk.Entry(frame_transaksi)
entry_jenis = tk.Entry(frame_transaksi)
entry_berat = tk.Entry(frame_transaksi)
entry_status = tk.Entry(frame_transaksi)

entry_id_pelanggan.grid(row=0, column=1)
entry_jenis.grid(row=1, column=1)
entry_berat.grid(row=2, column=1)
entry_status.grid(row=3, column=1)

def simpan_transaksi():
    id_pel = entry_id_pelanggan.get()
    jenis = entry_jenis.get()
    berat = float(entry_berat.get())
    status = entry_status.get()
    total = berat * 7000  # contoh harga/kg
    tanggal = datetime.now().strftime("%Y-%m-%d")
    database.insert_transaksi(id_pel, tanggal, jenis, berat, total, status)
    messagebox.showinfo("Berhasil", "Transaksi disimpan!")
    tampil_transaksi()

tk.Button(frame_transaksi, text="Simpan Transaksi", command=simpan_transaksi).grid(row=4, column=1, pady=5)

tree_transaksi = ttk.Treeview(root, columns=("ID", "Nama", "Tanggal", "Layanan", "Berat", "Total", "Status"), show="headings")
for col in ("ID", "Nama", "Tanggal", "Layanan", "Berat", "Total", "Status"):
    tree_transaksi.heading(col, text=col)
tree_transaksi.pack(fill="both", expand=True, padx=10, pady=5)

def tampil_transaksi():
    for row in tree_transaksi.get_children():
        tree_transaksi.delete(row)
    for row in database.get_transaksi():
        tree_transaksi.insert("", "end", values=row)

tampil_transaksi()

root.mainloop()
