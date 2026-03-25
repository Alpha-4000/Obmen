import requests
import time
import json
import os
from datetime import datetime

TOKEN = "8017480371:AAELsrLtoA3ONP-8XTQxNJe5mmpvYZ-mxNU"
ADMIN_ID = 5912710631
URL = f"https://api.telegram.org/bot{TOKEN}"

def bot(method, data=None):
    try:
        r = requests.post(f"{URL}/{method}", json=data or {}, timeout=30)
        return r.json()
    except Exception as e:
        print(f"API xatolik: {e}")
        return {"ok": False}

def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        data["reply_markup"] = reply_markup
    result = bot("sendMessage", data)
    if not result.get("ok"):
        print(f"Xatolik: {result}")
    return result

def delete_message(chat_id, msg_id):
    return bot("deleteMessage", {"chat_id": chat_id, "message_id": msg_id})

def answer_callback(cb_id, text, alert=False):
    return bot("answerCallbackQuery", {"callback_query_id": cb_id, "text": text, "show_alert": alert})

# Fayl operatsiyalari
def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except:
        return None

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(str(content))

def file_exists(path):
    return os.path.exists(path)

# Papkalar
for folder in ["ban", "step", "tizim", "tizim/kurs", "tugma", "obmen"]:
    os.makedirs(folder, exist_ok=True)

# Default fayllar
defaults = {
    "tugma/key1.txt": "🔄 Valyuta ayirboshlash",
    "tugma/key2.txt": "🔰 Hamyonlar",
    "tugma/key3.txt": "📊 Valyuta kursi",
    "tugma/key4.txt": "📞 Aloqa",
    "tugma/key5.txt": "🔁 Almashuvlar",
    "tizim/valyuta.txt": "so'm",
    "tizim/uslug.txt": "5",
    "tizim/holat.txt": "✅",
    "tizim/kurs/sotish_rub.txt": "140",
    "tizim/kurs/sotish_usd.txt": "12800",
    "tizim/kurs/sotib_rub.txt": "135",
    "tizim/kurs/sotib_usd.txt": "12700",
    "tizim/support.txt": "Admin bilan bog'lanish: @support",
    "obmen/obmen.txt": "0"
}
for f, c in defaults.items():
    if not file_exists(f):
        write_file(f, c)

# Menular
key1 = read_file("tugma/key1.txt")
key2 = read_file("tugma/key2.txt")
key3 = read_file("tugma/key3.txt")
key4 = read_file("tugma/key4.txt")
key5 = read_file("tugma/key5.txt")

menu = {
    "resize_keyboard": True,
    "keyboard": [
        [{"text": key1}],
        [{"text": key2}, {"text": key3}],
        [{"text": key4}, {"text": key5}]
    ]
}

admin_menu = {
    "resize_keyboard": True,
    "keyboard": [
        [{"text": key1}],
        [{"text": key2}, {"text": key3}],
        [{"text": key4}, {"text": key5}],
        [{"text": "🗄 Boshqarish"}]
    ]
}

back = {"resize_keyboard": True, "keyboard": [[{"text": "◀️ Orqaga"}]]}

panel = {
    "resize_keyboard": True,
    "keyboard": [
        [{"text": "📊 Statistika"}, {"text": "✉ Xabar yuborish"}],
        [{"text": "🔎 Foydalanuvchini boshqarish"}],
        [{"text": "◀️ Orqaga"}]
    ]
}

# Yordamchi funksiyalar
def get_valyuta():
    return read_file("tizim/valyuta.txt") or "so'm"

def get_kurs():
    return {
        "sotish_rub": float(read_file("tizim/kurs/sotish_rub.txt") or 140),
        "sotish_usd": float(read_file("tizim/kurs/sotish_usd.txt") or 12800),
        "sotib_rub": float(read_file("tizim/kurs/sotib_rub.txt") or 135),
        "sotib_usd": float(read_file("tizim/kurs/sotib_usd.txt") or 12700)
    }

def get_holat():
    return read_file("tizim/holat.txt") or "✅"

def save_user(chat_id):
    if not file_exists("azo.dat"):
        write_file("azo.dat", "")
    data = read_file("azo.dat") or ""
    if str(chat_id) not in data:
        with open("azo.dat", "a", encoding="utf-8") as f:
            f.write(f"{chat_id}\n")

def is_banned(chat_id):
    return file_exists(f"ban/{chat_id}.txt")

# Asosiy handler
user_steps = {}

