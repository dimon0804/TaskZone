import asyncio
import logging
from datetime import datetime, timedelta
from aiogram import Bot
from database.requests import get_tasks_with_users
import keyboards.user as kb

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def check_deadlines(bot: Bot):
    while True:
        now = datetime.now()
        current_time_str = now.strftime("%H:%M")  # Текущее время в формате "HH:MM"
        logging.info("Проверка времени: %s", current_time_str)
        
        await send_notifications(bot, current_time_str)
        await asyncio.sleep(60)  # Проверяем каждую минуту

async def send_notifications(bot: Bot, current_time_str: str):
    now = datetime.now().date()
    logging.info("Получение задач из базы данных...")
    
    task_list = await get_tasks_with_users()

    logging.info("Найдено %d задач", len(task_list))

    for task, telegram_id, notif_time in task_list:
        try:
            if notif_time == current_time_str:  # Проверка времени для каждого пользователя
                deadline = datetime.strptime(task.due_date, "%d.%m.%Y").date()
                text = get_notification_text(task.title, deadline, now)
                if text:
                    logging.info("Отправка уведомления пользователю %d: %s", telegram_id, text)
                    await bot.send_message(chat_id=telegram_id, text=text, reply_markup=await kb.task_notif(task.id))
        except Exception as e:
            logging.error("Ошибка при обработке задачи ID %d: %s", task.id, str(e))

def get_notification_text(title, deadline, now):
    if deadline == now + timedelta(days=3):
        return f"⚠️ Напоминание! До дедлайна задачи '{title}' осталось 3 дня."
    elif deadline == now + timedelta(days=1):
        return f"⏳ Завтра дедлайн задачи '{title}'!"
    elif deadline == now:
        return f"🚨 Сегодня дедлайн задачи '{title}'! Пора сдавать!"
    return None

async def start_notifier(bot: Bot):
    logging.info("Запуск системы уведомлений...")
    asyncio.create_task(check_deadlines(bot))
