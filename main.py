import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# التوكن الخاص بك
TOKEN = "8936817987:AAH5dGFi9q9VFWr3VUR_pHJA-NtyXCNTvOQ"

# معرف قناتك
CHANNEL_USERNAME = "@shbin4"

bot = telebot.TeleBot(TOKEN)

# دالة للتحقق من اشتراك العضو
def is_user_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['creator', 'administrator', 'member']:
            return True
        return False
    except Exception as e:
        print(f"خطأ في فحص الاشتراك: {e}")
        return False

# فحص كل رسالة في القروب
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'document', 'sticker'])
def check_group_message(message):
    if message.chat.type in ['group', 'supergroup']:
        user_id = message.from_user.id
        
        # إذا كان غير مشترك
        if not is_user_subscribed(user_id):
            try:
                # حذف رسالته من القروب
                bot.delete_message(message.chat.id, message.message_id)
                
                # زر الاشتراك
                markup = InlineKeyboardMarkup()
                channel_link = f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}"
                btn = InlineKeyboardButton("📢 اضغط هنا للاشتراك في القناة", url=channel_link)
                markup.add(btn)
                
                # تنبيه العضو
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
