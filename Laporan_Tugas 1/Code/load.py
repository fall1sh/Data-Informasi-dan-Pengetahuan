import mysql.connector
import csv

# Koneksi ke database MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Sesuaikan dengan user MySQL Anda
    password="",  # Sesuaikan dengan password MySQL Anda
    database="berita_detik"
)
cursor = conn.cursor()

# Buka file CSV dan masukkan data ke database
with open("berita_detik_Jan-Feb_2025.csv", "r", encoding="utf-8-sig") as file:
    reader = csv.reader(file)
    next(reader)  # Lewati header CSV

    for row in reader:
        sumber, tanggal, judul, link, snippet = row
        cursor.execute("""
            INSERT INTO berita (sumber, tanggal, judul, link, snippet)
            VALUES (%s, %s, %s, %s, %s)
        """, (sumber, tanggal, judul, link, snippet))

# Simpan perubahan dan tutup koneksi
conn.commit()
cursor.close()
conn.close()

print("✅ Data berhasil dimasukkan ke database!")
