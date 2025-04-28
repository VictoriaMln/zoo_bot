import config, logging, quiz
from quiz import format_question
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


START_KEYBOARD = ReplyKeyboardMarkup(
    [["▶️ Начать викторину"]],
    resize_keyboard=True,
    one_time_keyboard=False
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        welcome_text = (
            "🐾 *Добро пожаловать в викторину Московского зоопарка!* 🦁\n"
            "Нажми ▶️ «Начать викторину», чтобы узнать своё тотемное животное."
        )
        await update.message.reply_text(welcome_text, reply_markup=START_KEYBOARD, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Ошибка: {e}")

async def start_quiz_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Отлично, давай начнём!",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.clear()
    context.user_data["scores"] = {}
    context.user_data["current_q"] = 0

    text, markup = format_question(0)
    sent = await update.message.reply_text(text, reply_markup=markup)

    context.user_data["quiz_chat_id"] = sent.chat.id
    context.user_data["quiz_message_id"] = sent.message_id


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()

        if query.data == "program_info":
            program_text = """
             🐾 <b>Программа опеки животных</b> 🐾\n
    Став опекуном животного, ты помогаешь не только нашему зоопарку, но и сохранению биоразнообразия на планете. 
    📈 К 2050 году может исчезнуть до 10 000 видов, и каждый опекун — это вклад в их защиту.
    С 1864 года наши друзья-опекуны объединены в <b>Клуб друзей Московского зоопарка</b>. 
    Участие в нём даёт:
      • Персональный сертификат опекуна 🎟️
      • Регулярные отчёты о жизни твоего питомца 📸
      • Приглашения на закрытые мероприятия и кормления 🦁\n
      ✉️ Наша почта: zoo@moscowzoo.ru
      🌐 Сайт: https://moscowzoo.ru/about/guardianship
            """
            await query.message.edit_text(program_text, parse_mode="HTML")

        elif query.data == "restart":
            old_msg_id = context.user_data.get("quiz_message_id")
            if old_msg_id:
                try:
                    await context.bot.delete_message(
                        chat_id=query.message.chat.id,
                        message_id=old_msg_id
                    )
                except Exception:
                    pass
            context.user_data.clear()
            context.user_data["scores"] = {}
            context.user_data["current_q"] = 0

            text, markup = format_question(0)
            sent = await context.bot.send_message(
                chat_id=query.message.chat.id,
                text=text,
                reply_markup=markup
            )
            context.user_data["quiz_chat_id"] = sent.chat.id
            context.user_data["quiz_message_id"] = sent.message_id
        elif query.data == "feedback":
            context.user_data["awaiting_feedback"] = True
            await query.message.edit_text(
                "📝 Оставь свой отзыв о викторине!"
            )
        elif query.data.startswith("0:") or query.data.split(":")[0].isdigit():
            await quiz.process_answer(update, context)
        elif query.data == "contact":
            user = update.effective_user
            scores = context.user_data.get("scores", {})
            result = max(scores, key=scores.get) if scores else "— не определено —"

            text_to_staff = (
                f"*Новый запрос от участника викторины*\n\n"
                f"Пользователь: [{user.name}](tg://user?id={user.id})\n"
                f"ID: '{user.id}'\n"
                f"Результат викторины: *{result}*"
            )
            await context.bot.send_message(
                chat_id=config.STAFF_CHAT_ID,
                text=text_to_staff,
                parse_mode="Markdown"
            )
            await query.message.edit_text(
            "✅ Я передал твой запрос сотрудникам зоопарка. "
            "Они свяжутся с тобой в ближайшее время!\n\n",
            parse_mode="Markdown"
            )

    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await quiz.safe_reply(query.message, "⚠️ Произошла ошибка")

def main():
    try:
        app = ApplicationBuilder().token(config.BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.Regex(r"^▶️ Начать викторину$"), start_quiz_button))
        app.add_handler(CallbackQueryHandler(button_handler))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, feedback_handler))

        logger.info("Бот запущен")
        app.run_polling()

    except Exception as e:
        logger.critical(f"Фатальная ошибка: {e}")

async def feedback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_feedback"):
        feedback = update.message.text
        user = update.effective_user
        text_to_staff = (
            f"💬 *Новый отзыв от {user.full_name}* (ID {user.id}):\n\n"
            f"{feedback}"
        )

        await context.bot.send_message(
            chat_id=config.STAFF_CHAT_ID,
            text=text_to_staff,
            parse_mode="Markdown"
        )

        await update.message.reply_text("🙏 Спасибо за отзыв!")
        context.user_data["awaiting_feedback"] = False
    else:
        pass
if __name__ == '__main__':
    main()
