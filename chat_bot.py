from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, CallbackQueryHandler, filters
import random
import asyncio

# توکن ربات
TOKEN = '7824206393:AAH_gQdsmc7RMGhDt5nS3JPOZdA2sY4H2RA'

# صف کاربران در انتظار بر اساس جنسیت
waiting_girls = []
waiting_boys = []
waiting_users = []
active_chats = {}
chat_timers = {}

# شروع ربات - نسخه زیباتر و حرفه‌ای
async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    first_name = user.first_name if user.first_name else "ناشناس"

    welcome_message = f"""
👋 سلام {first_name} عزیز،

🕊️ به ربات چت ناشناس خوش اومدی!  
اینجا می‌تونی بدون اینکه کسی هویتت رو بفهمه، با افراد جدید چت کنی ✨

📩 برای شروع، یکی از گزینه‌های زیر رو انتخاب کن:
"""

    keyboard = [
        [InlineKeyboardButton("👧 جست‌وجوی دختر", callback_data='search_girl')],
        [InlineKeyboardButton("👦 جست‌وجوی پسر", callback_data='search_boy')],
        [InlineKeyboardButton("🔍 شروع چت تصادفی", callback_data='random_chat')],
        [InlineKeyboardButton("❌ پایان چت", callback_data='end_chat')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# وقتی کاربر روی "شروع چت تصادفی" کلیک می‌کنه
async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()

    if query.data == 'search_girl':
        if user_id in active_chats:
            await query.edit_message_text("⚠️ شما در حال حاضر در یک چت هستید. برای پایان، دکمه ❌ را بزنید.")
            return

        if waiting_girls and waiting_girls[0] != user_id:
            partner_id = waiting_girls.pop(0)
            active_chats[user_id] = partner_id
            active_chats[partner_id] = user_id

            await context.bot.send_message(chat_id=user_id, text="✅ شما به یک دختر متصل شدید. ناشناس باشید و مودب 😉")
            await context.bot.send_message(chat_id=partner_id, text="✅ یک پسر برای چت پیدا شد. خوش بگذره 😊")
            start_timer(user_id, partner_id)

        else:
            waiting_girls.append(user_id)
            await query.edit_message_text("⏳ در حال جست‌وجوی دختر هستید... لطفاً منتظر بمانید.")

    elif query.data == 'search_boy':
        if user_id in active_chats:
            await query.edit_message_text("⚠️ شما در حال حاضر در یک چت هستید. برای پایان، دکمه ❌ را بزنید.")
            return

        if waiting_boys and waiting_boys[0] != user_id:
            partner_id = waiting_boys.pop(0)
            active_chats[user_id] = partner_id
            active_chats[partner_id] = user_id

            await context.bot.send_message(chat_id=user_id, text="✅ شما به یک پسر متصل شدید. ناشناس باشید و مودب 😉")
            await context.bot.send_message(chat_id=partner_id, text="✅ یک دختر برای چت پیدا شد. خوش بگذره 😊")
            start_timer(user_id, partner_id)

        else:
            waiting_boys.append(user_id)
            await query.edit_message_text("⏳ در حال جست‌وجوی پسر هستید... لطفاً منتظر بمانید.")

    elif query.data == 'random_chat':
        if user_id in active_chats:
            await query.edit_message_text("⚠️ شما در حال حاضر در یک چت هستید. برای پایان، دکمه ❌ را بزنید.")
            return

        if waiting_users and waiting_users[0] != user_id:
            partner_id = waiting_users.pop(0)
            active_chats[user_id] = partner_id
            active_chats[partner_id] = user_id

            await context.bot.send_message(chat_id=user_id, text="✅ شما به یک نفر متصل شدید. ناشناس باشید و مودب 😉")
            await context.bot.send_message(chat_id=partner_id, text="✅ یک کاربر برای چت پیدا شد. خوش بگذره 😊")
            start_timer(user_id, partner_id)

        else:
            waiting_users.append(user_id)
            await query.edit_message_text("⏳ در حال جست‌وجوی کاربر دیگر هستید... لطفاً منتظر بمانید.")

    elif query.data == 'end_chat':
        partner_id = active_chats.pop(user_id, None)
        if partner_id:
            active_chats.pop(partner_id, None)
            cancel_timer(user_id)
            cancel_timer(partner_id)
            await context.bot.send_message(chat_id=partner_id, text="❌ چت توسط طرف مقابل پایان یافت.")
            await context.bot.send_message(chat_id=user_id, text="✅ چت پایان یافت.")
        else:
            await context.bot.send_message(chat_id=user_id, text="⛔ شما در هیچ چتی نیستید.")

# چت ناشناس - پاسخ زیباتر
async def anonymous_chat(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    if user_id in active_chats:
        partner_id = active_chats[user_id]
        await context.bot.send_message(chat_id=partner_id, text=f"💬 ناشناس:\n{update.message.text}")
    else:
        await update.message.reply_text("❗ هنوز به کسی متصل نیستید. روی 'شروع چت 🔍' بزنید.")

# شروع تایمر برای قطع چت بعد از مدت معین
def start_timer(user_id, partner_id):
    async def timeout():
        if user_id in active_chats and partner_id in active_chats:
            await active_chats.pop(user_id, None)
            await active_chats.pop(partner_id, None)
            await active_chats.get(user_id).send_message("⏰ زمان چت تمام شد و ارتباط قطع شد.")
            await active_chats.get(partner_id).send_message("⏰ زمان چت تمام شد و ارتباط قطع شد.")

    chat_timers[user_id] = asyncio.create_task(timeout())
    chat_timers[partner_id] = asyncio.create_task(timeout())

# لغو تایمر در صورت پایان چت
def cancel_timer(user_id):
    if user_id in chat_timers:
        chat_timers[user_id].cancel()
        del chat_timers[user_id]

# تنظیمات و شروع ربات
def main():
    application = Application.builder().token(TOKEN).build()

    # اضافه کردن هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anonymous_chat))
    application.add_handler(CallbackQueryHandler(button_handler))

    # شروع polling
    application.run_polling()

if __name__ == '__main__':
    main()
