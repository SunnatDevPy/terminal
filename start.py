import json

from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from config import clients
from inline import menu, checks_btn, district_btn, districts_from_btn, districts_btn
from models import BotUser, Check
from models import Tickets
from models.users import District, GroupFromBank

start_router = Router()


async def detail_check(checks):
    list_ = []
    for i in checks:
        list_.append(f"""
Check_id: {i.check_id}        
Text: {i.text}       
Group Id: {i.group_id}       
Tuman: {i.district}       
Xabar: {i.check}        
        """)
    return list_


@start_router.message(CommandStart())
async def command_start(message: Message):
    user = await BotUser.get(message.from_user.id)
    from_user = message.from_user
    if not user:
        await message.answer(f'Salom Admin', reply_markup=menu())
    else:
        if from_user.id in [5649321700, 885440903]:
            await message.answer(f'Salom Admin', reply_markup=menu())
        else:
            await message.answer(f'Salom Admin', reply_markup=menu())


@start_router.callback_query(F.data.startswith("admin_"))
async def command_start(call: CallbackQuery):
    data = call.data.split('_')[-1]
    if data == 'text':
        await call.message.edit_text("Xabarlarni tuman bo'yicha qidiruv", reply_markup=await districts_btn())
    elif data == "check":
        await call.message.edit_text("Chip qidiruv so'zlar", reply_markup=await checks_btn())
    elif data == "district":
        await call.message.edit_text("Tumanlar", reply_markup=await district_btn())
    elif data == "bank":
        await call.message.edit_text("Banklar", reply_markup=await district_btn())


class TextState(StatesGroup):
    text = State()
    group_id = State()
    district = State()


class DistrictState(StatesGroup):
    text = State()


@start_router.callback_query(F.data.startswith("check_"))
async def command_start(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_')
    if data[1] == 'delete':
        try:
            await Check.delete(int(data[-1]))
            try:
                await call.message.edit_text("Qidiruv chip so'zlar", reply_markup=await checks_btn())
            except:
                await call.message.answer("Qidiruv chip so'zlar", reply_markup=await checks_btn())
        except:
            await call.message.answer("O'chirishda xatolik", reply_markup=await checks_btn())
    elif data[1] == 'add':
        await call.message.delete()
        await state.set_state(TextState.text)
        await call.message.answer("Yangi chip devays nomini kiriting ⚠")
    elif data[1] == 'back':
        try:
            await call.message.edit_text("Bosh menu", reply_markup=menu())
        except:
            await call.message.answer("Bosh menu", reply_markup=menu())


@start_router.message(TextState.text)
async def command_start(message: Message, state: FSMContext):
    await state.update_data(device=message.text)
    await state.set_state(TextState.district)
    await message.answer("Tuman belgilang", reply_markup=await districts_from_btn())


@start_router.callback_query(TextState.district)
async def command_start(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_')
    await call.message.delete()
    res = await state.get_data()
    print(res)
    await Check.create(device=res.get('device'), district_id=int(data[1]), district=data[-1])
    await state.clear()
    await call.message.answer("Chek yaratildi", reply_markup=await checks_btn())


@start_router.callback_query(F.data.startswith("district_"))
async def command_start(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_')
    if data[1] == 'delete':
        try:
            await District.delete(int(data[-1]))
            try:
                await call.message.edit_text("Tumanlar", reply_markup=await district_btn())
            except:
                await call.message.answer("Tumanlar", reply_markup=await district_btn())
        except:
            await call.message.answer("O'chirishda xatolik", reply_markup=await district_btn())
    elif data[1] == 'add':
        await call.message.delete()
        await state.set_state(DistrictState.text)
        await call.message.answer("Yangi tuman  yaratish")
    elif data[1] == 'back':
        await call.answer()
        try:
            await call.message.edit_text("Bosh menu", reply_markup=menu())
        except:
            await call.message.answer("Bosh menu", reply_markup=menu())
    elif data[1] == 'text':
        texts: list[Tickets] = await Tickets.filter(Tickets.district_id == int(data[2]))
        if texts:
            for i in await detail_check(texts):
                await call.message.answer(i)
            else:
                await call.message.answer("Bosh menu", reply_markup=menu())
        else:
            await call.message.answer("Cheklar mavjud emas")
            await call.message.answer("Bosh menu", reply_markup=menu())


@start_router.message(DistrictState.text)
async def command_start(message: Message, state: FSMContext):
    await District.create(name=message.text)
    await message.answer("Tumanlar", reply_markup=await district_btn())
    await state.clear()


@start_router.message(lambda message: message.chat.type in {ChatType.GROUP, ChatType.SUPERGROUP})
async def handle_message(message: Message):
    text = message.text
    print(text)
    print(clients)
    bank_groups = await GroupFromBank.all()
    for i in bank_groups:
        if -1002279369370 == message.chat.id:
            for j in await Check.all():
                if j.device in text:
                    await Tickets.create(text=message.text, check=j.device, check_id=i.id, district_id=i.district_id,
                                         district=i.district)
                    data = {"device_id": j.device, "action": "PAYMENT", "amount": i.device}
                    print(data)
                    if j.device in clients:
                        try:
                            await clients[j.device].send_text(json.dumps(data))
                            print(f"🚀 Данные text на терминал {i.device}: {data}")
                        except Exception as e:
                            print(f"⚠ Ошибка device_id при отправке данных на терминал {i.device}: {e}")
                    else:
                        print(f"❌ Терминал {i.device} не подключен!")
