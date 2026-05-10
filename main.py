import os
import logging
import asyncio

from aiogram import Bot, Dispatcher, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.state import default_state
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

API_TOKEN = "8754323678:AAH8PJBEyxkGe3K5dvJvEehp2nTnO-utxe8"
ADMIN_CHAT_ID = int(os.environ["6400775424"])
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "@idarkfail")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "@xvpnconfigs")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

main_kb = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="💰 خرید اشتراک")],
        [types.KeyboardButton(text="📦 سرویس های من"),
         types.KeyboardButton(text="🆘 پشتیبانی")]
    ],
    resize_keyboard=True
)

plans = {
    "1": 270000,
    "2": 530000,
    "3": 790000,
    "4": 1000000,
    "5": 1200000,
    "10": 2180000,
}

pending_plan = {}
user_services = {}
admin_target = {}


class AdminState(StatesGroup):
    waiting_for_config = State()


def is_admin(user_id: int):
    return user_id == ADMIN_CHAT_ID


# ─── Start ─────────────────────────────

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("👋 خوش آمدید به ربات", reply_markup=main_kb)


# ─── Buy ─────────────────────────────

@dp.message(F.text == "💰 خرید اشتراک")
async def buy(message: types.Message):
    text = (
        "📦 جزئیات محصولات:\n\n"
        "📦 حجم: 1GB - 270,000\n"
        "📦 حجم: 2GB - 530,000\n"
        "📦 حجم: 3GB - 790,000\n"
        "📦 حجم: 4GB - 1,000,000\n"
        "📦 حجم: 5GB - 1,200,000\n"
        "📦 حجم: 10GB - 2,180,000\n"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1GB", callback_data="plan_1"),
         InlineKeyboardButton(text="2GB", callback_data="plan_2")],
        [InlineKeyboardButton(text="3GB", callback_data="plan_3"),
         InlineKeyboardButton(text="4GB", callback_data="plan_4")],
        [InlineKeyboardButton(text="5GB", callback_data="plan_5"),
         InlineKeyboardButton(text="10GB", callback_data="plan_10")]
    ])

    await message.answer(text, reply_markup=kb)


# ─── Plan ─────────────────────────────

@dp.callback_query(F.data.startswith("plan_"))
async def plan(call: types.CallbackQuery):
    p = call.data.split("_")[1]
    pending_plan[call.from_user.id] = p

    await call.message.answer(
        f"📦 انتخاب شد: {p}GB\nبرای پرداخت ادامه دهید"
    )
    await call.answer()


# ─── Receipt ─────────────────────────────

@dp.message(F.photo)
async def receipt(message: types.Message):
    user_id = message.from_user.id

    await message.answer("✅ رسید دریافت شد")

    await bot.forward_message(
        ADMIN_CHAT_ID,
        message.chat.id,
        message.message_id
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📤 ارسال کانفیگ",
            callback_data=f"sendcfg_{user_id}"
        )]
    ])

    await bot.send_message(
        ADMIN_CHAT_ID,
        f"رسید جدید از {user_id}",
        reply_markup=kb
    )


# ─── Admin send config ─────────────────────────────

@dp.callback_query(F.data.startswith("sendcfg_"))
async def sendcfg(call: types.CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return

    user_id = int(call.data.split("_")[1])
    admin_target["user"] = user_id

    await state.set_state(AdminState.waiting_for_config)
    await call.message.answer("کانفیگ را ارسال کن:")
    await call.answer()


@dp.message(AdminState.waiting_for_config)
async def send_config(message: types.Message, state: FSMContext):
    user_id = admin_target.get("user")

    if not user_id:
        await message.answer("خطا")
        return

    await bot.send_message(user_id, f"🎉 کانفیگ شما:\n\n{message.text}")

    await message.answer("ارسال شد")
    await state.clear()


# ─── Run ─────────────────────────────

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
