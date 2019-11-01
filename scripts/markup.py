from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from scripts.db_manager import UsersDbManager

change = ReplyKeyboardMarkup([['Изменить выбор']])

admin = ReplyKeyboardMarkup([['Сделать рассылку 📩'], ['Статистика 📊'], ['⬅️ Назад']])


def choose_exam():
    k = InlineKeyboardMarkup()
    k.add(InlineKeyboardButton('ОГЭ', callback_data='oge'), InlineKeyboardButton('ЕГЭ', callback_data='ege'))
    return k


async def class_choose_ege(tel_id, loop):
    user = await UsersDbManager.get_user(tel_id, loop)
    k = InlineKeyboardMarkup()
    if user.ege_math_base:
        k.add(InlineKeyboardButton('📕Математика (База) ✅', callback_data='ege_math_base_0'))
    else:
        k.add(InlineKeyboardButton('📕Математика (База)', callback_data='ege_math_base_1'))
    if user.ege_math_pro:
        k.add(InlineKeyboardButton('📗Математика (Профиль) ✅', callback_data='ege_math_pro_0'))
    else:
        k.add(InlineKeyboardButton('📗Математика (Профиль)', callback_data='ege_math_pro_1'))
    if user.ege_physics:
        k.add(InlineKeyboardButton('📘Физика ✅', callback_data='ege_physics_0'))
    else:
        k.add(InlineKeyboardButton('📘Физика', callback_data='ege_physics_1'))
    if user.ege_history:
        k.add(InlineKeyboardButton('📙История ✅', callback_data='ege_history_0'))
    else:
        k.add(InlineKeyboardButton('📙История', callback_data='ege_history_1'))
    if user.ege_social:
        k.add(InlineKeyboardButton('📓Обществознание ✅', callback_data='ege_social_0'))
    else:
        k.add(InlineKeyboardButton('📓Обществознание', callback_data='ege_social_1'))
    k.add(InlineKeyboardButton('Готово 👍🏻', callback_data='ready'))
    k.add(InlineKeyboardButton('⬅️ Назад', callback_data='back'))
    return k


async def class_choose_oge(tel_id, loop):
    user = await UsersDbManager.get_user(tel_id, loop)
    k = InlineKeyboardMarkup()
    if user.oge_math:
        k.add(InlineKeyboardButton('📕Математика ✅', callback_data='oge_math_0'))
    else:
        k.add(InlineKeyboardButton('📕Математика', callback_data='oge_math_1'))
    if user.oge_physics:
        k.add(InlineKeyboardButton('📗Физика ✅', callback_data='oge_physics_0'))
    else:
        k.add(InlineKeyboardButton('📗Физика', callback_data='oge_physics_1'))
    if user.oge_history:
        k.add(InlineKeyboardButton('📘История ✅', callback_data='oge_history_0'))
    else:
        k.add(InlineKeyboardButton('📘История', callback_data='oge_history_1'))
    if user.oge_lit:
        k.add(InlineKeyboardButton('📙Литература ✅', callback_data='oge_lit_0'))
    else:
        k.add(InlineKeyboardButton('📙Литература', callback_data='oge_lit_1'))
    if user.oge_social:
        k.add(InlineKeyboardButton('📓Обществозание ✅', callback_data='oge_social_0'))
    else:
        k.add(InlineKeyboardButton('📓Обществозание', callback_data='oge_social_1'))
    k.add(InlineKeyboardButton('Готово 👍🏻', callback_data='ready'))
    k.add(InlineKeyboardButton('⬅️ Назад', callback_data='back'))
    return k


def choose_class_for_message():
    k = InlineKeyboardMarkup()
    k.add(InlineKeyboardButton('📕Математика (База) (ЕГЭ)', callback_data='message_ege_math_base'))
    k.add(InlineKeyboardButton('📗Математика (Профиль) (ЕГЭ)', callback_data='message_ege_math_pro'))
    k.add(InlineKeyboardButton('📘Физика (ЕГЭ)', callback_data='message_ege_physics'))
    k.add(InlineKeyboardButton('📙История (ЕГЭ)', callback_data='message_ege_history'))
    k.add(InlineKeyboardButton('📓Обществознание (ЕГЭ)', callback_data='message_ege_social'))
    k.add(InlineKeyboardButton('📕Математика (ОГЭ)', callback_data='message_oge_math'))
    k.add(InlineKeyboardButton('📗Физика (ОГЭ)', callback_data='message_oge_physics'))
    k.add(InlineKeyboardButton('📘История (ОГЭ)', callback_data='message_oge_history'))
    k.add(InlineKeyboardButton('📙Литература (ОГЭ)', callback_data='message_oge_lit'))
    k.add(InlineKeyboardButton('📓Обществозание (ОГЭ)', callback_data='message_oge_social'))
    k.add(InlineKeyboardButton('Всем', callback_data='message_all'))
    return k