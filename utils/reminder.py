import asyncio
import logging
from datetime import datetime, timedelta
from aiogram import Bot
from database.requests import get_reminders_with_users

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def check_reminders(bot: Bot):
    while True:
        now = datetime.now()
        current_time_str = now.strftime("%H:%M")
        logging.info("Проверка времени: %s", current_time_str)
        
        await send_notifications(bot, current_time_str)
        await asyncio.sleep(60)

async def send_notifications(bot: Bot, current_time_str: str):
    now = datetime.now().date()
    logging.info("Получение напоминаний из базы данных...")
    
    reminders = await get_reminders_with_users()
    logging.info("Найдено %d напоминаний", len(reminders))

    for reminder in reminders:
        try:
            if len(reminder) != 7:
                logging.error(f"Некорректная структура данных напоминания: {reminder}")
                continue

            reminder_id, title, text, date_str, notif_time, rule, telegram_id = reminder
            reminder_date = datetime.strptime(date_str, "%d.%m.%Y").date()

            # Отправка напоминания только если время и дата совпадают
            if notif_time == current_time_str and reminder_date == now:
                last_sent_date = reminder.sending_time if hasattr(reminder, 'sending_time') else None
                
                # Если напоминание еще не отправлялось или не было отправлено сегодня, отправляем его
                if last_sent_date is None or last_sent_date != str(now):
                    message_text = f"Напоминание: {title}\n\n{text}"

                    # Проверка по правилам
                    if rule in ["Единоразово", "Каждый день", "Через день", "Раз в неделю", "Раз в месяц"]:
                        await send_reminder(bot, reminder_id, telegram_id, message_text, now)
                
        except Exception as e:
            logging.error("Ошибка при обработке напоминания: %s", str(e))

async def send_reminder(bot: Bot, reminder_id, telegram_id, text, now):
    logging.info(f"Отправка уведомления пользователю {telegram_id}: {text}")
    await bot.send_message(chat_id=telegram_id, text=text)
    await update_reminder_send_time(reminder_id)

async def update_reminder_send_time(reminder_id: int):
    from database.requests import update_sending_time
    await update_sending_time(reminder_id)

async def start_notifier(bot: Bot):
    logging.info("Запуск системы уведомлений...")
    asyncio.create_task(check_reminders(bot))
