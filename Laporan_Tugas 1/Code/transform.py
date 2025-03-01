import mysql.connector
from collections import defaultdict

# Koneksi ke database MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="berita_detik"
)
cursor = conn.cursor()

# Ambil semua berita dari database
cursor.execute("SELECT judul FROM berita")
berita_list = cursor.fetchall()

# Daftar kategori dan kata kunci yang terkait
kategori_mapping = {
    "Korupsi": ["korupsi", "suap", "gratifikasi"],
    "Pencurian": ["maling", "curi", "pencurian", "perampokan"],
    "Pembunuhan": ["bunuh", "pembunuhan", "pembantaian"],
    "Narkoba": ["narkoba", "sabu", "ganja"],
    "Kecelakaan": ["tabrak", "kecelakaan", "laka"],
}

# Buat dictionary untuk menghitung jumlah berita per kategori
kategori_count = defaultdict(int)

# Proses pengelompokan berita ke dalam kategori
for (judul,) in berita_list:
    kategori_ditemukan = False
    for kategori, keywords in kategori_mapping.items():
        if any(keyword.lower() in judul.lower() for keyword in keywords):
            kategori_count[kategori] += 1
            kategori_ditemukan = True
            break
    if not kategori_ditemukan:
        kategori_count["Lainnya"] += 1  # Jika tidak cocok dengan kategori lain

# Simpan hasil transformasi ke dalam tabel `kasus_terkategori`
cursor.execute("DELETE FROM kasus_terkategori")  # Hapus data lama sebelum memasukkan data baru
for kategori, jumlah in kategori_count.items():
    cursor.execute("""
        INSERT INTO kasus_terkategori (kategori, jumlah)
        VALUES (%s, %s)
    """, (kategori, jumlah))

# Simpan perubahan dan tutup koneksi
conn.commit()
cursor.close()
conn.close()

print("✅ Transformasi selesai! Data telah dikategorikan dan dimasukkan ke database.")
