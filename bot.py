import asyncio

import logging

import os
import sys
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, Request, Query, Form
from pyexpat.errors import messages

from src.cron_job.send_message_from_june import schedule_morning_task, on_message
from src.db.database import db_init, sessionmaker
from src.keys.onboard_keys import send_access_complete
from src.middlewares import db, register_check
from src.handlers import router as onnboard_router


from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from src.service.webhook_bitrix import get_data_by_webhook, get_userid_by_username

load_dotenv()
bot = Bot(os.getenv("TOKEN"))
scheduler = AsyncIOScheduler()

dp = Dispatcher()
async def on_startup():
    await db_init()

async def main():
    dp.startup.register(on_startup)
    dp.update.middleware(db.DbSessionMiddleware(session_pool=sessionmaker))
    dp.message.middleware(register_check.RegisterCheck(session_pool=sessionmaker))
    dp.include_routers(onnboard_router)

    await dp.start_polling(bot)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    schedule_morning_task(scheduler, sessionmaker, bot)
    bot_task = asyncio.create_task(main())  # main = polling
    yield
    bot_task.cancel()
    scheduler.shutdown()
    try:
        await bot_task
    except asyncio.CancelledError:
        pass
        # bot_task.cancel()
        # scheduler.shutdown()


app = FastAPI(lifespan=lifespan)


@app.post("/get_access")
async def get_access(request: Request, username=None, login=None, password=None):
    # data = await request.json()

    # print(f'data: {[username,login,password]}')

    user_id = await get_userid_by_username(sessionmaker=sessionmaker, username=username)
    # print(f'data: {[username,login,password,user_id]}')
    await bot.send_message(user_id, f"""Привет! День Х настал - добро пожаловать в команду!🎉

Вот  доступы к основным сервисам — с ними ты сможешь начать работу:

💻 Google аккаунт:
Логин: {login}
Пароль: {password}

💻 Bitrix24:
После входа в Google ты получишь уведомление на почту — там будет всё, что нужно для входа в Bitrix.

Если что-то не получается — не стесняйся, пиши Лере @to_see_sea и она поможет. Мы всегда на связи!""", reply_markup=send_access_complete())

@app.post("/bitrix25/")
async def bitrix_webhook(request: Request):
    form = await request.form()
    print("Form data:", form)
    get_data_by_webhook(dict(form))
    return {"form": dict(form)}


@app.get("/")
async def root(request: Request):
    print(f'url yandex: {request.url}')
    return {"message": "Hello World"}

@app.post("/send_second_day")
async def send_second_day_message(request: Request, username=None):
    if username is None:
        return False
    user_id = await get_userid_by_username(sessionmaker=sessionmaker, username=username)
    await on_message(user_id, bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # asyncio.run(main())

    import uvicorn

    uvicorn.run("bot:app", host="localhost", port=8000, reload=True)