from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from inline import menu, bank_group_btn, bank_btn
from models.users import BankName, GroupFromBank

bank_router = Router()


class BankState(StatesGroup):
    text = State()


class GroupState(StatesGroup):
    text = State()


@bank_router.callback_query(F.data.startswith('bank_'))
async def command_start(call: CallbackQuery, state: FSMContext):
    bank_data = call.data.split("_")
    if bank_data[1] == 'text':
        await state.update_data(bank_id=bank_data[2], bank_name=bank_data[-1])
        await call.message.edit_text(f"{bank_data[-1]} Guruhlari", reply_markup=await bank_group_btn(int(bank_data[2])))
    elif bank_data[1] == 'add':
        await state.set_state(BankState.text)
        await call.message.delete()
        await call.message.answer("Bank nomini kiriting")
    elif bank_data[1] == 'delete':
        await BankName.delete(int(bank_data[2]))
        await call.message.edit_text(f"Banklar", reply_markup=await bank_btn())
    elif bank_data[1] == 'back':
        await call.message.edit_text(f"Bosh menu", reply_markup=await menu())


@bank_router.message(BankState.text)
async def command_start(message: Message, state: FSMContext):
    await BankName.create(name=message.text)
    await message.answer(f"Banklar", reply_markup=await bank_btn())
    await state.clear()


@bank_router.callback_query(F.data.startswith("group_"))
async def command_start(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_')
    res = await state.get_data()
    bank_id, bank_name = res.get('bank_id'), res.get('bank_name')
    if data[1] == 'delete':
        try:
            await GroupFromBank.delete(int(data[-1]))
            try:
                await call.message.edit_text(f"{bank_name} bank guruxlari",
                                             reply_markup=await bank_group_btn(int(bank_id)))
            except:
                await call.message.answer(f"{bank_name} bank guruxlari",
                                          reply_markup=await bank_group_btn(int(bank_id)))
        except:
            await call.message.answer("O'chirishda xatolik", reply_markup=await bank_group_btn(int(bank_id)))
    elif data[1] == 'add':
        await call.message.delete()
        await state.set_state(GroupState.text)
        await call.message.answer(f"{bank_name} bank uchun gurux id kiriting")
    elif data[1] == 'back':
        try:
            await call.message.edit_text("Banklar", reply_markup=await bank_btn())
        except:
            await call.message.answer("Banklar", reply_markup=await bank_btn())


@bank_router.message(GroupState.text)
async def command_start(message: Message, state: FSMContext):
    res = await state.get_data()
    bank_id, bank_name = res.get('bank_id'), res.get('bank_name')
    await GroupFromBank.create(bank_name=bank_name, group_id=int(message.text), bank_id=int(bank_id))
    await message.answer(f"{bank_name} bank guruxlari",
                         reply_markup=await bank_group_btn(int(bank_id)))
    await state.clear()
