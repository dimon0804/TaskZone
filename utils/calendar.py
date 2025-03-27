from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
import calendar


class CalendarKeyboard:
    def __init__(self, month=None, year=None):
        self.current_month = month or datetime.now().month
        self.current_year = year or datetime.now().year
        self.month_name = calendar.month_name[self.current_month]
        self.days_in_month = calendar.monthrange(self.current_year, self.current_month)[1]
        self.keyboard = self.create_calendar_keyboard()

    def create_calendar_keyboard(self):
        keyboard = []
        keyboard.append(
            [InlineKeyboardButton(text=f"{self.month_name} {self.current_year}", callback_data="month_info")]
        )
        navigation_row = [
            InlineKeyboardButton(text="<< Предыдущий месяц", callback_data="prev_month"),
            InlineKeyboardButton(text="Следующий месяц >>", callback_data="next_month"),
        ]
        keyboard.append(navigation_row)
        week = []
        for day in range(1, self.days_in_month + 1):
            week.append(InlineKeyboardButton(text=str(day), callback_data=f"day_{day}"))
            if len(week) == 7:
                keyboard.append(week)
                week = []
        if week:
            while len(week) < 7:
                week.append(InlineKeyboardButton(text=" ", callback_data="empty"))
            keyboard.append(week)
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    def get_keyboard(self):
        return self.keyboard

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        return CalendarKeyboard(self.current_month, self.current_year)

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        return CalendarKeyboard(self.current_month, self.current_year)

    def get_date(self, day):
        return f"{day:02d}.{self.current_month:02d}.{self.current_year}"
