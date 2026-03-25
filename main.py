import requests
import time
import json
import os
import shutil
import traceback
from datetime import datetime

TOKEN = "8017480371:AAELsrLtoA3ONP-8XTQxNJe5mmpvYZ-mxNU"
ADMIN_ID = 5912710631
URL = f"https://api.telegram.org/bot{TOKEN}"

# ============ FUNKSIYALAR ============
def bot(method, data=None):
    if data is None:
        data = {}
    try:
        r = requests.post(f"{URL}/{method}", json=data, timeout=30)
        return r.json()
    except:
        return {"ok": False}

def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        data["reply_markup"] = reply_markup
    result = bot("sendMessage", data)
    if not result.get("ok"):
        print(f"SendMessage xatolik: {result}")
    return result

def edit_message(chat_id, msg_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "message_id": msg_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        data["reply_markup"] = reply_markup
    return bot("editMessageText", data)

def delete_message(chat_id, msg_id):
    return bot("deleteMessage", {"chat_id": chat_id, "message_id": msg_id})

def answer_callback(cb_id, text, alert=False):
    return bot("answerCallbackQuery", {"callback_query_id": cb_id, "text": text, "show_alert": alert})

# ============ FAYL ISHLARI ============
def read_file(path):
    if not path:
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except:
        return None

def write_file(path, content):
    if not path:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(str(content))

def file_exists(path):
    return os.path.exists(path) if path else False

def delete_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)

# ============ PAPKALAR ============
folders = ["ban", "step", "tizim", "tizim/hamyon", "tizim/hamyon/raqam", f"tizim/hamyon/raqam/{ADMIN_ID}", "tizim/kurs", "odam", "tugma", "obmen"]
for f in folders:
    os.makedirs(f, exist_ok=True)

# ============ DEFAULT FAYLLAR ============
default_files = {
    "tugma/key1.txt": "🔄 Valyuta ayirboshlash",
    "tugma/key2.txt": "🔰 Hamyonlar",
    "tugma/key3.txt": "📊 Valyuta kursi",
    "tugma/key4.txt": "📞 Aloqa",
    "tugma/key5.txt": "🔁 Almashuvlar",
    "tizim/user.txt": "Kiritilmagan",
    "tizim/promo.txt": "Kiritilmagan",
    "tizim/uslug.txt": "20",
    "tizim/valyuta.txt": "so'm",
    "tizim/holat.txt": "✅",
    "tizim/support.txt": "Bot 08:00 dan 00:00 gacha ishlaydi",
    "obmen/obmen.txt": "0",
    "tizim/kurs/sotish_rub.txt": "140.00",
    "tizim/kurs/sotish_usd.txt": "12800.00",
    "tizim/kurs/sotib_rub.txt": "135.00",
    "tizim/kurs/sotib_usd.txt": "12700.00"
}
for f, c in default_files.items():
    if not file_exists(f):
        write_file(f, c)

# ============ VALYUTALAR ============
wallets = ["uzcard", "humo", "qiwi_rub", "qiwi_usd", "payeer_rub", "payeer_usd", "wmz_rub", "sberbank_rub", "tinkoff_rub"]

for w in wallets:
    path = f"tizim/hamyon/{ADMIN_ID}/{w}.txt"
    if not file_exists(path):
        write_file(path, "kiritilmagan")

# ============ MENULAR ============
key1 = read_file("tugma/key1.txt") or "🔄 Valyuta ayirboshlash"
key2 = read_file("tugma/key2.txt") or "🔰 Hamyonlar"
key3 = read_file("tugma/key3.txt") or "📊 Valyuta kursi"
key4 = read_file("tugma/key4.txt") or "📞 Aloqa"
key5 = read_file("tugma/key5.txt") or "🔁 Almashuvlar"

menu = {
    "resize_keyboard": True,
    "keyboard": [
        [{"text": key1}],
        [{"text": key2}, {"text": key3}],
        [{"text": key4}, {"text": key5}]
    ]
}

