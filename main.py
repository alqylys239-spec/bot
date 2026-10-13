import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# تشغيل سيرفر وهمي لإرضاء موقع Render
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running successfully!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# بدء سيرفر الويب في خلفية النظام
threading.Thread(target=run_web_server, daemon=True).start()

# بيانات البوت والقناة
TOKEN = "8936817987:AAH5dGFi9q9VFWr3VUR_pHJA-NtyXCNTvOQ"
CHANNEL_USERNAME = "@shbin4"

bot = telebot.TeleBot(TOKEN)

def is_user_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['creator', 'administrator', 'member']:
            return True
        return False
    except Exception as e:
        print(f"خطأ في فحص الاشتراك: {e}")
        return False

@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'document', 'sticker'])
def check_group_message(message):
    if message.chat.type in ['group', 'supergroup']:
        user_id = message.from_user.id
        
        if not is_user_subscribed(user_id):
            try:
                bot.delete_message(message.chat.id, message.message_id)
                
                markup = InlineKeyboardMarkup()
                channel_link = f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}"
                btn = InlineKeyboardButton("📢 اضغط هنا للاشتراك في القناة", url=channel_link)
                markup.add(btn)
                
                user_name = message.from_user.first_name
                warning_msg = f"عذراً [{user_name}](tg://user?id={user_id}) ⚠️\n\nلا يمكنك النشر في القروب حتى تشترك في القناة أولاً!\nاشترك ثم أعد إرسال رسالتك."
                
                bot.send_message(
                    message.chat.id, 
                    warning_msg, 
                    reply_markup=markup, 
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"خطأ: {e}")

print("البوت يعمل الان بنجاح...")
bot.infinity_polling()