def handle_message(chat_id, text, username, msg_id):
    print(f"Xabar: {text} (chat={chat_id})")
    if is_banned(chat_id):
        return
    save_user(chat_id)

    step = user_steps.get(chat_id, "")
    valyuta = get_valyuta()
    kurs = get_kurs()

    if text == "/start":
        if chat_id == ADMIN_ID:
            send_message(chat_id, "💎 Admin paneliga xush kelibsiz!", json.dumps(admin_menu))
        else:
            send_message(chat_id, "💎 Valyuta ayirboshlash botiga xush kelibsiz!", json.dumps(menu))
        if chat_id in user_steps:
            del user_steps[chat_id]

    elif text == "◀️ Orqaga":
        if chat_id == ADMIN_ID:
            send_message(chat_id, "🏠 Asosiy menyu", json.dumps(admin_menu))
        else:
            send_message(chat_id, "🏠 Asosiy menyu", json.dumps(menu))
        if chat_id in user_steps:
            del user_steps[chat_id]

    elif text == key2:  # Hamyonlar
        msg = "<b>💳 Sizning hamyonlaringiz:</b>\n"
        for w in ["uzcard", "humo", "qiwi"]:
            val = read_file(f"tizim/hamyon/{chat_id}/{w}.txt") or "kiritilmagan"
            msg += f"\n📌 {w.upper()}: <code>{val}</code>"
        kb = {"inline_keyboard": [[{"text": "➕ UZCARD", "callback_data": "add_uzcard"},
                                   {"text": "➕ HUMO", "callback_data": "add_humo"}],
                                  [{"text": "➕ QIWI", "callback_data": "add_qiwi"}]]}
        send_message(chat_id, msg, json.dumps(kb))

    elif text == key3:  # Valyuta kursi
        msg = f"📉 Sotish:\n1 RUB = {kurs['sotish_rub']} {valyuta}\n1 USD = {kurs['sotish_usd']} {valyuta}\n\n📉 Sotib olish:\n1 RUB = {kurs['sotib_rub']} {valyuta}\n1 USD = {kurs['sotib_usd']} {valyuta}"
        send_message(chat_id, msg)

    elif text == key4:  # Aloqa
        kb = {"inline_keyboard": [[{"text": "📝 Xabar yozish", "callback_data": "contact"}]]}
        send_message(chat_id, f"<b>{read_file('tizim/support.txt')}</b>", json.dumps(kb))

    elif text == key5:  # Almashuv ID qidirish
        send_message(chat_id, "🆔 Almashuv ID sini yuboring:", json.dumps(back))
        user_steps[chat_id] = "search_exchange"

    elif text == key1:  # Ayirboshlash
        if get_holat() == "❌":
            send_message(chat_id, "⚠️ Almashinuv vaqtinchalik to‘xtatilgan.")
            return
        kb = {"inline_keyboard": [
            [{"text": "🔼 UZCARD", "callback_data": "from_uzcard"}, {"text": "🔽 UZCARD", "callback_data": "error"}],
            [{"text": "🔼 HUMO", "callback_data": "from_humo"}, {"text": "🔽 HUMO", "callback_data": "error"}],
            [{"text": "🔼 QIWI", "callback_data": "from_qiwi"}, {"text": "🔽 QIWI", "callback_data": "error"}]
        ]}
        send_message(chat_id, "🔼 Berish valyutasini tanlang:", json.dumps(kb))

    elif text == "🗄 Boshqarish" and chat_id == ADMIN_ID:
        send_message(chat_id, "Admin paneli", json.dumps(panel))
        if chat_id in user_steps:
            del user_steps[chat_id]

    # Admin buyruqlari
    elif chat_id == ADMIN_ID:
        if text == "📊 Statistika":
            users = len((read_file("azo.dat") or "").split("\n")) if file_exists("azo.dat") else 0
            exchanges = len(os.listdir("obmen")) if os.path.exists("obmen") else 0
            send_message(chat_id, f"👥 Foydalanuvchilar: {users}\n🔄 Almashuvlar: {exchanges}")

        elif text == "✉ Xabar yuborish":
            send_message(chat_id, "Xabarni yuboring:", json.dumps(back))
            user_steps[chat_id] = "broadcast"

        elif text == "🔎 Foydalanuvchini boshqarish":
            send_message(chat_id, "ID raqamini kiriting:", json.dumps(back))
            user_steps[chat_id] = "find_user"

    # Qadamlar
    elif step == "search_exchange":
        if file_exists(f"obmen/{text}/id.txt"):
            info = f"ID: {read_file(f'obmen/{text}/id.txt')}\nHolat: {read_file(f'obmen/{text}/holat.txt')}"
            send_message(chat_id, f"✅ Almashuv topildi:\n{info}")
        else:
            send_message(chat_id, "❌ Almashuv topilmadi!")
        del user_steps[chat_id]

    elif step.startswith("add_"):
        w = step[4:]
        write_file(f"tizim/hamyon/{chat_id}/{w}.txt", text)
        send_message(chat_id, f"✅ {w.upper()} hamyon saqlandi!", json.dumps(menu))
        del user_steps[chat_id]

    elif step == "broadcast" and chat_id == ADMIN_ID:
        users = (read_file("azo.dat") or "").split("\n")
        count = 0
        for uid in users:
            if uid.strip():
                send_message(int(uid), f"📢 <b>Xabar</b>\n\n{text}")
                count += 1
        send_message(chat_id, f"✅ {count} ta foydalanuvchiga yuborildi!")
        del user_steps[chat_id]

    elif step == "find_user" and chat_id == ADMIN_ID:
        if file_exists(f"odam/{text}.dat") or file_exists(f"tizim/hamyon/{text}"):
            banned = file_exists(f"ban/{text}.txt")
            btn = "🔕 Bandan olish" if banned else "🔔 Banlash"
            kb = {"inline_keyboard": [[{"text": btn, "callback_data": f"ban_{text}"}]]}
            send_message(chat_id, f"✅ Foydalanuvchi topildi!\nID: {text}", json.dumps(kb))
        else:
            send_message(chat_id, "❌ Topilmadi!")
        del user_steps[chat_id]

