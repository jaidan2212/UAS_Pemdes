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

def edit_pelanggan():
    selected = tree_pelanggan.focus()
    if not selected:
        messagebox.showwarning("Peringatan", "Pilih data pelanggan yang akan diedit!")
        return

    values = tree_pelanggan.item(selected, "values")
    id_pelanggan = values[0]
    nama_lama = values[1]
    alamat_lama = values[2]
    hp_lama = values[3]

    top = tk.Toplevel(root)
    top.title("Edit Pelanggan")

    tk.Label(top, text="Nama:").grid(row=0, column=0)
    tk.Label(top, text="Alamat:").grid(row=1, column=0)
    tk.Label(top, text="No HP:").grid(row=2, column=0)

    entry_nama_edit = tk.Entry(top)
    entry_alamat_edit = tk.Entry(top)
    entry_hp_edit = tk.Entry(top)

    entry_nama_edit.insert(0, nama_lama)
    entry_alamat_edit.insert(0, alamat_lama)
    entry_hp_edit.insert(0, hp_lama)

    entry_nama_edit.grid(row=0, column=1)
    entry_alamat_edit.grid(row=1, column=1)
    entry_hp_edit.grid(row=2, column=1)

    def simpan_edit():
        nama = entry_nama_edit.get()
        alamat = entry_alamat_edit.get()
        hp = entry_hp_edit.get()
        if nama:
            database.update_pelanggan(id_pelanggan, nama, alamat, hp)
            messagebox.showinfo("Berhasil", "Data pelanggan diperbarui!")
            top.destroy()
            tampil_pelanggan()
        else:
            messagebox.showwarning("Peringatan", "Nama tidak boleh kosong!")

    tk.Button(top, text="Simpan", command=simpan_edit).grid(row=3, column=1, pady=5)

tk.Button(frame_pelanggan, text="Simpan", command=simpan_pelanggan).grid(row=3, column=1, pady=5)
tk.Button(frame_pelanggan, text="Edit Pelanggan", command=edit_pelanggan).grid(row=4, column=1, pady=5)

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
# Opsi layanan default — ubah/luaskan sesuai kebutuhan
jenis_options = [
    "Cuci Kering",
    "Cuci Basah",
    "Setrika",
    "Cuci & Setrika",
]
entry_jenis = ttk.Combobox(frame_transaksi, values=jenis_options, state="readonly")
entry_jenis.current(0)
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

def edit_transaksi():
    selected = tree_transaksi.focus()
    if not selected:
        messagebox.showwarning("Peringatan", "Pilih data transaksi yang akan diedit!")
        return

    values = tree_transaksi.item(selected, "values")
    id_transaksi = values[0]
    id_pelanggan = values[1]
    nama = values[1]  # ini nama, bukan id_pelanggan
    tanggal = values[2]
    jenis = values[3]
    berat = values[4]
    total = values[5]
    diskon = values[6]
    status = values[7]

    # Ambil id_pelanggan dari nama
    conn = database.koneksi()
    cursor = conn.cursor()
    cursor.execute("SELECT id_pelanggan FROM pelanggan WHERE nama = ?", (nama,))
    result = cursor.fetchone()
    conn.close()
    if not result:
        messagebox.showerror("Error", "Pelanggan tidak ditemukan!")
        return
    id_pelanggan = result[0]

    top = tk.Toplevel(root)
    top.title("Edit Transaksi")

    tk.Label(top, text="ID Pelanggan:").grid(row=0, column=0)
    tk.Label(top, text="Jenis Layanan:").grid(row=1, column=0)
    tk.Label(top, text="Berat (kg):").grid(row=2, column=0)
    tk.Label(top, text="Status:").grid(row=3, column=0)

    entry_id_edit = tk.Entry(top)
    entry_jenis_edit = ttk.Combobox(top, values=jenis_options, state="readonly")
    entry_berat_edit = tk.Entry(top)
    entry_status_edit = tk.Entry(top)

    entry_id_edit.insert(0, id_pelanggan)
    entry_jenis_edit.set(jenis)
    entry_berat_edit.insert(0, berat)
    entry_status_edit.insert(0, status)

    entry_id_edit.grid(row=0, column=1)
    entry_jenis_edit.grid(row=1, column=1)
    entry_berat_edit.grid(row=2, column=1)
    entry_status_edit.grid(row=3, column=1)

    def simpan_edit_transaksi():
        try:
            id_pel = int(entry_id_edit.get())
            jenis = entry_jenis_edit.get()
            berat = float(entry_berat_edit.get())
            status = entry_status_edit.get()
            total, diskon = hitung_total_dengan_diskon(berat)

            database.update_transaksi(id_transaksi, id_pel, jenis, berat, total, diskon, status)
            messagebox.showinfo("Berhasil", "Transaksi diperbarui!")
            top.destroy()
            tampil_transaksi()
        except ValueError:
            messagebox.showerror("Error", "Input tidak valid!")

    tk.Button(top, text="Simpan", command=simpan_edit_transaksi).grid(row=4, column=1, pady=5)

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
tk.Button(frame_transaksi, text="Edit Transaksi", command=edit_transaksi).grid(row=5, column=1, pady=5)

# === Tabel Transaksi ===
tree_transaksi = ttk.Treeview(root, columns=("ID", "Nama", "Tanggal", "Layanan", "Berat", "Total", "Diskon", "Status"), show="headings")
for col in ("ID", "Nama", "Tanggal", "Layanan", "Berat", "Total", "Diskon", "Status"):
    tree_transaksi.heading(col, text=col)
    
col_widths = {
    "ID": 50,
    "Nama": 180,
    "Tanggal": 100,
    "Layanan": 120,
    "Berat": 60,
    "Total": 100,
    "Diskon": 80,
    "Status": 90,
}
for col, w in col_widths.items():
    tree_transaksi.column(col, width=w, minwidth=20, anchor="center")

tree_transaksi.pack(fill="both", expand=True, padx=10, pady=5)

def tampil_transaksi():
    for row in tree_transaksi.get_children():
        tree_transaksi.delete(row)
    for row in database.get_transaksi():
        tree_transaksi.insert("", "end", values=row)

tampil_transaksi()

root.mainloop()
