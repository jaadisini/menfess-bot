# 🤖 Menfess Bot Telegram - by @aesneverhere

Bot Telegram anonim yang memungkinkan pengguna mengirimkan pesan rahasia (menfess) ke channel dengan sistem preferensi, reply, hashtag, dan berbagai fitur lainnya.

---

## 🚀 Fitur Utama

- 🔒 **Anonim Menfess** — kirim pesan tanpa identitas ke channel
- 🎯 **Preferensi User** — gender, umur, domisili, dll
- 💬 **Sistem Reply Otomatis** — balas pesan menfess langsung via bot
- 🔎 **Pencarian Hashtag** — cari menfess berdasarkan topik (#cinta, #galau, dll)
- 📊 **Statistik & Voting** — lihat siapa yang aktif dan paling banyak kirim menfess
- 🧠 **Auto Moderasi** — blokir spam, kata kasar, dan pelanggaran lainnya
- 🖼️ **Dukungan Media** — bisa kirim foto, video, stiker, dan dokumen
- 💾 **Backup & Restore** — simpan preferensi user secara lokal
- 🌐 **Fallback Database** — pakai MongoDB atau database lokal
- 🔧 **Struktur Modular** — anti-crash, setiap fitur terpisah
- ⚙️ **Maintenance Otomatis** (CI/CD) — linting, audit keamanan, auto update dependency

---

## 🛠️ Teknologi yang Digunakan

- [Pyrogram](https://docs.pyrogram.org/) – Bot API
- Python 3.11+
- SQLite / JSON – local storage fallback
- GitHub Actions – otomatisasi testing, linting, dan security audit
- (Opsional) MongoDB – penyimpanan online

---

## 📦 Setup Cepat

```bash
# Clone repo
git clone https://github.com/namamu/menfess-bot.git
cd menfess-bot

# Install dependencies
pip install -r requirements.txt

# Jalankan bot
python main.py
