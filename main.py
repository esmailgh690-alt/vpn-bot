
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import asyncio

TOKEN = "8754323678:AAH8PJBEyxkGe3K5dvJvEehp2nTnO-utxe8"
ADMIN_ID = 6400775424

CARD_INFO = """
💳 شماره کارت:
5022 2915 9897 9472

👤 به نام:
اسماعیل غلامی نژادماسوله
"""

PLANS = """
⭕️ قیمت کانفیگ ها

🌏 1GB — 270000T
🌍 2GB — 530000T
🌍 3GB — 790000T
🌏 4GB — 1000000T
🌍 5GB — 1200000T
🪐 10GB — 2180000T
"""

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💰 خرید اشتراک")],
        [KeyboardButton(text="📋 تعرفه ها")],
        [KeyboardButton(text="📞 پشتیبانی")]
    ],
    resize_keyboard=True
)

waiting_users = set()

@dp.message(CommandStart())
async def start(message: types.Message):
    text = """
سلام 👋
به ربات فروش VPN خوش اومدی.
از منوی زیر انتخاب کن 👇
"""
    await message.answer(text, reply_markup=menu)

@dp.message()
async def handler(message: types.Message):
    user_id = message.from_user.id

    if message.text == "📋 تعرفه ها":
        await message.answer(PLANS)

    elif message.text == "📞 پشتیبانی":
        await message.answer("برای پشتیبانی به ادمین پیام بده.")

    elif message.text == "💰 خرید اشتراک":
        waiting_users.add(user_id)

        text = f"""
{PLANS}

{CARD_INFO}

✅ بعد از واریز، عکس رسید را ارسال کن.
"""
        await message.answer(text)

    elif message.photo and user_id in waiting_users:
        caption = f"""
📥 سفارش جدید

👤 آیدی کاربر:
<code>{user_id}</code>

✉️ یوزرنیم:
@{message.from_user.username}
"""

        await bot.send_photo(
            ADMIN_ID,
            photo=message.photo[-1].file_id,
            caption=caption
        )

        await message.answer(
            "✅ رسید شما ارسال شد."
بعد از تایید، کانفیگ برایتان فرستاده می‌شود."
       " )

        waiting_users.remove(user_id)

    else:
        await message.answer("از منوی زیر استفاده کن 👇")

async def main():
    print("Bot Started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