menus_admin = {
    "resize_keyboard": True,
    "keyboard": [
        [{"text": key1}],
        [{"text": key2}, {"text": key3}],
        [{"text": key4}, {"text": key5}],
        [{"text": "🗄 Boshqarish"}]
    ]
}

back = {"resize_keyboard": True, "keyboard": [[{"text": "◀️ Orqaga"}]]}

admin_panel = {
    "resize_keyboard": True,
    "keyboard": [
        [{"text": "⚙ Asosiy sozlamalar"}],
        [{"text": "📊 Statistika"}, {"text": "✉ Xabar yuborish"}],
        [{"text": "🔎 Foydalanuvchini boshqarish"}],
        [{"text": "🎛 Tugmalar"}, {"text": "🔄 Almashuv holati"}],
        [{"text": "◀️ Orqaga"}]
    ]
}

asosiy = {
    "resize_keyboard": True,
    "keyboard": [
        [{"text": "*️⃣ Birlamchi sozlamalar"}],
        [{"text": "📢 Kanallar"}, {"text": "🗄 Boshqarish"}]
    ]
}

boshqarish = {"resize_keyboard": True, "keyboard": [[{"text": "🗄 Boshqarish"}]]}

# ============ QO'SHIMCHA FUNKSIYALAR ============
def get_valyuta():
    return read_file("tizim/valyuta.txt") or "so'm"

def get_foiz():
    return float(read_file("tizim/uslug.txt") or 20)

def get_status():
    return read_file("tizim/holat.txt") or "✅"

def get_support():
    return read_file("tizim/support.txt") or "Aloqa"

def get_promo():
    return read_file("tizim/promo.txt") or ""

def get_kurs():
    return {
        "sotish_rub": float(read_file("tizim/kurs/sotish_rub.txt") or 140),
        "sotish_usd": float(read_file("tizim/kurs/sotish_usd.txt") or 12800),
        "sotib_rub": float(read_file("tizim/kurs/sotib_rub.txt") or 135),
        "sotib_usd": float(read_file("tizim/kurs/sotib_usd.txt") or 12700)
    }

def save_user(chat_id):
    if not file_exists("azo.dat"):
        write_file("azo.dat", "")
    data = read_file("azo.dat") or ""
    if str(chat_id) not in data:
        with open("azo.dat", "a", encoding="utf-8") as f:
            f.write(f"{chat_id}\n")

def is_banned(chat_id):
    return file_exists(f"ban/{chat_id}.txt")

def joinchat(chat_id):
    kanal = read_file("tizim/kanal.txt")
    if not kanal:
        return True
    lines = kanal.split("\n")
    uns = False
    keyboard = {"inline_keyboard": []}
    for line in lines:
        if "-" not in line:
            continue
        name, url = line.split("-")
        res = bot("getChatMember", {"chat_id": f"@{url}", "user_id": chat_id})
        status = res.get("result", {}).get("status", "")
        if status in ["creator", "administrator", "member"]:
            keyboard["inline_keyboard"].append([{"text": f"✅ {name}", "url": f"https://t.me/{url}"}])
        else:
            keyboard["inline_keyboard"].append([{"text": f"❌ {name}", "url": f"https://t.me/{url}"}])
            uns = True
    keyboard["inline_keyboard"].append([{"text": "🔄 Tekshirish", "callback_data": "check_sub"}])
    if uns:
        send_message(chat_id, "⚠️ <b>Botdan foydalanish uchun kanallarga obuna bo'ling:</b>", json.dumps(keyboard))
        return False
    return True

def get_admin(chat):
    url = f"https://api.telegram.org/bot{TOKEN}/getChatAdministrators?chat_id=@{chat}"
    try:
        r = requests.get(url)
        return r.json().get("ok", False)
    except:
        return False

