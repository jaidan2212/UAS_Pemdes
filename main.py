import tkinter as tk
from tkinter import ttk, messagebox
import database
from datetime import datetime
import math

# [NOMOR 1] Init Database saat aplikasi jalan
database.init_db()

root = tk.Tk()
root.title("Aplikasi Laundry - UAS Pemdes")
root.geometry("950x700")

# Variabel Global Pagination
hal_pel = 1
limit_pel = 5
hal_trans = 1
limit_trans = 5

# ==========================================
# BAGIAN 1: PELANGGAN
# ==========================================
frame_pel_container = tk.LabelFrame(root, text="Kelola Pelanggan", padx=10, pady=10)
frame_pel_container.pack(fill="both", expand=True, padx=10, pady=5)

# --- FORM INPUT ---
frame_form_pel = tk.Frame(frame_pel_container)
frame_form_pel.pack(fill="x", pady=5)

tk.Label(frame_form_pel, text="Nama:").grid(row=0, column=0, sticky="w")
entry_nama = tk.Entry(frame_form_pel, width=30)
entry_nama.grid(row=0, column=1, padx=5)

tk.Label(frame_form_pel, text="Alamat:").grid(row=1, column=0, sticky="w")
entry_alamat = tk.Entry(frame_form_pel, width=30)
entry_alamat.grid(row=1, column=1, padx=5)

tk.Label(frame_form_pel, text="No HP:").grid(row=2, column=0, sticky="w")
entry_hp = tk.Entry(frame_form_pel, width=30)
entry_hp.grid(row=2, column=1, padx=5)

# --- TOMBOL NAVIGASI PINTAR (SEAMLESS) ---
frame_nav_record_pel = tk.Frame(frame_form_pel)
frame_nav_record_pel.grid(row=3, column=1, pady=5, sticky="w")

def nav_record_pel(arah):
    global hal_pel
    items = tree_pelanggan.get_children()
    if not items and arah not in ["first", "last"]: return

    # Cek posisi sekarang
    selected = tree_pelanggan.selection()
    if not selected:
        idx = -1 # Belum ada yg dipilih
    else:
        idx = items.index(selected[0])
    
    # Hitung Total Halaman Dulu
    kw_nama = fil_nama_pel.get()
    kw_almt = fil_alamat_pel.get()
    total = database.count_pelanggan(kw_nama, kw_almt)
    max_hal = math.ceil(total / limit_pel) or 1

    # === LOGIKA NAVIGASI ANTAR HALAMAN ===
    target_idx = -1 # Penanda mau pilih baris mana nanti

    if arah == "next":
        if idx < len(items) - 1 and idx != -1:
            # Masih di halaman yang sama, geser ke bawah
            target_idx = idx + 1
            child = items[target_idx]
            tree_pelanggan.selection_set(child); tree_pelanggan.focus(child); tree_pelanggan.see(child)
            on_select_pelanggan(None)
        elif hal_pel < max_hal:
            # Sudah mentok bawah, PINDAH KE HALAMAN BERIKUTNYA
            hal_pel += 1
            tampil_pelanggan()
            # Pilih baris paling atas di halaman baru
            new_items = tree_pelanggan.get_children()
            if new_items:
                child = new_items[0]
                tree_pelanggan.selection_set(child); tree_pelanggan.focus(child); tree_pelanggan.see(child)
                on_select_pelanggan(None)

    elif arah == "prev":
        if idx > 0:
            # Masih di halaman yang sama, geser ke atas
            target_idx = idx - 1
            child = items[target_idx]
            tree_pelanggan.selection_set(child); tree_pelanggan.focus(child); tree_pelanggan.see(child)
            on_select_pelanggan(None)
        elif hal_pel > 1:
            # Sudah mentok atas, PINDAH KE HALAMAN SEBELUMNYA
            hal_pel -= 1
            tampil_pelanggan()
            # Pilih baris paling bawah di halaman sebelumnya
            new_items = tree_pelanggan.get_children()
            if new_items:
                child = new_items[-1]
                tree_pelanggan.selection_set(child); tree_pelanggan.focus(child); tree_pelanggan.see(child)
                on_select_pelanggan(None)

    elif arah == "last":
        # Loncat ke HALAMAN TERAKHIR
        hal_pel = max_hal
        tampil_pelanggan()
        # Pilih baris paling bawah
        new_items = tree_pelanggan.get_children()
        if new_items:
            child = new_items[-1]
            tree_pelanggan.selection_set(child); tree_pelanggan.focus(child); tree_pelanggan.see(child)
            on_select_pelanggan(None)

    elif arah == "first":
        # Loncat ke HALAMAN PERTAMA
        hal_pel = 1
        tampil_pelanggan()
        # Pilih baris paling atas
        new_items = tree_pelanggan.get_children()
        if new_items:
            child = new_items[0]
            tree_pelanggan.selection_set(child); tree_pelanggan.focus(child); tree_pelanggan.see(child)
            on_select_pelanggan(None)

