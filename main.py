from telegram import Update
import os
import json
from datetime import datetime
from google.oauth2.service_account import Credentials
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    filters,
    ContextTypes
)

TOKEN = os.getenv("BOT_TOKEN")




scope = [...]

google_creds = json.loads(
    os.environ["GOOGLE_CREDENTIALS"]
)

creds = Credentials.from_service_account_info(
    google_creds,
    scopes=scope
)
# Tempat menyimpan transaksi sementara
transaksi = []

nama_hari = {
"Monday": "Senin",
"Tuesday": "Selasa",
"Wednesday": "Rabu",
"Thursday": "Kamis",
"Friday": "Jumat",
"Saturday": "Sabtu",
"Sunday": "Minggu"
}

nama_bulan = {
1: "Januari",
2: "Februari",
3: "Maret",
4: "April",
5: "Mei",
6: "Juni",
7: "Juli",
8: "Agustus",
9: "September",
10: "Oktober",
11: "November",
12: "Desember"
}

async def balas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pesan = update.message.text

    try:
        data = pesan.split()

        jenis = data[0]
        kategori = data[1]
        nominal = int(data[2])

        if jenis == "+":
            tipe = "Pemasukan 💰"

        elif jenis == "-":
            tipe = "Pengeluaran 💸"

        else:
            await update.message.reply_text(
                "Format salah.\n\nContoh:\n+ gaji 5000000\n- makan 25000"
            )
            return

        # Simpan transaksi
        transaksi.append({
            "tipe": tipe,
            "kategori": kategori,
            "nominal": nominal
        })

        sekarang = datetime.now()

        timestamp = sekarang.strftime("%Y-%m-%d %H:%M:%S")

        hari = nama_hari[sekarang.strftime("%A")]
        bulan = nama_bulan[sekarang.month]
        tanggal = sekarang.day
        tahun = sekarang.year

        sheet.append_row([
        timestamp,
        hari,
        tanggal,
        bulan,
        tahun,
        tipe,
        kategori,
        nominal
        ])

        print(transaksi)

        await update.message.reply_text(
            f"""✅ Transaksi berhasil dicatat

        Tipe      : {tipe}
        Kategori  : {kategori}
        Nominal   : Rp{nominal:,}
        """
        )

    except Exception as e:
        print("Error:", e)

    await update.message.reply_text(
        f"Error: {e}"
    )


async def saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    pemasukan = 0
    pengeluaran = 0

    for item in transaksi:

        if item["tipe"] == "Pemasukan 💰":
            pemasukan += item["nominal"]

        elif item["tipe"] == "Pengeluaran 💸":
            pengeluaran += item["nominal"]

    saldo_akhir = pemasukan - pengeluaran

    await update.message.reply_text(
        f"""💰 Ringkasan Keuangan

Pemasukan   : Rp{pemasukan:,}
Pengeluaran : Rp{pengeluaran:,}

Saldo       : Rp{saldo_akhir:,}
"""
    )
app = Application.builder().token(TOKEN).build()
# Handler command
app.add_handler(CommandHandler("saldo", saldo))

# Handler pesan biasa
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, balas)
)

print("Finance Bot aktif 🔥")

app.run_polling()