# ============ AYIRBOSHLASH ============
def create_exchange(chat_id, from_w, to_w, amount, valyuta, foiz):
    idlar = int(read_file("obmen/obmen.txt") or 0)
    ex_id = idlar + 1
    write_file("obmen/obmen.txt", str(ex_id))
    os.makedirs(f"obmen/{ex_id}", exist_ok=True)
    komissiya = amount * foiz / 100
    jami = amount - komissiya
    write_file(f"obmen/{ex_id}/id.txt", str(ex_id))
    write_file(f"obmen/{ex_id}/egasi.txt", str(chat_id))
    write_file(f"obmen/{ex_id}/holat.txt", "♻️ Bajarilmoqda")
    write_file(f"obmen/{ex_id}/miqdor.txt", str(jami))
    write_file(f"obmen/{ex_id}/sana.txt", datetime.now().strftime("%d.%m.%Y"))
    write_file(f"obmen/{ex_id}/vaqt.txt", datetime.now().strftime("%H:%M"))
    write_file(f"obmen/{ex_id}/valyuta.txt", f"{from_w} > {to_w}")
    write_file(f"obmen/{chat_id}/miqdor.txt", str(amount))
    write_file(f"obmen/{chat_id}/fozimiqdor.txt", str(jami))
    write_file(f"obmen/{chat_id}/obid.txt", str(ex_id))
    return ex_id, jami, komissiya

# ============ HANDLERLAR ============
user_steps = {}
temp_data = {}