tk.Button(frame_nav_record_pel, text="<<", width=3, command=lambda: nav_record_pel("first")).pack(side="left")
tk.Button(frame_nav_record_pel, text="<", width=3, command=lambda: nav_record_pel("prev")).pack(side="left")
tk.Button(frame_nav_record_pel, text=">", width=3, command=lambda: nav_record_pel("next")).pack(side="left")
tk.Button(frame_nav_record_pel, text=">>", width=3, command=lambda: nav_record_pel("last")).pack(side="left")

# --- TOMBOL AKSI CRUD ---
frame_aksi_pel = tk.Frame(frame_form_pel)
frame_aksi_pel.grid(row=4, column=1, pady=5, sticky="w")

def clear_pel():
    entry_nama.delete(0, tk.END)
    entry_alamat.delete(0, tk.END)
    entry_hp.delete(0, tk.END)
    if tree_pelanggan.selection():
        tree_pelanggan.selection_remove(tree_pelanggan.selection())

def simpan_pel():
    if entry_nama.get():
        database.insert_pelanggan(entry_nama.get(), entry_alamat.get(), entry_hp.get())
        messagebox.showinfo("Sukses", "Data disimpan")
        tampil_pelanggan()
        clear_pel()
    else: messagebox.showwarning("Error", "Nama wajib diisi")

def update_pel():
    sel = tree_pelanggan.selection()
    if sel:
        uid = tree_pelanggan.item(sel[0], "values")[0]
        database.update_pelanggan(uid, entry_nama.get(), entry_alamat.get(), entry_hp.get())
        messagebox.showinfo("Sukses", "Data diupdate")
        tampil_pelanggan()
    else:
        messagebox.showwarning("Peringatan", "Pilih data dulu di tabel!")

tk.Button(frame_aksi_pel, text="Clear / Baru", command=clear_pel).pack(side="left", padx=2)
tk.Button(frame_aksi_pel, text="Simpan Baru", command=simpan_pel).pack(side="left", padx=2)
tk.Button(frame_aksi_pel, text="Update Data", command=update_pel).pack(side="left", padx=2)

# --- FILTER ---
frame_filter_pel = tk.Frame(frame_pel_container, bg="#eee", padx=5, pady=5)
frame_filter_pel.pack(fill="x", pady=5)

tk.Label(frame_filter_pel, text="Cari Nama:", bg="#eee").pack(side="left")
fil_nama_pel = tk.Entry(frame_filter_pel)
fil_nama_pel.pack(side="left", padx=5)

tk.Label(frame_filter_pel, text="Cari Alamat:", bg="#eee").pack(side="left")
fil_alamat_pel = tk.Entry(frame_filter_pel)
fil_alamat_pel.pack(side="left", padx=5)

tk.Button(frame_filter_pel, text="Cari", command=lambda: [reset_hal_pel(), tampil_pelanggan()]).pack(side="left", padx=5)
tk.Button(frame_filter_pel, text="Reset", command=lambda: [fil_nama_pel.delete(0,tk.END), fil_alamat_pel.delete(0,tk.END), reset_hal_pel(), tampil_pelanggan()]).pack(side="left")

