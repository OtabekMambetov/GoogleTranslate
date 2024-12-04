from googletrans import Translator
from aiogram import executor, types, Bot, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import logging

# Telegram bot tokeni
API_TOKEN = "7528776801:AAFBQCsd_E7uXWxDRyyLhHZ8CqXNHymDe2s"

# Loglashni sozlash
logging.basicConfig(level=logging.INFO)

# Bot va dispatcherni ishga tushirish
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
translator = Translator()

# Tarjima qilish uchun tilni tanlash tugmalari
language_buttons = ReplyKeyboardMarkup(resize_keyboard=True)

# Qo'shilgan tillar
languages = {
    "🇬🇧 English (UK)": "en",  # Ingliz tili (Buyuk Britaniya)
    "🇷🇺 Русский": "ru",       # Rus tili
    "🇺🇿 O'zbekcha": "uz",     # O‘zbek tili
    "🇫🇷 Français": "fr",      # Fransuz tili
    "🇰🇷 한국어 (Korean)": "ko", # Koreys tili
    "🇨🇳 中文 (Chinese)": "zh-cn", # Xitoy tili
    "🇮🇳 हिन्दी (Hindi)": "hi",   # Hind tili
    "🇰🇿 Қазақша": "kk",        # Qozoq tili
    "🇺🇦 Українська": "uk",     # Ukrain tili
    "🇦🇪 العربية": "ar",         # Arab tili
    "🇩🇪 Deutsch": "de",        # Nemis tili
    "🇪🇸 Español": "es",        # Ispan tili
    "🇮🇹 Italiano": "it",       # Italyan tili
    "🇯🇵 日本語 (Japanese)": "ja", # Yapon tili
    "🇹🇷 Türkçe": "tr",  # Turkiy tili

}
language_buttons.row(
    KeyboardButton("🇬🇧 English (UK)"),
    KeyboardButton("🇷🇺 Русский"),
    KeyboardButton("🇺🇿 O'zbekcha")
)
language_buttons.row(
    KeyboardButton("🇫🇷 Français"),
    KeyboardButton("🇰🇷 한국어 (Korean)"),
    KeyboardButton("🇨🇳 中文 (Chinese)")
)
language_buttons.row(
    KeyboardButton("🇮🇳 हिन्दी (Hindi)"),
    KeyboardButton("🇰🇿 Қазақша"),
    KeyboardButton("🇺🇦 Українська")
)
language_buttons.row(
    KeyboardButton("🇦🇪 العربية"),
    KeyboardButton("🇩🇪 Deutsch"),
    KeyboardButton("🇪🇸 Español")
)
language_buttons.row(
    KeyboardButton("🇮🇹 Italiano"),
    KeyboardButton("🇯🇵 日本語 (Japanese)")
)

# Tugmalarni yaratish
for lang_name in languages.keys():
    language_buttons.add(KeyboardButton(lang_name))

# Foydalanuvchi tanlagan tilni saqlash uchun lug‘at
user_languages = {}

# "/start" va "/help" buyruqlariga javob
@dp.message_handler(commands=["start", "help"])
async def start(message: types.Message):
    await message.answer(
        "Assalomu alaykum! Botimizga xush kelibsiz. 😊\n"
        "Matningizni boshqa tillarga tarjima qilish uchun avval tilni tanlang.",
        reply_markup=language_buttons
    )

# Foydalanuvchi tilni tanlaydi
@dp.message_handler(lambda message: message.text in languages)
async def set_language(message: types.Message):
    # Tanlangan tilni foydalanuvchi uchun saqlash
    user_languages[message.from_user.id] = languages[message.text]
    await message.reply(f"Til tanlandi: {message.text}. Endi matningizni yuboring!")

# Tarjima qilish funksiyasi
@dp.message_handler()
async def translate_text(message: types.Message):
    # Agar foydalanuvchi tilni tanlamagan bo‘lsa, standart til — ingliz tili
    user_language = user_languages.get(message.from_user.id, "en")
    try:
        # Matnni foydalanuvchi tanlagan tilga tarjima qilish
        translation = translator.translate(message.text, dest=user_language)
        translated_text = translation.text
        await message.reply(f"Tarjima ({user_language}): {translated_text}")
    except Exception as e:
        # Agar xatolik yuz bersa, foydalanuvchiga xabar berish
        await message.reply("Uzr, tarjima qilishda xatolik yuz berdi. Qayta urinib ko‘ring.")

# Botni ishga tushirish
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