def handle_message(chat_id, text, username, msg_id):
    print(f"DEBUG: Xabar keldi: {text} (chat_id={chat_id})")
    if is_banned(chat_id):
        return
    if not joinchat(chat_id):
        return
    save_user(chat_id)

    step = user_steps.get(chat_id, "")
    valyuta = get_valyuta()
    kurs = get_kurs()
    status = get_status()
    foiz = get_foiz()

    if text == "/start":
        if chat_id == ADMIN_ID:
            send_message(chat_id, f"💎 <b>Salom! @{username} ga xush kelibsiz!</b>", json.dumps(menus_admin))
        else:
            send_message(chat_id, "💎 <b>Salom! Valyuta ayirboshlash botiga xush kelibsiz!</b>", json.dumps(menu))
        if chat_id in user_steps:
            del user_steps[chat_id]

    elif text == "◀️ Orqaga":
        if chat_id == ADMIN_ID:
            send_message(chat_id, "🖥 Asosiy menyu", json.dumps(menus_admin))
        else:
            send_message(chat_id, "🖥 Asosiy menyu", json.dumps(menu))
        if chat_id in user_steps:
            del user_steps[chat_id]

    elif text == key2:
        msg = "<b>💳 Sizning hamyonlaringiz:</b>\n\n"
        for w in wallets:
            val = read_file(f"tizim/hamyon/{chat_id}/{w}.txt") or "kiritilmagan"
            msg += f"📌 {w.upper()}: <code>{val}</code>\n"
        keyboard = {"inline_keyboard": [[{"text": f"➕ {w.upper()}", "callback_data": f"add_{w}"} for w in wallets[:2]]]}
        for i in range(2, len(wallets), 2):
            row = [{"text": f"➕ {wallets[i].upper()}", "callback_data": f"add_{wallets[i]}"}]
            if i+1 < len(wallets):
                row.append({"text": f"➕ {wallets[i+1].upper()}", "callback_data": f"add_{wallets[i+1]}"})
            keyboard["inline_keyboard"].append(row)
        send_message(chat_id, msg, json.dumps(keyboard))

    elif text == key3:
        msg = f"📉 Sotish:\n1 RUB = {kurs['sotish_rub']} {valyuta}\n1 USD = {kurs['sotish_usd']} {valyuta}\n\n📉 Sotib olish:\n1 RUB = {kurs['sotib_rub']} {valyuta}\n1 USD = {kurs['sotib_usd']} {valyuta}"
        send_message(chat_id, msg)

    elif text == key4:
        keyboard = {"inline_keyboard": [[{"text": "📞 Bot orqali xabar", "callback_data": "supp"}]]}
        send_message(chat_id, f"<b>{get_support()}</b>", json.dumps(keyboard))

    elif text == key5:
        send_message(chat_id, "<b>🆔 Almashuv ID'sini yuboring:</b>", json.dumps(back))
        user_steps[chat_id] = "search_exchange"

    elif text == key1:
        if status == "❌":
            send_message(chat_id, "<b>⚠️ Almashinuv jarayonlari vaqtinchalik bloklangan.</b>")
            return
        keyboard = {"inline_keyboard": []}
        for w in wallets:
            keyboard["inline_keyboard"].append([{"text": f"🔼 {w.upper()}", "callback_data": f"from_{w}"}, {"text": f"🔽 {w.upper()}", "callback_data": "error"}])
        send_message(chat_id, "<b>🔼 Berish va 🔽 Olish valyutalarini tanlang:</b>", json.dumps(keyboard))

    elif text == "🗄 Boshqarish" and chat_id == ADMIN_ID:
        print(f"DEBUG: Admin panel yuborilmoqda, chat_id={chat_id}")
        send_message(chat_id, "<b>Admin paneliga xush kelibsiz!</b>", json.dumps(admin_panel))
        if chat_id in user_steps:
            del user_steps[chat_id]

    elif step == "search_exchange":
        if os.path.exists(f"obmen/{text}/id.txt"):
            info = f"ID: {read_file(f'obmen/{text}/id.txt')}\n"
            info += f"Egasi: {read_file(f'obmen/{text}/egasi.txt')}\n"
            info += f"Holat: {read_file(f'obmen/{text}/holat.txt')}\n"
            info += f"Valyuta: {read_file(f'obmen/{text}/valyuta.txt')}\n"
            info += f"Sana: {read_file(f'obmen/{text}/sana.txt')}\n"
            info += f"Miqdor: {read_file(f'obmen/{text}/miqdor.txt')} {valyuta}"
            send_message(chat_id, f"<b>✅ Almashuv topildi:</b>\n\n{info}")
        else:
            send_message(chat_id, "<b>⚠️ Almashuv topilmadi!</b>")
        if chat_id in user_steps:
            del user_steps[chat_id]

    elif step.startswith("add_"):
        w = step.replace("add_", "")
        write_file(f"tizim/hamyon/{chat_id}/{w}.txt", text)
        send_message(chat_id, f"✅ {w.upper()} hamyon saqlandi!", json.dumps(menu))
        if chat_id in user_steps:
            del user_steps[chat_id]

    elif step.startswith("amount_"):
        if text.isdigit():
            _, from_w, to_w = step.split("_")
            amount = float(text)
            komissiya = amount * foiz / 100
            jami = amount - komissiya
            ex_id, _, _ = create_exchange(chat_id, from_w, to_w, amount, valyuta, foiz)
            user_w = read_file(f"tizim/hamyon/{chat_id}/{from_w}.txt")
            admin_w = read_file(f"tizim/hamyon/raqam/{ADMIN_ID}/{from_w}.txt")
            msg = f"✅ Qabul qilindi!\n\n🆔 ID: {ex_id}\nTuri: {from_w} > {to_w}\nBerish: {amount} {valyuta}\nOlish: {jami} {valyuta}\n💳 {from_w}: {user_w}"
            keyboard = {"inline_keyboard": [[{"text": "✅ Tasdiqlash", "callback_data": f"confirm_{ex_id}"}, {"text": "❌ Bekor", "callback_data": f"cancel_{ex_id}"}]]}
            send_message(chat_id, msg, json.dumps(keyboard))
            temp_data[chat_id] = {"from": from_w, "to": to_w, "amount": amount, "ex_id": ex_id, "jami": jami}
        else:
            send_message(chat_id, "<b>Faqat raqam kiriting!</b>")

    elif step.startswith("send_"):
        target = step.replace("send_", "")
        send_message(int(target), text)
        send_message(chat_id, "✅ Xabar yuborildi!")
        if chat_id in user_steps:
            del user_steps[chat_id]

    elif step == "contact":
        send_message(chat_id, "✅ Xabaringiz adminga yuborildi!")
        keyboard = {"inline_keyboard": [[{"text": "📝 Javob", "callback_data": f"reply_{chat_id}"}]]}
        send_message(ADMIN_ID, f"📩 Yangi xabar:\n👤 {username}\n🆔 {chat_id}\n💬 {text}", json.dumps(keyboard))
        if chat_id in user_steps:
            del user_steps[chat_id]

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

        elif text == "🎛 Tugmalar":
            keyboard = {"inline_keyboard": [[{"text": key1, "callback_data": "edit_key1"}], [{"text": key2, "callback_data": "edit_key2"}, {"text": key3, "callback_data": "edit_key3"}], [{"text": key4, "callback_data": "edit_key4"}, {"text": key5, "callback_data": "edit_key5"}]]}
            send_message(chat_id, "Tugmalardan birini tanlang:", json.dumps(keyboard))

        elif text == "🔄 Almashuv holati":
            keyboard = {"inline_keyboard": [[{"text": "☑️", "callback_data": "status_on"}, {"text": "❌", "callback_data": "status_off"}]]}
            send_message(chat_id, f"Holat: {get_status()}", json.dumps(keyboard))

        elif text == "⚙ Asosiy sozlamalar":
            send_message(chat_id, "⚙ Asosiy sozlamalar", json.dumps(asosiy))

        elif step == "find_user":
            if file_exists(f"odam/{text}.dat") or file_exists(f"tizim/hamyon/{text}"):
                ban = file_exists(f"ban/{text}.txt")
                btn = "🔕 Bandan olish" if ban else "🔔 Banlash"
                keyboard = {"inline_keyboard": [[{"text": btn, "callback_data": f"ban_{text}"}]]}
                send_message(chat_id, f"✅ Foydalanuvchi topildi!\nID: {text}", json.dumps(keyboard))
            else:
                send_message(chat_id, "❌ Topilmadi!")
            if chat_id in user_steps:
                del user_steps[chat_id]

        elif step == "broadcast":
            users = (read_file("azo.dat") or "").split("\n")
            count = 0
            for uid in users:
                if uid.strip():
                    send_message(int(uid), f"📢 <b>Xabar:</b>\n\n{text}")
                    count += 1
            send_message(chat_id, f"✅ {count} ta foydalanuvchiga yuborildi!")
            if chat_id in user_steps:
                del user_steps[chat_id]

    elif step.startswith("reply_"):
        target = step.replace("reply_", "")
        send_message(int(target), f"📩 <b>Admin javobi:</b>\n\n{text}")
        send_message(chat_id, "✅ Javob yuborildi!")
        if chat_id in user_steps:
            del user_steps[chat_id]

