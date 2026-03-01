from sys import prefix

from aiogram.filters.callback_data import CallbackData


# определяет, что именно эта кнопка была нажата для этого класса. префикс должен быть уникальным
class RoleSelect(CallbackData, prefix="role_select"):
    role: str