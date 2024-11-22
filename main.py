import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from cfg import TOKEN

bot = Bot(token=TOKEN)

dp = Dispatcher()


users_tasks = {}


@dp.message(Command('start'))
async def start_handler(message: types.Message):
    await message.answer(
        f'Привет!\n' +
        'Данный бот помогает пользователю составить план дня, ' +
        'добавляя задачи с указанием времени и пометками о приоритете'
    )



@dp.message(Command('add_task'))
async def add_task_handler(message: types.Message,command):
    if command.args is None or len(command.args.split()) < 2:
        await message.answer(
            f'Для использования данной функции нужно передать 2 аргумента <Время>(Часы:Минуты) <Описание>' +
            f' \nПример: /add_task 14:00 Купить продукты'
        )
        return

    chat_id = message.chat.id

    users_tasks[chat_id] = users_tasks.get(chat_id,[])
    if chat_id not in users_tasks:
        users_tasks[chat_id] = command.args

    else:
        users_tasks[chat_id].append(command.args)

    await message.answer(
        f'Я добавил задачу "{command.args}"'
    )

@dp.message(Command('show_task'))
async def show_task_handler(message: types.Message):
    chat_id = message.chat.id
    if chat_id not in users_tasks.keys():
        await message.answer(
            f'Нет задач!' +
            f'\nДля их создания используйте /add_task'
        )

        return

    result = users_tasks[chat_id]
    await message.answer ('\n'.join(result))


@dp.message(Command('remove_task'))
async def remove_task_handler(message: types.Message,command):
    if command.args is None or len(command.args.split()) != 1:
        await message.answer(
            f'Для вызова данной функции необходимо передать аргумент <Время> ' +
            f'Пример: /remove_task 14:00'
        )

        return

    chat_id = message.chat.id

    if chat_id not in users_tasks:
        await message.answer(
            f'Вы не можете удалить задачи, так как их нет!'
        )
        return

    # args = command.args
    # del_values = []
    # for key,value in users_tasks.items():
    #     if args in str(value):
    #         del_values.append(users_tasks[key])
    #         await message.answer(
    #             f'Задача(и) на {args} была удалена!'
    #         )


@dp.message(Command('clear_tasks'))
async def clear_tasks_handler(message: types.Message):
    for key,value in dict(users_tasks).items():
        del users_tasks[key]
    await message.answer(
        f'Все задачи были удалены!'
    )



@dp.message(F.text)
async def process_input_handler(message: types.Message):
    await message.answer('Используй команды!!!')





async def main():
    await dp.start_polling(bot)

asyncio.run(main())