def reset_hal_pel():
    global hal_pel
    hal_pel = 1

# --- TABEL PELANGGAN ---
tree_pelanggan = ttk.Treeview(frame_pel_container, columns=("ID", "Nama", "Alamat", "No HP"), show="headings", height=5)
for c in ("ID", "Nama", "Alamat", "No HP"):
    tree_pelanggan.heading(c, text=c)
    tree_pelanggan.column(c, width=100)
tree_pelanggan.pack(fill="x")

def on_select_pelanggan(e):
    sel = tree_pelanggan.selection()
    if sel: 
        val = tree_pelanggan.item(sel[0], "values")
        entry_nama.delete(0, tk.END); entry_nama.insert(0, val[1])
        entry_alamat.delete(0, tk.END); entry_alamat.insert(0, val[2])
        entry_hp.delete(0, tk.END); entry_hp.insert(0, val[3])

tree_pelanggan.bind("<<TreeviewSelect>>", on_select_pelanggan)

# Pagination Control
frame_page_pel = tk.Frame(frame_pel_container)
frame_page_pel.pack(pady=5)
lbl_hal_pel = tk.Label(frame_page_pel, text="Halaman 1")

def ganti_hal_pel(arah):
    global hal_pel
    kw_nama = fil_nama_pel.get()
    kw_almt = fil_alamat_pel.get()
    total = database.count_pelanggan(kw_nama, kw_almt)
    max_hal = math.ceil(total / limit_pel) or 1
    
    if arah == "next" and hal_pel < max_hal: hal_pel += 1
    elif arah == "prev" and hal_pel > 1: hal_pel -= 1
    tampil_pelanggan()

tk.Button(frame_page_pel, text="< Mundur", command=lambda: ganti_hal_pel("prev")).pack(side="left")
lbl_hal_pel.pack(side="left", padx=10)
tk.Button(frame_page_pel, text="Maju >", command=lambda: ganti_hal_pel("next")).pack(side="left")

def tampil_pelanggan():
    for i in tree_pelanggan.get_children(): tree_pelanggan.delete(i)
    
    offset = (hal_pel - 1) * limit_pel
    kw_nama = fil_nama_pel.get()
    kw_almt = fil_alamat_pel.get()
    
    rows = database.get_pelanggan_page(limit_pel, offset, kw_nama, kw_almt)
    for r in rows: tree_pelanggan.insert("", "end", values=r)
    
    total = database.count_pelanggan(kw_nama, kw_almt)
    max_hal = math.ceil(total / limit_pel) or 1
    lbl_hal_pel.config(text=f"Halaman {hal_pel} dari {max_hal}")


# ==========================================
# BAGIAN 2: TRANSAKSI (Logic Navigasi Seamless Juga)
# ==========================================
frame_trans_container = tk.LabelFrame(root, text="Kelola Transaksi", padx=10, pady=10)
frame_trans_container.pack(fill="both", expand=True, padx=10, pady=5)

# --- FORM TRANSAKSI ---
frame_form_trans = tk.Frame(frame_trans_container)
frame_form_trans.pack(fill="x")

tk.Label(frame_form_trans, text="ID Pelanggan:").grid(row=0, column=0)
entry_id_pel = tk.Entry(frame_form_trans, width=20)
entry_id_pel.grid(row=0, column=1)

tk.Label(frame_form_trans, text="Layanan:").grid(row=1, column=0)
cmb_layanan = ttk.Combobox(frame_form_trans, values=["Cuci Kering", "Cuci Basah", "Setrika", "Cuci & Setrika"], width=17)
cmb_layanan.grid(row=1, column=1)

tk.Label(frame_form_trans, text="Berat (kg):").grid(row=0, column=2)
entry_berat = tk.Entry(frame_form_trans, width=10)
entry_berat.grid(row=0, column=3)

tk.Label(frame_form_trans, text="Status:").grid(row=1, column=2)
entry_status = tk.Entry(frame_form_trans, width=10)
entry_status.grid(row=1, column=3)

# --- NAVIGASI TRANSAKSI PINTAR ---
frame_nav_rec_tr = tk.Frame(frame_form_trans)
frame_nav_rec_tr.grid(row=2, column=1, pady=5, sticky="w")

