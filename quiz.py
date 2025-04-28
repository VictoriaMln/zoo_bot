import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import config
from urllib.parse import quote

logger = logging.getLogger(__name__)

# ID стикеров с животными
STICKERS = {
    "Камышовый кот": "CAACAgIAAxkBAAICIWgKDryuMVR9TtmPmaVWcCHBGIklAAKxdwAC5F1ISO5lYgIOGAtJNgQ",
    "Гривистый волк": "CAACAgIAAxkBAAICGWgKDm1oJJMM_Wex8Nd6htaH7SduAALRawAC4rVRSMV3wTQoE8tCNgQ",
    "Викунья": "CAACAgIAAxkBAAICG2gKDovjWafo36pYL9ZKDJ-tP7cxAAIoeAACTctISH3ASkGKw_5mNgQ",
    "Большой тукан": "CAACAgIAAxkBAAICHWgKDp5Xardl-dr-kXEVUTMfRvlXAAJTdQACzDpQSIBSIgvmV02GNgQ",
    "Альпака": "CAACAgIAAxkBAAICI2gKDslnvRUtJnkhGPabtonzdHOtAAKGeAACKeNQSOO87I5S1Yu0NgQ",
    "Зебра Греви": "CAACAgIAAxkBAAICF2gKDZ2KR9v_IigtO5rvFScsH5aIAAKYeAACVDxJSAABNsEPDcktAAE2BA",
    "Азиатский слон": "CAACAgIAAxkBAAICH2gKDq3yEqZTf--J4ur5CtuBuFGsAAItawACsIVQSDkOT9iro_4GNgQ"
}

# Ссылка на бот для возможности поделиться результатами
BOT_LINK = f"https://t.me/{config.BOT_USERNAME}"

# Вопросы викторины
QUESTIONS = [
    {
        "question": "Твой идеальный отпуск проходит...",
        "options": [
            {"text": "У водоёмов: плаванье, ныряние, брызги!", "scores": {"Камышовый кот": 2, "Большой тукан": 1}},
            {"text": "В бескрайних равнинах с видом на горизонт", "scores": {"Гривистый волк": 2, "Зебра Греви": 1}},
            {"text": "Среди горных вершин и чистого воздуха", "scores": {"Викунья": 2, "Азиатский слон": 1}},
            {"text": "На наблюдательном пункте с панорамным видом", "scores": {"Азиатский слон": 2, "Гривистый волк": 1}}
        ]
    },
    {
        "question": "Твоё хобби — это...",
        "options": [
            {"text": "Искать уютные потаённые уголки", "scores": {"Камышовый кот": 2, "Гривистый волк": 1}},
            {"text": "Обозначать границы своих владений", "scores": {"Гривистый волк": 2, "Зебра Греви": 1}},
            {"text": "Наслаждаться сочной горной растительностью", "scores": {"Викунья": 2, "Альпака": 1}},
            {"text": "Размеренно двигаться по любимым маршрутам", "scores": {"Азиатский слон": 2, "Зебра Греви": 1}}
        ]
    },
    {
        "question": "Твои кулинарные предпочтения:",
        "options": [
            {"text": "Энергичная охота за свежей добычей", "scores": {"Камышовый кот": 2, "Большой тукан": 1}},
            {"text": "Сладкий фуршет из сезонных плодов", "scores": {"Большой тукан": 2, "Гривистый волк": 1}},
            {"text": "Нежное сбалансированное питание", "scores": {"Альпака": 2, "Викунья": 1}},
            {"text": "Величественный пир на весь мир", "scores": {"Азиатский слон": 2, "Зебра Греви": 1}}
        ]
    },
    {
        "question": "Твоя суперсила — это...",
        "options": [
            {"text": "Водная стихия: как рыба в воде!", "scores": {"Камышовый кот": 2, "Большой тукан": 1}},
            {"text": "Радар для мельчайших звуков", "scores": {"Гривистый волк": 2, "Камышовый кот": 1}},
            {"text": "Искусство создания социальных связей", "scores": {"Азиатский слон": 2, "Викунья": 1}},
            {"text": "Неповторимый внешний вид", "scores": {"Зебра Греви": 2, "Большой тукан": 1}}
        ]
    },
    {
        "question": "Звук, лучше всего передающий твоё настроение:",
        "options": [
            {"text": "Кошачье мурлыканье с шипящим акцентом", "scores": {"Камышовый кот": 2}},
            {"text": "Басовитое уханье лесного сторожа", "scores": {"Гривистый волк": 2}},
            {"text": "Мелодичное посвистывание на ветру", "scores": {"Викунья": 2, "Большой тукан": 1}},
            {"text": "Торжественная симфония джунглей", "scores": {"Азиатский слон": 2}}
        ]
    },
    {
        "question": "Какие ассоциации ты обычно вызываешь у друзей?",
        "options": [
            {"text": "Олицетворение домашнего тепла и уюта", "scores": {"Альпака": 2, "Викунья": 1}},
            {"text": "Ходячая энциклопедия экзотики", "scores": {"Большой тукан": 2}},
            {"text": "Символ неутомимого странника", "scores": {"Зебра Греви": 2, "Гривистый волк": 1}},
            {"text": "Воплощение природной мудрости", "scores": {"Азиатский слон": 2}}
        ]
    },
    {
        "question": "Если бы ты стал супергероем, твоя сила:",
        "options": [
            {"text": "Маскировка в любой среде", "scores": {"Камышовый кот": 2}},
            {"text": "Орлиное зрение на дистанции", "scores": {"Гривистый волк": 1, "Зебра Греви": 1}},
            {"text": "Невероятные возможности адаптации к любым условиям", "scores": {"Викунья": 2, "Альпака": 1}},
            {"text": "Контроль над стихиями природы", "scores": {"Азиатский слон": 1, "Большой тукан": 1}}
        ]
    },
    {
        "question": "Что тебя заряжает энергией?",
        "options": [
            {"text": "Адреналин от активности и игр", "scores": {"Камышовый кот": 1, "Гривистый волк": 2}},
            {"text": "Болтовня с ярким аккомпанементом", "scores": {"Большой тукан": 2}},
            {"text": "Уют тактильного комфорта", "scores": {"Альпака": 2}},
            {"text": "Сила коллектива и традиций", "scores": {"Азиатский слон": 2, "Зебра Греви": 1}}
        ]
    }
]

