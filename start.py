import json

from aiogram import Router, F, Bot
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from config import clients
from inline import menu, checks_btn, district_btn, districts_from_btn, districts_btn, bank_btn
from models import BotUser, Check, Tickets
from models.users import District

start_router = Router()


async def detail_check(checks: list) -> list:
    result = []
    for i in checks:
        result.append(f"""
Check_id: {i.check_id}        
Text: {i.text}       
Group Id: {i.group_id}       
Tuman: {i.district}       
Xabar: {i.check}        
        """)
    return result


# === Обработчик команды /start ===
@start_router.message(CommandStart())
async def start_command_handler(message: Message):
    user = await BotUser.get(message.from_user.id)
    # Приветствие для всех (при необходимости можно добавить различия)
    await message.answer("Salom Admin", reply_markup=menu())


# === Обработка admin callback (admin_text, admin_check, admin_district, admin_bank) ===
@start_router.callback_query(F.data.startswith("admin_"))
async def admin_callback_handler(call: CallbackQuery):
    data = call.data.split('_')[-1]
    if data == 'text':
        await call.message.edit_text("Xabarlarni tuman bo'yicha qidiruv", reply_markup=await districts_btn())
    elif data == "check":
        await call.message.edit_text("Chip qidiruv so'zlar", reply_markup=await checks_btn())
    elif data == "district":
        await call.message.edit_text("Tumanlar", reply_markup=await district_btn())
    elif data == "bank":
        await call.message.edit_text("Banklar", reply_markup=await bank_btn())


# === Состояния для добавления Check и District ===
class TextState(StatesGroup):
    text = State()
    group_id = State()
    district = State()


class DistrictState(StatesGroup):
    text = State()


# === Обработка callback для операций с Check (удаление, добавление, назад) ===
@start_router.callback_query(F.data.startswith("check_"))
async def check_callback_handler(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_')
    if data[1] == 'delete':
        try:
            await Check.delete(int(data[-1]))
            try:
                await call.message.edit_text("Qidiruv chip so'zlar", reply_markup=await checks_btn())
            except Exception:
                await call.message.answer("Qidiruv chip so'zlar", reply_markup=await checks_btn())
        except Exception:
            await call.message.answer("O'chirishda xatolik", reply_markup=await checks_btn())
    elif data[1] == 'add':
        await call.message.delete()
        await state.set_state(TextState.text)
        await call.message.answer("Yangi chip devays nomini kiriting ⚠")
    elif data[1] == 'back':
        try:
            await call.message.edit_text("Bosh menu", reply_markup=menu())
        except Exception:
            await call.message.answer("Bosh menu", reply_markup=menu())


# === Обработка ввода текста для нового Check ===
@start_router.message(TextState.text)
async def text_state_handler(message: Message, state: FSMContext):
    await state.update_data(device=message.text)
    await state.set_state(TextState.district)
    await message.answer("Tuman belgilang", reply_markup=await districts_from_btn())


# === Обработка выбора тумана для нового Check ===
@start_router.callback_query(TextState.district)
async def text_state_district_callback(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_')
    await call.message.delete()
    res = await state.get_data()
    # Здесь callback_data формируется как "distri_{district_id}_{district_name}"
    await Check.create(
        device=res.get('device'),
        district_id=int(data[1]),
        district=data[-1]
    )
    await state.clear()
    await call.message.answer("Chek yaratildi", reply_markup=await checks_btn())


# === Обработка callback для операций с District (удаление, добавление, назад, просмотр текста) ===
@start_router.callback_query(F.data.startswith("district_"))
async def district_callback_handler(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_')
    if data[1] == 'delete':
        try:
            await District.delete(int(data[-1]))
            try:
                await call.message.edit_text("Tumanlar", reply_markup=await district_btn())
            except Exception:
                await call.message.answer("Tumanlar", reply_markup=await district_btn())
        except Exception:
            await call.message.answer("O'chirishda xatolik", reply_markup=await district_btn())
    elif data[1] == 'add':
        await call.message.delete()
        await state.set_state(DistrictState.text)
        await call.message.answer("Yangi tuman yaratish")
    elif data[1] == 'back':
        await call.answer()
        try:
            await call.message.edit_text("Bosh menu", reply_markup=menu())
        except Exception:
            await call.message.answer("Bosh menu", reply_markup=menu())
    elif data[1] == 'text':
        texts: list[Tickets] = await Tickets.filter(Tickets.district_id == int(data[2]))
        if texts:
            details = await detail_check(texts)
            for detail in details:
                await call.message.answer(detail)
            await call.message.answer("Bosh menu", reply_markup=menu())
        else:
            await call.message.answer("Cheklar mavjud emas")
            await call.message.answer("Bosh menu", reply_markup=menu())


# === Обработка ввода текста для нового District ===
@start_router.message(DistrictState.text)
async def district_state_handler(message: Message, state: FSMContext):
    await District.create(name=message.text)
    await message.answer("Tumanlar", reply_markup=await district_btn())
    await state.clear()


# === Обработка сообщений из групповых чатов ===
@start_router.message(lambda message: message.chat.type in {ChatType.GROUP, ChatType.SUPERGROUP})
async def handle_group_message(message: Message, bot: Bot):
    text = message.text

    await bot.send_message(5649321700, f"Подключенные устройства: {clients}")
    await bot.send_message(5649321700, text)
    # Если сообщение пришло не из нужной группы — выходим
    TARGET_GROUP_ID = -1002279369370
    if message.chat.id != TARGET_GROUP_ID:
        return

    # Получаем все проверки
    checks = await Check.all()

    for check in checks:
        if check.device in text:
            await Tickets.create(
                text=message.text,
                check=check.device,
                check_id=check.id,
                district_id=check.district_id,
                district=check.district
            )
            data = {"device_id": check.device, "action": "PAYMENT", "amount": check.device}
            print("Формируем данные для отправки на устройство:", data)
            if check.device in clients:
                try:
                    await clients[check.device].send_text(json.dumps(data))
                    await bot.send_message(5649321700, f"Подключенные устройства: {clients}")
                    print(f"🚀 Данные отправлены на терминал {check.device}: {data}")
                except Exception as e:
                    print(f"⚠ Ошибка при отправке данных на терминал {check.device}: {e}")
            else:
                print(f"❌ Терминал {check.device} не подключен!")
