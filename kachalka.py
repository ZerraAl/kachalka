from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import os
TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Список задач по дням
tasks = [
    "Девочки, сегодня качаем жопу. И чтоб каждая по кружку сообразила. БЫРА",
    "Прессуха для братухи. Ножницы для нежных дам",
    "Тельце больное свое качнули... пора и за мозговую мышцу брацца"
]

user_status = {}  
day_index = 0     

# Функция отправки сообщений
async def send_daily_message(context: ContextTypes.DEFAULT_TYPE):
    global day_index
    message = tasks[day_index % len(tasks)]
    for chat_id, active in user_status.items():
        if active:
            await context.bot.send_message(chat_id=chat_id, text=message)
    day_index += 1

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_status[chat_id] = True  
    keyboard = [
        [
            InlineKeyboardButton("турн он нах", callback_data="on"),
            InlineKeyboardButton("ня.пока", callback_data="off")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет, кто здесь в качалке самый главный? 💪 БУМ ОПУЩЕН. Теперь я буду говорить шо делать.",
        reply_markup=reply_markup
    )

# Обработка кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    if query.data == "on":
        user_status[chat_id] = True
        await query.edit_message_text("Напоминания активированы")
    elif query.data == "off":
        user_status[chat_id] = False
        await query.edit_message_text("Напоминания отключены")

# Основной запуск
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    # Планировщик на 9:00 утра
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_daily_message, "cron", hour=9, minute=0, args=[app])
    scheduler.start()

    print("Бот запущен!")
    app.run_polling()  

if __name__ == "__main__":
    main()
