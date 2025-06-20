#!/bin/bash

clear

echo "============================================="
echo "🤖 MENFESS TELEGRAM BOT SETUP"
echo "============================================="

# ASCII Art Banner
echo -e "
\033[1;35m
 __  __ ______ _   _ ______ ______ _____  _____  _____ 
|  \/  |  ____| \ | |  ____|  ____|  __ \|  __ \|  __ \\
| \  / | |__  |  \| | |__  | |__  | |__) | |__) | |  | |
| |\/| |  __| | . \` |  __| |  __| |  _  /|  _  /| |  | |
| |  | | |____| |\  | |____| |____| | \ \| | \ \| |__| |
|_|  |_|______|_| \_|______|______|_|  \_\_|  \_\_____/ \033[0m
"

echo -e "\033[1;36mDibuat oleh: @aesneverhere\033[0m"
echo -e "\033[1;36mDeskripsi : Bot Telegram untuk mengirim pesan anonim ke channel.\033[0m"
echo -e "\033[1;36mRepo GitHub: https://github.com/aesneverhere/menfess-bot\033[0m"
echo "============================================="

pkg update -y 2>/dev/null || sudo apt update -y
pkg install -y python git 2>/dev/null || sudo apt install -y python3 python3-pip git

python3 -m venv env 2>/dev/null
source env/bin/activate 2>/dev/null || echo "⚠️ Virtualenv tidak aktif. Lanjut tanpa venv."

pip install -r requirements.txt

if [ ! -f .env ]; then
    echo "🔧 Membuat file .env..."

    read -p "Masukkan API_ID: " API_ID
    read -p "Masukkan API_HASH: " API_HASH
    read -p "Masukkan BOT_TOKEN: " BOT_TOKEN
    read -p "Masukkan BOT_USERNAME (tanpa @): " BOT_USERNAME
    read -p "Masukkan CHANNEL_USERNAME (pakai @): " CHANNEL_USERNAME
    read -p "Masukkan ADMIN_ID (angka): " ADMIN_ID
    read -p "Masukkan LOG_CHAT_ID (bisa ID grup/channel, contoh: -1001234567890): " LOG_CHAT_ID

    cat <<EOF > .env
API_ID=$API_ID
API_HASH=$API_HASH
BOT_TOKEN=$BOT_TOKEN
BOT_USERNAME=$BOT_USERNAME
CHANNEL_USERNAME=$CHANNEL_USERNAME
ADMIN_ID=$ADMIN_ID
EOF

    echo "✅ File .env berhasil dibuat."
fi

echo "✅ Instalasi selesai. Jalankan bot dengan:"
echo "python3 main.py"
