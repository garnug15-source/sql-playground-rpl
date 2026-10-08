import sqlite3
import pandas as pd
import streamlit as st

# Konfigurasi halaman agar rapi di HP
st.set_page_config(
    page_title="Belajar SQL RPL", page_icon="💻", layout="centered"
)

st.title("💻 Mini SQL Playground")
st.caption(
    "Media latihan database mandiri untuk Kelas XI RPL - Versi Super Lengkap!"
)


# Inisialisasi Database SQLite
def init_db():
  conn = sqlite3.connect("sekolah.db")
  c = conn.cursor()
  c.execute("""
        CREATE TABLE IF NOT EXISTS siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            kelas TEXT,
            nilai INTEGER,
            jurusan TEXT
        )
    """)
  # Masukin data awal kalau kosong
  c.execute("SELECT COUNT(*) FROM siswa")
  if c.fetchone()[0] == 0:
    c.executemany(
        "INSERT INTO siswa (nama, kelas, nilai, jurusan) VALUES (?, ?, ?, ?)",
        [
            ("AKBAR HABIBI", "XI RPL 1", 85, "RPL"),
            ("M ALFATH JABAR", "XI RPL 1", 90, "RPL"),
            ("ALDY", "XI RPL 2", 78, "TKJ"),
            ("HUMAIRA UMBU", "XI RPL 2", 92, "RPL"),
            ("SITI AMINAH", "XI RPL 1", 88, "RPL"),
            ("JOKO ANWAR", "XI RPL 2", 65, "TKJ"),
        ],
    )
  conn.commit()
  conn.close()


init_db()

# Hubungkan ke database
conn = sqlite3.connect("sekolah.db")

# Cheat sheet materi query super lengkap
with st.expander("💡 Panduan & Cheat Sheet Query SQL Lengkap"):
  st.markdown("Anak-anak bisa coba beberapa variasi perintah di bawah ini:")
  st.code("SELECT * FROM siswa;", language="sql")
  st.code("SELECT nama, nilai FROM siswa WHERE nilai > 80;", language="sql")
  st.code("SELECT * FROM siswa ORDER BY nilai DESC;", language="sql")
  st.code("SELECT * FROM siswa WHERE nama LIKE '%A%';", language="sql")
  st.code(
      "INSERT INTO siswa (nama, kelas, nilai, jurusan) VALUES ('RIAN', 'XI RPL"
      " 1', 88, 'RPL');",
      language="sql",
  )
  st.code(
      "UPDATE siswa SET nilai = 95 WHERE nama = 'ALDY';", language="sql"
  )
  st.code("DELETE FROM siswa WHERE nilai < 70;", language="sql")

# Kotak input query SQL
query = st.text_area(
    "Ketik Perintah SQL di Sini:",
    "SELECT * FROM siswa;",
    height=100,
)

if st.button("Jalankan Query 🚀", type="primary"):
  try:
    if query.strip().lower().startswith("select"):
      # Kalau SELECT, tampilkan hasilnya dalam bentuk tabel
      df = pd.read_sql_query(query, conn)
      st.success(
          f"Query berhasil dieksekusi! Menampilkan {len(df)} baris data."
      )
      st.dataframe(df, use_container_width=True)
    else:
      # Kalau INSERT/UPDATE/DELETE
      c = conn.cursor()
      c.execute(query)
      conn.commit()
      st.success("Perintah berhasil dijalankan! Database telah diperbarui.")

      # Tampilkan tabel terbaru setelah diubah
      df_updated = pd.read_sql_query("SELECT * FROM siswa", conn)
      st.markdown("### Data Tabel Siswa Terbaru:")
      st.dataframe(df_updated, use_container_width=True)
  except Exception as e:
    st.error(f"Error SQL: {e}")

conn.close()
