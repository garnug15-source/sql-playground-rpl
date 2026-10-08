import sqlite3
import pandas as pd
import streamlit as st

# Konfigurasi halaman agar rapi di HP
st.set_page_config(
    page_title="Belajar SQL RPL", page_icon="💻", layout="centered"
)

st.title("💻 Mini SQL Playground")
st.caption("Media latihan database mandiri untuk Kelas XI RPL via HP.")


# Inisialisasi Database SQLite
def init_db():
  conn = sqlite3.connect("sekolah.db")
  c = conn.cursor()
  c.execute("""
        CREATE TABLE IF NOT EXISTS siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            kelas TEXT,
            nilai INTEGER
        )
    """)
  # Masukin data awal kalau kosong
  c.execute("SELECT COUNT(*) FROM siswa")
  if c.fetchone()[0] == 0:
    c.executemany(
        "INSERT INTO siswa (nama, kelas, nilai) VALUES (?, ?, ?)",
        [
            ("AKBAR HABIBI", "XI RPL 1", 85),
            ("M ALFATH JABAR", "XI RPL 1", 90),
            ("ALDY", "XI RPL 2", 78),
            ("HUMAIRA UMBU", "XI RPL 2", 92),
        ],
    )
  conn.commit()
  conn.close()


init_db()

# Hubungkan ke database
conn = sqlite3.connect("sekolah.db")

# Cheat sheet materi buat contekan mereka
with st.expander("💡 Contoh Query untuk Latihan"):
  st.code("SELECT * FROM siswa;", language="sql")
  st.code("SELECT nama, nilai FROM siswa WHERE nilai > 80;", language="sql")
  st.code(
      "INSERT INTO siswa (nama, kelas, nilai) VALUES ('Rian', 'XI RPL 1',"
      " 88);",
      language="sql",
  )

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
      st.success("Query berhasil dieksekusi!")
      st.dataframe(df, use_container_width=True)
    else:
      # Kalau INSERT/UPDATE/DELETE
      c = conn.cursor()
      c.execute(query)
      conn.commit()
      st.success("Perintah berhasil dijalankan! Data diperbarui.")

      # Tampilkan tabel terbaru setelah diubah
      df_updated = pd.read_sql_query("SELECT * FROM siswa", conn)
      st.dataframe(df_updated, use_container_width=True)
  except Exception as e:
    st.error(f"Error SQL: {e}")

conn.close()
