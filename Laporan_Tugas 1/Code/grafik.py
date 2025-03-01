import mysql.connector
import matplotlib.pyplot as plt

# Koneksi ke database MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Sesuaikan dengan username MySQL
    password="",  # Sesuaikan dengan password MySQL
    database="berita_detik"
)
cursor = conn.cursor()

# Ambil data kategori dan jumlah dari database
query = "SELECT kategori, jumlah FROM kasus_terkategori"
cursor.execute(query)
data = cursor.fetchall()

# Tutup koneksi database
cursor.close()
conn.close()

# Pisahkan data menjadi dua list: kategori dan jumlah
kategori = [row[0] for row in data]
jumlah = [row[1] for row in data]

# Buat explode untuk memisahkan bagian yang lebih besar
explode = [0.1 if j == max(jumlah) else 0.05 for j in jumlah]  # Memisahkan kategori dengan jumlah terbesar lebih jauh

# Buat pie chart dengan angka asli dan irisan yang terpisah
plt.figure(figsize=(8, 8))
plt.pie(jumlah, labels=kategori, autopct=lambda p: f'{int(p * sum(jumlah) / 100)}', 
        startangle=140, explode=explode, shadow=True, wedgeprops={'edgecolor': 'black'})

plt.title("Distribusi Kasus Berdasarkan Kategori")
plt.show()