def nav_rec_trans(arah):
    global hal_trans
    items = tree_transaksi.get_children()
    if not items and arah not in ["first", "last"]: return
    
    sel = tree_transaksi.selection()
    if not sel: idx = -1
    else: idx = items.index(sel[0])

    kw_nm = fil_nm_tr.get()
    kw_st = fil_st_tr.get()
    total = database.count_transaksi(kw_nm, kw_st)
    max_hal = math.ceil(total/limit_trans) or 1

    if arah == "next":
        if idx < len(items) - 1 and idx != -1:
            child = items[idx+1]
            tree_transaksi.selection_set(child); tree_transaksi.focus(child); tree_transaksi.see(child)
            on_select_trans(None)
        elif hal_trans < max_hal:
            hal_trans += 1
            tampil_transaksi()
            new_items = tree_transaksi.get_children()
            if new_items:
                child = new_items[0]
                tree_transaksi.selection_set(child); tree_transaksi.focus(child); tree_transaksi.see(child)
                on_select_trans(None)

    elif arah == "prev":
        if idx > 0:
            child = items[idx-1]
            tree_transaksi.selection_set(child); tree_transaksi.focus(child); tree_transaksi.see(child)
            on_select_trans(None)
        elif hal_trans > 1:
            hal_trans -= 1
            tampil_transaksi()
            new_items = tree_transaksi.get_children()
            if new_items:
                child = new_items[-1]
                tree_transaksi.selection_set(child); tree_transaksi.focus(child); tree_transaksi.see(child)
                on_select_trans(None)

    elif arah == "last":
        hal_trans = max_hal
        tampil_transaksi()
        new_items = tree_transaksi.get_children()
        if new_items:
            child = new_items[-1]
            tree_transaksi.selection_set(child); tree_transaksi.focus(child); tree_transaksi.see(child)
            on_select_trans(None)

    elif arah == "first":
        hal_trans = 1
        tampil_transaksi()
        new_items = tree_transaksi.get_children()
        if new_items:
            child = new_items[0]
            tree_transaksi.selection_set(child); tree_transaksi.focus(child); tree_transaksi.see(child)
            on_select_trans(None)

tk.Button(frame_nav_rec_tr, text="<<", width=3, command=lambda: nav_rec_trans("first")).pack(side="left")
tk.Button(frame_nav_rec_tr, text="<", width=3, command=lambda: nav_rec_trans("prev")).pack(side="left")
tk.Button(frame_nav_rec_tr, text=">", width=3, command=lambda: nav_rec_trans("next")).pack(side="left")
tk.Button(frame_nav_rec_tr, text=">>", width=3, command=lambda: nav_rec_trans("last")).pack(side="left")

# --- AKSI CRUD TRANSAKSI ---
def hitung(b):
    h = b * 7000
    d = 0.15 if b >= 7 else (0.1 if b >= 3 else 0)
    return h * (1-d), d

def simpan_trans():
    try:
        b = float(entry_berat.get())
        tot, dis = hitung(b)
        database.insert_transaksi(entry_id_pel.get(), datetime.now().strftime("%Y-%m-%d"), 
                                  cmb_layanan.get(), b, tot, dis, entry_status.get())
        tampil_transaksi()
        messagebox.showinfo("Info", f"Total: {int(tot)}")
    except: messagebox.showerror("Err", "Cek input!")

def update_trans():
    sel = tree_transaksi.selection()
    if sel:
        tid = tree_transaksi.item(sel[0], "values")[0]
        try:
            b = float(entry_berat.get())
            tot, dis = hitung(b)
            database.update_transaksi(tid, entry_id_pel.get(), cmb_layanan.get(), b, tot, dis, entry_status.get())
            tampil_transaksi()
            messagebox.showinfo("Info", "Update sukses")
        except: pass
    else:
        messagebox.showwarning("Info", "Pilih transaksi dulu")

