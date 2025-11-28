import json
from telegram.ext import Updater, CommandHandler

DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {"quy": 0, "lich_su": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def start(update, context):
    update.message.reply_text(
        "👋 Xin chào!\n"
        "Bot quản lý tiền quỹ và tiền đi chợ.\n\n"
        "Lệnh dùng:\n"
        "/addquy 100000 – thêm vào quỹ\n"
        "/chitieu 50000 Mua rau – trừ quỹ\n"
        "/report – xem báo cáo"
    )

def add_quy(update, context):
    data = load_data()
    if len(context.args) == 0:
        update.message.reply_text("❗ Hãy nhập số tiền. Ví dụ: /addquy 100000")
        return

    try:
        so_tien = int(context.args[0])
    except:
        update.message.reply_text("❗ Số tiền không hợp lệ.")
        return

    data["quy"] += so_tien
    data["lich_su"].append(f"+ {so_tien} (Nạp quỹ)")

    save_data(data)
    update.message.reply_text(f"✔ Đã thêm {so_tien} vào quỹ.\n💰 Quỹ hiện tại: {data['quy']}")

def chi_tieu(update, context):
    data = load_data()

    if len(context.args) < 2:
        update.message.reply_text("❗ Dùng:\n/chitieu 50000 Mua thịt")
        return

    try:
        so_tien = int(context.args[0])
    except:
        update.message.reply_text("❗ Số tiền không hợp lệ.")
        return

    mo_ta = " ".join(context.args[1:])

    data["quy"] -= so_tien
    data["lich_su"].append(f"- {so_tien} ({mo_ta})")

    save_data(data)

    update.message.reply_text(f"🧾 Đã chi: {so_tien} - {mo_ta}\n💰 Quỹ còn lại: {data['quy']}")

def report(update, context):
    data = load_data()
    text = f"💰 Quỹ hiện tại: {data['quy']}\n\n📜 Lịch sử:\n"

    if len(data["lich_su"]) == 0:
        text += "Chưa có giao dịch nào."
    else:
        text += "\n".join(data["lich_su"][-20:])

    update.message.reply_text(text)

def main():
    import os
    TOKEN = os.getenv("BOT_TOKEN")

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("addquy", add_quy))
    dp.add_handler(CommandHandler("chitieu", chi_tieu))
    dp.add_handler(CommandHandler("report", report))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
