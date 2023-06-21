from aiogram import types

kb = [
    [types.KeyboardButton(text='Получить данные о сотрудниках')]
]

keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True,
    input_field_placeholder='Нажмите для получения данных',
    one_time_keyboard=True
)