tk.Button(frame_form_trans, text="Simpan", command=simpan_trans).grid(row=3, column=1, sticky="w")
tk.Button(frame_form_trans, text="Update", command=update_trans).grid(row=3, column=3, sticky="w")

# --- FILTER TRANSAKSI ---
frame_fil_tr = tk.Frame(frame_trans_container, bg="#eee", padx=5, pady=5)
frame_fil_tr.pack(fill="x", pady=5)
tk.Label(frame_fil_tr, text="Nama Pelanggan:", bg="#eee").pack(side="left")
fil_nm_tr = tk.Entry(frame_fil_tr)
fil_nm_tr.pack(side="left")
tk.Label(frame_fil_tr, text="Status:", bg="#eee").pack(side="left")
fil_st_tr = ttk.Combobox(frame_fil_tr, values=["", "Proses", "Selesai"], width=10)
fil_st_tr.pack(side="left")
tk.Button(frame_fil_tr, text="Cari", command=lambda: [reset_hal_tr(), tampil_transaksi()]).pack(side="left", padx=5)
tk.Button(frame_fil_tr, text="Reset", command=lambda: [fil_nm_tr.delete(0,tk.END), fil_st_tr.set(""), reset_hal_tr(), tampil_transaksi()]).pack(side="left")

def reset_hal_tr(): global hal_trans; hal_trans=1

# --- TABEL TRANSAKSI ---
cols = ("ID", "Pelanggan", "Tanggal", "Layanan", "Berat", "Total", "Diskon", "Status")
tree_transaksi = ttk.Treeview(frame_trans_container, columns=cols, show="headings", height=5)
for c in cols: 
    tree_transaksi.heading(c, text=c)
    tree_transaksi.column(c, width=80)
tree_transaksi.pack(fill="x")

def on_select_trans(e):
    sel = tree_transaksi.selection()
    if sel:
        v = tree_transaksi.item(sel[0], "values")
        cmb_layanan.set(v[3])
        entry_berat.delete(0,tk.END); entry_berat.insert(0, v[4])
        entry_status.delete(0,tk.END); entry_status.insert(0, v[7])
        # Auto fill ID Pelanggan
        conn = database.koneksi()
        cur = conn.cursor()
        cur.execute("SELECT id_pelanggan FROM pelanggan WHERE nama=?", (v[1],))
        res = cur.fetchone()
        conn.close()
        entry_id_pel.delete(0,tk.END)
        if res: entry_id_pel.insert(0, res[0])

tree_transaksi.bind("<<TreeviewSelect>>", on_select_trans)

# Pagination Transaksi
frame_page_tr = tk.Frame(frame_trans_container)
frame_page_tr.pack(pady=5)
lbl_hal_tr = tk.Label(frame_page_tr, text="Halaman 1")

def ganti_hal_tr(arah):
    global hal_trans
    kw_nm = fil_nm_tr.get()
    kw_st = fil_st_tr.get()
    total = database.count_transaksi(kw_nm, kw_st)
    mx = math.ceil(total/limit_trans) or 1
    if arah=="next" and hal_trans < mx: hal_trans+=1
    elif arah=="prev" and hal_trans > 1: hal_trans-=1
    tampil_transaksi()

tk.Button(frame_page_tr, text="< Mundur", command=lambda: ganti_hal_tr("prev")).pack(side="left")
lbl_hal_tr.pack(side="left", padx=10)
tk.Button(frame_page_tr, text="Maju >", command=lambda: ganti_hal_tr("next")).pack(side="left")

def tampil_transaksi():
    for i in tree_transaksi.get_children(): tree_transaksi.delete(i)
    off = (hal_trans-1)*limit_trans
    rows = database.get_transaksi_page(limit_trans, off, fil_nm_tr.get(), fil_st_tr.get())
    for r in rows: tree_transaksi.insert("", "end", values=r)
    tot = database.count_transaksi(fil_nm_tr.get(), fil_st_tr.get())
    mx = math.ceil(tot/limit_trans) or 1
    lbl_hal_tr.config(text=f"Halaman {hal_trans} dari {mx}")

# Init awal
tampil_pelanggan()
tampil_transaksi()
root.mainloop()