def format_question(q_idx: int) -> (str, InlineKeyboardMarkup):
    q = QUESTIONS[q_idx]
    opts = "\n".join(f"{i+1}.{opt['text']}" for i, opt in enumerate(q["options"]))
    text = (
        f"Вопрос {q_idx+1}/{len(QUESTIONS)}\n\n"
        f"{q['question']}\n\n"
        f"{opts}"
    )
    buttons = [
        [InlineKeyboardButton(f"{i + 1}", callback_data=f"{q_idx}:{i}")]
        for i in range(len(q["options"]))
    ]
    return text, InlineKeyboardMarkup(buttons)
async def safe_reply(message, text, reply_markup=None, parse_mode=None):
    try:
        await message.reply_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения: {e}")

def get_top_animals(scores):
    if not scores:
        return []
    max_score = max(scores.values())
    return [animal for animal, score in scores.items() if score == max_score]

async def advance_question(update, context, q_idx: int):
    chat_id = context.user_data["quiz_chat_id"]
    msg_id = context.user_data["quiz_message_id"]

    if q_idx >= len(QUESTIONS):
        await send_result(chat_id, msg_id, context)
        return

    text, markup = format_question(q_idx)

    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=msg_id,
        text=text,
        reply_markup=markup
    )
    context.user_data["current_q"] = q_idx

async def process_answer(update, context):
    try:
        query = update.callback_query
        await query.answer()

        q_idx, a_idx = map(int, query.data.split(":"))
        opt = QUESTIONS[q_idx]["options"][a_idx]

        scores = context.user_data.setdefault('scores', {})
        for animal, pts in opt['scores'].items():
            scores[animal] = scores.get(animal, 0) + pts

        await advance_question(update, context, q_idx + 1)

    except Exception as e:
        logger.error(f"Ошибка: {e}", exc_info=True)
        await query.message.reply_text("⚠️ Ошибка обработки ответа. Попробуй ещё раз /start")

async def send_result(chat_id, msg_id, context):
    scores = context.user_data.get("scores", {})

    if not scores:
        result_animal = "— не определено —"
        result_text = "Не удалось определить животное😪 Попробуй ещё раз!"
        sticker_id = None
    else:
        top_animals = get_top_animals(scores)
        result_animal = random.choice(top_animals)
        result_text = f"🎉Твое тотемное животное в Московском зоопарке: *{result_animal}*!"
        sticker_id = STICKERS.get(result_animal)

    if sticker_id:
        await context.bot.send_sticker(chat_id=chat_id, sticker=sticker_id)

    raw = f"Моё тотемное животное в Московском зоопарке - {result_animal}! Пройди викторину и узнай своё. "
    enc = quote(raw, safe='')
    enc_link = quote(config.BOT_LINK, safe='')

    share_buttons = [
        [InlineKeyboardButton(" Telegram", url=f"https://t.me/share/url?url={enc_link}&text={enc}")],
        [InlineKeyboardButton(" WhatsApp", url=f"https://api.whatsapp.com/send?text={enc}")],
        [InlineKeyboardButton(" VK", url=f"https://vk.com/share.php?url={enc_link}&title={enc}")],
        [InlineKeyboardButton(" Facebook", url=f"https://www.facebook.com/sharer/sharer.php?u={enc_link}&quote={enc}")],
    ]

    share_buttons += [
        [InlineKeyboardButton("⁉️Узнать больше о программе опеки", callback_data="program_info")],
        [InlineKeyboardButton("✏️ Оставить отзыв", callback_data="feedback")],
        [InlineKeyboardButton("🔄Попробовать ещё раз", callback_data="restart")],
        [InlineKeyboardButton("📞 Связаться с сотрудником", callback_data="contact")]
    ]
    markup = InlineKeyboardMarkup(share_buttons)

    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=msg_id,
        text=result_text,
        reply_markup=markup,
        parse_mode="Markdown"
    )