def handle_callback(cb_id, chat_id, msg_id, data):
    print(f"Callback: {data}")
    if is_banned(chat_id):
        return

    if data == "contact":
        delete_message(chat_id, msg_id)
        send_message(chat_id, "Xabaringizni yozing:", json.dumps(back))
        user_steps[chat_id] = "contact"

    elif data.startswith("add_"):
        w = data[4:]
        delete_message(chat_id, msg_id)
        send_message(chat_id, f"➕ {w.upper()} raqamini kiriting:", json.dumps(back))
        user_steps[chat_id] = f"add_{w}"

    elif data.startswith("from_"):
        from_w = data[5:]
        kb = {"inline_keyboard": []}
        for w in ["uzcard", "humo", "qiwi"]:
            if w != from_w:
                kb["inline_keyboard"].append([{"text": f"🔽 {w.upper()}", "callback_data": f"to_{from_w}_{w}"}])
        delete_message(chat_id, msg_id)
        send_message(chat_id, f"🔼 {from_w.upper()} dan qaysi valyutaga?", json.dumps(kb))

    elif data.startswith("to_"):
        _, from_w, to_w = data.split("_")
        user_w = read_file(f"tizim/hamyon/{chat_id}/{from_w}.txt")
        admin_w = read_file(f"tizim/hamyon/raqam/{ADMIN_ID}/{from_w}.txt") or "kiritilmagan"
        if user_w in [None, "kiritilmagan"]:
            answer_callback(cb_id, f"⚠️ Avval {from_w.upper()} hamyon kiriting!", True)
            return
        if admin_w == "kiritilmagan":
            answer_callback(cb_id, "⚠️ Admin hamyoni kiritilmagan!", True)
            return
        delete_message(chat_id, msg_id)
        send_message(chat_id, f"🔄 {from_w.upper()} → {to_w.upper()}\n\n💳 Siz: {user_w}\n💳 Admin: {admin_w}\n\nSummani kiriting:", json.dumps(back))
        user_steps[chat_id] = f"amount_{from_w}_{to_w}"

    elif data.startswith("amount_"):
        # Bu qism oddiy ayirboshlash uchun, amalda to‘liq funksiya kerak, hozircha demo
        answer_callback(cb_id, "Bu funksiya sinovda", True)

    elif data.startswith("ban_"):
        target = data[4:]
        if file_exists(f"ban/{target}.txt"):
            os.remove(f"ban/{target}.txt")
            send_message(chat_id, f"✅ {target} bandan olindi!")
        else:
            write_file(f"ban/{target}.txt", "ban")
            send_message(chat_id, f"✅ {target} banlandi!")
        delete_message(chat_id, msg_id)

    answer_callback(cb_id, "")

# ============ POLLING LOOP ============
def main():
    print("Bot ishga tushdi!")
    offset = 0
    while True:
        try:
            resp = bot("getUpdates", {"offset": offset, "timeout": 30})
            if resp.get("ok"):
                for upd in resp.get("result", []):
                    msg = upd.get("message")
                    cb = upd.get("callback_query")
                    if msg:
                        chat = msg["chat"]["id"]
                        txt = msg.get("text", "")
                        user = msg["from"].get("username", "")
                        mid = msg["message_id"]
                        handle_message(chat, txt, user, mid)
                    elif cb:
                        chat = cb["message"]["chat"]["id"]
                        mid = cb["message"]["message_id"]
                        cid = cb["id"]
                        d = cb["data"]
                        handle_callback(cid, chat, mid, d)
                    offset = upd["update_id"] + 1
            time.sleep(1)
        except Exception as e:
            print(f"Xatolik: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
