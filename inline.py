from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from models import Check
from models.users import District, BankName, GroupFromBank


def menu():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Textlar", callback_data="admin_text"),
        InlineKeyboardButton(text="Check Chip textlar", callback_data="admin_check"),
        InlineKeyboardButton(text="Tumanlar", callback_data="admin_district"),
        InlineKeyboardButton(text="Banklar", callback_data="admin_bank")
    )
    # Упорядочиваем кнопки по одной в ряду
    builder.adjust(1)
    return builder.as_markup()


async def checks_btn():
    builder = InlineKeyboardBuilder()
    checks = await Check.all()
    if checks:
        for check in checks:
            builder.add(
                InlineKeyboardButton(text=check.device, callback_data=f"check_text_{check.id}"),
                InlineKeyboardButton(text="❌", callback_data=f"check_delete_{check.id}")
            )
    # Добавляем кнопки управления
    builder.row(InlineKeyboardButton(text="Check qo'shish", callback_data="check_add"))
    builder.row(InlineKeyboardButton(text="Ortga", callback_data="check_back"))
    builder.adjust(2)
    return builder.as_markup()


async def district_btn():
    builder = InlineKeyboardBuilder()
    districts = await District.all()
    if districts:
        for district in districts:
            builder.add(
                InlineKeyboardButton(text=district.name, callback_data=f"district_text_{district.id}"),
                InlineKeyboardButton(text="❌", callback_data=f"district_delete_{district.id}")
            )
    builder.row(InlineKeyboardButton(text="Tuman qo'shish", callback_data="district_add"))
    builder.row(InlineKeyboardButton(text="Ortga", callback_data="district_back"))
    builder.adjust(2)
    return builder.as_markup()


async def bank_btn():
    builder = InlineKeyboardBuilder()
    banks = await BankName.all()
    if banks:
        for bank in banks:
            builder.add(
                InlineKeyboardButton(text=bank.name, callback_data=f"bank_text_{bank.id}_{bank.name}"),
                InlineKeyboardButton(text="❌", callback_data=f"bank_delete_{bank.id}")
            )
    builder.row(InlineKeyboardButton(text="Bank qo'shish", callback_data="bank_add"))
    builder.row(InlineKeyboardButton(text="Ortga", callback_data="bank_back"))
    builder.adjust(2)
    return builder.as_markup()


async def bank_group_btn(bank_id: int):
    builder = InlineKeyboardBuilder()
    groups = await GroupFromBank.filter(GroupFromBank.bank_id == bank_id)
    if groups:
        for group in groups:
            builder.add(
                InlineKeyboardButton(text=group.bank_name, callback_data=f"group_text_{group.id}"),
                InlineKeyboardButton(text=str(group.group_id), callback_data=f"group_text_{group.id}"),
                InlineKeyboardButton(text="❌", callback_data=f"group_delete_{group.id}")
            )
    builder.row(InlineKeyboardButton(text="Gurux qo'shish", callback_data="group_add"))
    builder.row(InlineKeyboardButton(text="Ortga", callback_data="group_back"))
    builder.adjust(3)
    return builder.as_markup()


async def districts_btn():
    builder = InlineKeyboardBuilder()
    districts = await District.all()
    for district in districts:
        builder.add(
            InlineKeyboardButton(text=district.name, callback_data=f"district_text_{district.id}_{district.name}")
        )
    builder.adjust(1)
    return builder.as_markup()


async def districts_from_btn():
    builder = InlineKeyboardBuilder()
    districts = await District.all()
    for district in districts:
        builder.add(
            InlineKeyboardButton(text=district.name, callback_data=f"distri_{district.id}_{district.name}")
        )
    builder.adjust(1)
    return builder.as_markup()
