import asyncio
import os
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
CHANNEL = os.getenv("CHANNEL")

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_orders = {}

# بررسی عضویت
async def is_member(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# منوی اصلی
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 خرید اشتراک", callback_data="buy")],
        [InlineKeyboardButton(text="📦 سرویس های من", callback_data="my")],
        [InlineKeyboardButton(text="🛠 پشتیبانی", url=f"https://t.me/{ADMIN_ID.replace('@','')}")]
    ])

# پلن‌ها
def plans_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("1GB - 270k", callback_data="plan_1")],
        [InlineKeyboardButton("2GB - 530k", callback_data="plan_2")],
        [InlineKeyboardButton("3GB - 790k", callback_data="plan_3")],
        [InlineKeyboardButton("4GB - 1M", callback_data="plan_4")],
        [InlineKeyboardButton("5GB - 1.2M", callback_data="plan_5")],
        [InlineKeyboardButton("10GB - 2.18M", callback_data="plan_10")]
    ])

def pay_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("💰 پرداخت و دریافت سرویس", callback_data="pay")],
        [InlineKeyboardButton("🏡 بازگشت", callback_data="home")]
    ])

def after_pay():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("🪪 دریافت شماره کارت", url=f"https://t.me/{ADMIN_ID.replace('@','')}")],
        [InlineKeyboardButton("📸 ارسال رسید", callback_data="send_receipt")]
    ])

# /start
@dp.message(Command("start"))
async def start(msg: types.Message):

    if not await is_member(msg.from_user.id):
        await msg.answer("❗ برای استفاده باید عضو کانال باشید:\n@xvpnconfigs")
        return

    await msg.answer("به ربات خوش آمدید 👇", reply_markup=main_menu())

# کلیک دکمه‌ها
@dp.callback_query()
async def cb(call: types.CallbackQuery):

    uid = call.from_user.id

    # خرید
    if call.data == "buy":
        text = """📦 لیست سرویس‌ها:

1GB - 270,000
2GB - 530,000
3GB - 790,000
4GB - 1,000,000
5GB - 1,200,000
10GB - 2,180,000

⏳ 30 روز"""
        await call.message.edit_text(text, reply_markup=plans_menu())

    # انتخاب پلن
    if call.data.startswith("plan_"):

        size = call.data.split("_")[1]

        prices = {
            "1": 270000,
            "2": 530000,
            "3": 790000,
            "4": 1000000,
            "5": 1200000,
            "10": 2180000
        }

        price = prices[size]
        username = f"xvpn_{random.randint(1000,9999)}"

        user_orders[uid] = {
            "size": size,
            "price": price,
            "username": username
        }

        text = f"""📇 پیش فاکتور:

🔐 سرویس: {size}GB
👤 یوزرنیم: {username}

💰 مبلغ: {price:,} تومان"""

        await call.message.edit_text(text, reply_markup=pay_menu())

    # پرداخت
    if call.data == "pay":
        order = user_orders.get(uid)

        await call.message.edit_text(
            f"""💳 برای پرداخت با پشتیبانی تماس بگیرید

👤 {ADMIN_ID}
💰 مبلغ: {order['price']:,} تومان

پس از پرداخت، رسید ارسال کنید""",
            reply_markup=after_pay()
        )

    # بازگشت
    if call.data == "home":
        await call.message.edit_text("منوی اصلی", reply_markup=main_menu())

    # ارسال رسید
    if call.data == "send_receipt":
        await call.message.answer("📸 عکس رسید را ارسال کنید")

    await call.answer()

# دریافت رسید
@dp.message()
async def receipt(msg: types.Message):
    if msg.photo:
        await bot.forward_message(ADMIN_ID, msg.chat.id, msg.message_id)
        await msg.answer("✅ رسید ارسال شد")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
