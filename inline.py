from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from models import Check
from models.users import District


def menu():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[
        InlineKeyboardButton(text="Textlar", callback_data='admin_text'),
        InlineKeyboardButton(text="Check textlar", callback_data='admin_check'),
        InlineKeyboardButton(text="Tumanlar", callback_data='admin_district')
    ])
    ikb.adjust(1)
    return ikb.as_markup()


async def checks_btn():
    ikb = InlineKeyboardBuilder()
    checks = await Check.all()
    if checks:
        for i in checks:
            ikb.add(*[
                InlineKeyboardButton(text=i.text, callback_data=f'check_text_{i.id}'),
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
