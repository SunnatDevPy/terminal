from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from models import Check
from models.users import District, BankName, GroupFromBank


def menu():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[
        InlineKeyboardButton(text="Textlar", callback_data='admin_text'),
        InlineKeyboardButton(text="Check Chip textlar", callback_data='admin_check'),
        InlineKeyboardButton(text="Tumanlar", callback_data='admin_district'),
        InlineKeyboardButton(text="Banklar", callback_data='admin_bank')
    ])
    ikb.adjust(1)
    return ikb.as_markup()


async def checks_btn():
    ikb = InlineKeyboardBuilder()
    checks = await Check.all()
    if checks:
        for i in checks:
            ikb.add(*[
                InlineKeyboardButton(text=i.device, callback_data=f'check_text_{i.id}'),
                InlineKeyboardButton(text="❌", callback_data=f'check_delete_{i.id}'),
            ])
    ikb.row(InlineKeyboardButton(text="Check qo'shish", callback_data=f'check_add'))
    ikb.row(InlineKeyboardButton(text="Ortga", callback_data=f'check_back'))
    ikb.adjust(2)
    return ikb.as_markup()


async def district_btn():
    ikb = InlineKeyboardBuilder()
    checks = await District.all()
    if checks:
        for i in checks:
            ikb.add(*[
                InlineKeyboardButton(text=i.name, callback_data=f'district_text_{i.id}'),
                InlineKeyboardButton(text="❌", callback_data=f'district_delete_{i.id}'),
            ])
    ikb.row(InlineKeyboardButton(text="Tuman qo'shish", callback_data=f'district_add'))
    ikb.row(InlineKeyboardButton(text="Ortga", callback_data=f'district_back'))
    ikb.adjust(2)
    return ikb.as_markup()


async def bank_btn():
    ikb = InlineKeyboardBuilder()
    checks = await BankName.all()
    if checks:
        for i in checks:
            ikb.add(*[
                InlineKeyboardButton(text=i.name, callback_data=f'bank_text_{i.id}_{i.name}'),
                InlineKeyboardButton(text="❌", callback_data=f'bank_delete_{i.id}'),
            ])
    ikb.row(InlineKeyboardButton(text="Bank qo'shish", callback_data=f'bank_add'))
    ikb.row(InlineKeyboardButton(text="Ortga", callback_data=f'bank_back'))
    ikb.adjust(2)
    return ikb.as_markup()


async def bank_group_btn(bank_id):
    ikb = InlineKeyboardBuilder()
    checks = await GroupFromBank.filter(GroupFromBank.bank_id == bank_id)
    if checks:
        for i in checks:
            ikb.add(*[
                InlineKeyboardButton(text=i.bank_name, callback_data=f'group_text_{i.id}'),
                InlineKeyboardButton(text=str(i.group_id), callback_data=f'group_text_{i.id}'),
                InlineKeyboardButton(text="❌", callback_data=f'group_delete_{i.id}'),
            ])
    ikb.row(InlineKeyboardButton(text=f"Gurux qo'shish", callback_data=f'group_add'))
    ikb.row(InlineKeyboardButton(text="Ortga", callback_data=f'group_back'))
    ikb.adjust(3)
    return ikb.as_markup()


async def districts_btn():
    ikb = InlineKeyboardBuilder()
    checks = await District.all()
    for i in checks:
        ikb.add(*[
            InlineKeyboardButton(text=i.name, callback_data=f'district_text_{i.id}_{i.name}'),
        ])
    ikb.adjust(1)
    return ikb.as_markup()


async def districts_from_btn():
    ikb = InlineKeyboardBuilder()
    checks = await District.all()
    for i in checks:
        ikb.add(*[
            InlineKeyboardButton(text=i.name, callback_data=f'distri_{i.id}_{i.name}'),
        ])
    ikb.adjust(1)
    return ikb.as_markup()
