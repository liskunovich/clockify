import asyncio

from aiogram.filters.command import Command
from aiogram.filters import Text
from aiogram import types, Router, html
from keyboard import keyboard
from usecases.workspace import get_workspace, get_details_about_workspace

router = Router()


@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(f"Привет, {message.chat.username}!", reply_markup=keyboard)


@router.message(Text('Получить данные о сотрудниках'))
async def get_memberships_data(message: types.Message):
    upload_message = await message.answer("Обработка данных началась, ожидайте")

    workspace = await get_workspace()
    data = await get_details_about_workspace(workspace)

    for d in data:
        await message.answer(f'👤 {html.bold("Employee: ")}{d.employee.name}\n'
                             f'⌛️ {html.bold("Worktime (2 weeks)")}: {d.worktime} hours \n'
                             f'🧠 {html.bold("Longest Task:")} {d.longest_task.description} - {round(d.longest_task.get_worktime() / 3600, 2)} hours \n'
                             f'💵 {html.bold("Total cash")}: {d.salary}$', parse_mode='HTML')


@router.message()
async def echo(message: types.Message):
    await message.answer(message.text, reply_markup=keyboard)
