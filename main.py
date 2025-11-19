import tkinter as tk
from tkinter import ttk, messagebox
import database
from datetime import datetime

root = tk.Tk()
root.title("Aplikasi Laundry")
root.geometry("750x500")

# === Frame Pelanggan ===
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
for col in ("ID", "Nama", "Alamat", "No HP"):
    tree_pelanggan.heading(col, text=col)
tree_pelanggan.pack(fill="x", padx=10, pady=5)

def tampil_pelanggan():
    for row in tree_pelanggan.get_children():
        tree_pelanggan.delete(row)
    for row in database.get_pelanggan():
        tree_pelanggan.insert("", "end", values=row)

tampil_pelanggan()

# === Frame Transaksi ===
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

# === Fungsi Diskon ===
def hitung_total_dengan_diskon(berat, harga_per_kg=7000):
    total_awal = berat * harga_per_kg
    if berat >= 7:
        diskon = 0.15
    elif berat >= 3:
        diskon = 0.10
    else:
        diskon = 0.0
    total_akhir = total_awal * (1 - diskon)
    return total_akhir, diskon

def simpan_transaksi():
    try:
        id_pel = entry_id_pelanggan.get()
        jenis = entry_jenis.get()
        berat = float(entry_berat.get())
        status = entry_status.get()
        tanggal = datetime.now().strftime("%Y-%m-%d")

        total, diskon = hitung_total_dengan_diskon(berat)

        database.insert_transaksi(id_pel, tanggal, jenis, berat, total, diskon, status)

        messagebox.showinfo("Berhasil", f"Transaksi disimpan!\nDiskon: {int(diskon*100)}%\nTotal: Rp{int(total)}")
        tampil_transaksi()
    except ValueError:
        messagebox.showerror("Error", "Berat harus berupa angka!")

tk.Button(frame_transaksi, text="Simpan Transaksi", command=simpan_transaksi).grid(row=4, column=1, pady=5)

# === Tabel Transaksi ===
tree_transaksi = ttk.Treeview(root, columns=("ID", "Nama", "Tanggal", "Layanan", "Berat", "Total", "Diskon", "Status"), show="headings")
for col in ("ID", "Nama", "Tanggal", "Layanan", "Berat", "Total", "Diskon", "Status"):
    tree_transaksi.heading(col, text=col)
tree_transaksi.pack(fill="both", expand=True, padx=10, pady=5)

def tampil_transaksi():
    for row in tree_transaksi.get_children():
        tree_transaksi.delete(row)
    for row in database.get_transaksi():
        tree_transaksi.insert("", "end", values=row)

tampil_transaksi()

root.mainloop()