def handle_callback(cb_id, chat_id, msg_id, data):
    if is_banned(chat_id):
        return
    if not joinchat(chat_id):
        return

    if data == "check_sub":
        delete_message(chat_id, msg_id)
        if joinchat(chat_id):
            send_message(chat_id, "✅ Obuna tasdiqlandi!", json.dumps(menu))
        answer_callback(cb_id, "Tekshirildi")

    elif data == "supp":
        delete_message(chat_id, msg_id)
        send_message(chat_id, "📝 Murojaat matnini kiriting:", json.dumps(back))
        user_steps[chat_id] = "contact"

    elif data.startswith("add_"):
        w = data.replace("add_", "")
        delete_message(chat_id, msg_id)
        send_message(chat_id, f"➕ {w.upper()} raqamini kiriting:", json.dumps(back))
        user_steps[chat_id] = f"add_{w}"

    elif data.startswith("from_"):
        from_w = data.replace("from_", "")
        keyboard = {"inline_keyboard": []}
        for w in wallets:
            if w != from_w:
                keyboard["inline_keyboard"].append([{"text": f"🔽 {w.upper()}", "callback_data": f"to_{from_w}_{w}"}])
        delete_message(chat_id, msg_id)
        send_message(chat_id, f"🔼 {from_w.upper()} dan qaysi valyutaga?", json.dumps(keyboard))

    elif data.startswith("to_"):
        _, from_w, to_w = data.split("_")
        user_w = read_file(f"tizim/hamyon/{chat_id}/{from_w}.txt")
        admin_w = read_file(f"tizim/hamyon/raqam/{ADMIN_ID}/{from_w}.txt")
        if user_w == "kiritilmagan" or not user_w:
            answer_callback(cb_id, f"⚠️ Avval {from_w.upper()} hamyon kiriting!", True)
            return
        if admin_w == "kiritilmagan" or not admin_w:
            answer_callback(cb_id, "⚠️ Admin hamyoni kiritilmagan!", True)
            return
        edit_message(chat_id, msg_id, f"🔄 {from_w.upper()} > {to_w.upper()}\n\n💳 Siz: {user_w}\n💳 Admin: {admin_w}\n\nSummani kiriting:", json.dumps(back))
        user_steps[chat_id] = f"amount_{from_w}_{to_w}"

    elif data.startswith("confirm_"):
        ex_id = data.replace("confirm_", "")
        delete_message(chat_id, msg_id)
        send_message(chat_id, "📸 To'lov chekini yuboring:", json.dumps(back))
        user_steps[chat_id] = f"check_{ex_id}"

    elif data.startswith("cancel_"):
        ex_id = data.replace("cancel_", "")
        delete_message(chat_id, msg_id)
        send_message(chat_id, "❌ Almashuv bekor qilindi!", json.dumps(menu))

    elif data.startswith("check_"):
        ex_id = data.replace("check_", "")
        user_id = read_file(f"obmen/{ex_id}/egasi.txt")
        if user_id:
            send_message(ADMIN_ID, f"🆕 To'lov keldi!\nID: {ex_id}\nFoydalanuvchi: {user_id}")
            send_message(chat_id, "✅ To'lov ma'lumotingiz yuborildi!")

    elif data.startswith("ban_"):
        target = data.replace("ban_", "")
        if file_exists(f"ban/{target}.txt"):
            os.remove(f"ban/{target}.txt")
            send_message(chat_id, f"✅ {target} bandan olindi!")
        else:
            write_file(f"ban/{target}.txt", "ban")
            send_message(chat_id, f"✅ {target} banlandi!")
        delete_message(chat_id, msg_id)

    elif data == "status_on":
        write_file("tizim/holat.txt", "✅")
        edit_message(chat_id, msg_id, "Holat: ✅", json.dumps({"inline_keyboard": [[{"text": "☑️", "callback_data": "status_on"}, {"text": "❌", "callback_data": "status_off"}]]}))

    elif data == "status_off":
        write_file("tizim/holat.txt", "❌")
        edit_message(chat_id, msg_id, "Holat: ❌", json.dumps({"inline_keyboard": [[{"text": "☑️", "callback_data": "status_on"}, {"text": "❌", "callback_data": "status_off"}]]}))

    elif data.startswith("reply_"):
        target = data.replace("reply_", "")
        delete_message(chat_id, msg_id)
        send_message(chat_id, "Javobingizni yozing:", json.dumps(back))
        user_steps[chat_id] = f"reply_{target}"

    elif data.startswith("edit_key"):
        num = data.replace("edit_key", "")
        delete_message(chat_id, msg_id)
        send_message(chat_id, "Yangi nom yuboring:", json.dumps(back))
        user_steps[chat_id] = f"edit_{num}"

    elif chat_id == ADMIN_ID:
        if data == "key1" or data == "key2" or data == "key3" or data == "key4" or data == "key5":
            delete_message(chat_id, msg_id)
            send_message(chat_id, "Yangi nom yuboring:", json.dumps(back))
            user_steps[chat_id] = f"edit_{data}"

    answer_callback(cb_id, "")

# ============ POLLING LOOP ============
def main():
    print("🚀 Bot ishga tushdi!")
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
            print(f"Xatolik: {e}\n{traceback.format_exc()}")
            time.sleep(5)

if __name__ == "__main__":
    main()
