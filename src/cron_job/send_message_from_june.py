import pytz
from aiogram import Dispatcher
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.keys.onboard_keys import send_check_list
from src.service.webhook_bitrix import get_smart_proccess_by_date, get_userid_by_username


async def on_message(item, bot):


    await bot.send_message(item, """ 
 	Привет!

📆 Уже завтра тот самый день, когда мы начнём сотрудничество.

☑️ Утром я пришлю тебе доступы в почту и корпоративный портал Битрикс.

☑️ Также пришлю информацию по вводной встрече с руководителем, на которой вы сможете подробнее обсудить проект и задачи на ближайшее время.

Если на этом этапе всё понятно, поехали дальше, нажимай кнопку «Что дальше?».

❔Если остались вопросы – напиши Лере @to_see_sea""", reply_markup=send_check_list())




async def get_junes(sessionmaker, bot):
        junes = get_smart_proccess_by_date()

        if len(junes) > 0:
            # print(junes)
            for item in junes['result']['items']:
                print(item)
                print("отправка...")
                if item['ufCrm31_1758624931'] is None:
                    continue
                user_id = await get_userid_by_username(username=item['ufCrm31_1758624931'], sessionmaker=sessionmaker)
                print(user_id)
                await on_message(user_id, bot)


def schedule_morning_task(scheduler, sessionmaker, bot):
    """Настройка планировщика для задачи в 10:00 по МСК"""
    # Устанавливаем московский часовой пояс
    msk_timezone = pytz.timezone('Europe/Moscow')

    # Создаем триггер на 10:00 каждый день
    trigger = CronTrigger(
        hour=10,
        minute= 0,
        timezone=msk_timezone
    )

    # Добавляем задачу в планировщик
    scheduler.add_job(
        get_junes,
        trigger=trigger,
        id='morning_messages',
        args=[sessionmaker, bot],
        name='Ежедневная утренняя рассылка в 10:00 МСК',
        replace_existing=True
    )

    # logging.info("📅 Планировщик настроен на запуск в 10:00 по МСК")