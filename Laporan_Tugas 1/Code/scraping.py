import requests
import csv
import datetime
import time
import random
from bs4 import BeautifulSoup

# Header agar tidak terdeteksi sebagai bot
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Rentang waktu: 1 Januari 2025 - 28 Februari 2025
start_date = datetime.date(2025, 1, 1)
end_date = datetime.date(2025, 2, 28)
tanggal_list = [(start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d") 
                 for i in range((end_date - start_date).days + 1)]

# Fungsi untuk scraping berita Detik berdasarkan indeks tanggal
def scrape_detik(tanggal):
    data = []
    url = f"https://news.detik.com/indeks?date={tanggal}"
    print(f"📄 Mengambil berita dari {url}")

    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"⚠️ Gagal mengambil data dari {url}")
        return data

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article")

    if not articles:
        print(f"❌ Tidak ada artikel ditemukan untuk {tanggal}")
        return data

    for article in articles:
        try:
            title_elem = article.find("h2") or article.find("h3")
            title = title_elem.text.strip() if title_elem else "No Title"

            link_elem = article.find("a")
            link = link_elem["href"] if link_elem else "No Link"

            snippet_elem = article.find("p")
            snippet = snippet_elem.text.strip() if snippet_elem else "No Snippet"

            data.append(["Detik", tanggal, title, link, snippet])
        except Exception as e:
            print(f"⚠️ Gagal mengambil artikel: {e}")
            continue

    time.sleep(random.uniform(2, 5))  # Delay lebih panjang agar tidak terdeteksi bot
    return data

# Looping untuk scraping semua tanggal
data_berita = []
print("🔍 Mengambil semua berita dari Detik untuk Januari - Februari 2025...")

for tanggal in tanggal_list:
    try:
        berita_harian = scrape_detik(tanggal)
        data_berita.extend(berita_harian)
        print(f"✅ Berita dari {tanggal} berhasil diambil! ({len(berita_harian)} berita)")
    except Exception as e:
        print(f"⚠️ Gagal mengambil berita untuk {tanggal}: {e}")

# Simpan hasil scraping ke CSV
if data_berita:
    with open("berita_detik_Jan-Feb_2025.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Sumber", "Tanggal", "Judul", "Link", "Snippet"])  # Header CSV
        writer.writerows(data_berita)

    print("\n✅ Scraping selesai! Data telah disimpan dalam 'berita_detik_Jan-Feb_2025.csv'.")
else:
    print("\n❌ Tidak ada data yang berhasil diambil! Periksa struktur HTML situs web.")
