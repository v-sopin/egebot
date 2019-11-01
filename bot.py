import asyncio
from aiogram import Bot, Dispatcher, executor, exceptions
from scripts.db_manager import UsersDbManager
from scripts.config import TOKEN, DEVELOPER_ID, ADMINS
import scripts.markup as mk

bot = Bot(TOKEN)
dp = Dispatcher(bot)
loop = asyncio.get_event_loop()


@dp.message_handler(commands=['start'])
async def start(message):
    tel_id = message.chat.id
    if not await UsersDbManager.user_exist(tel_id, loop):
        await UsersDbManager.add_user(tel_id, loop)

    await bot.send_message(tel_id, 'Выбери экзамен', disable_notification=True, reply_markup=mk.choose_exam())


@dp.message_handler(commands=['cancle'])
async def cancel(message):
    tel_id = message.chat.id
    await UsersDbManager.update_context(tel_id, '0', loop)
    await bot.send_message(tel_id, 'Операция отменена')

'''
    
    Админка
    
'''


@dp.message_handler(commands=['admin'])
async def admin(message):
    tel_id = message.chat.id
    if tel_id != DEVELOPER_ID and tel_id not in ADMINS:
        await bot.send_message(tel_id, '❌ У вас нет прав администратора')
        return

    await bot.send_message(tel_id, 'Панель администратора', reply_markup=mk.admin, disable_notification=True)


@dp.message_handler(lambda message: message.text == '⬅️ Назад')
async def back(message):
    tel_id = message.chat.id
    await UsersDbManager.update_context(tel_id, '0', loop)
    await bot.send_message(tel_id, 'Главное меню', disable_notification=True, reply_markup=mk.change)
    await bot.send_message(tel_id, 'Выбери экзамен', disable_notification=True, reply_markup=mk.choose_exam())


@dp.message_handler(lambda message: message.text == 'Статистика 📊')
async def stats(message):
    tel_id = message.chat.id
    if tel_id != DEVELOPER_ID and tel_id not in ADMINS:
        await bot.send_message(tel_id, '❌ У вас нет прав администратора')
        return

    users = await UsersDbManager.get_all_users(loop)
    subscribed = 0
    unsubscribed = 0
    choosed_oge = 0
    choosed_ege = 0
    for u in users:
        if u.is_using:
            subscribed += 1
        else:
            unsubscribed += 1

        if u.oge_social or u.oge_math or u.oge_history or u.oge_lit or u.oge_physics:
            choosed_oge += 1

        if u.ege_social or u.ege_history or u.ege_physics or u.ege_math_pro or u.ege_math_base:
            choosed_ege += 1

    text = f'''
<b>Всего людей в базе:</b> {len(users)}

<b>Подписаны на бота:</b> {subscribed}

<b>Отписались:</b> {unsubscribed}

<b>Выбрали предметы для ЕГЭ:</b> {choosed_ege}

<b>Выбрали предметы для ОГЭ:</b> {choosed_oge}'''

    await bot.send_message(tel_id, text, parse_mode='HTML', disable_notification=True)


@dp.message_handler(lambda message: message.text == 'Сделать рассылку 📩')
async def message_(message):
    tel_id = message.chat.id
    if tel_id != DEVELOPER_ID and tel_id not in ADMINS:
        await bot.send_message(tel_id, '❌ У вас нет прав администратора')
        return

    await bot.send_message(tel_id, 'По какой категории сделать рассылку?', reply_markup=mk.choose_class_for_message(), disable_notification=True)


@dp.callback_query_handler(lambda call: call.data.startswith('message_'))
async def clas_choosed(call):
    tel_id = call.message.chat.id
    if tel_id != DEVELOPER_ID and tel_id not in ADMINS:
        await bot.send_message(tel_id, '❌ У вас нет прав администратора')
        return

    clas = call.data[8:]

    await bot.send_message(tel_id, ('Отправьте мне сообщение, которое нужно разослать. Это может быть текст, картинка,'
                                    ' видео, стикер или файл. Если хотите отменить операцию, используйте /cancel'),
                           disable_notification=True)
    await UsersDbManager.update_context(tel_id, f'wait_message_{clas}', loop)


@dp.message_handler(lambda message: UsersDbManager.sync_get_context(message.chat.id).startswith('wait_message_'),
                    content_types=['text', 'photo', 'video', 'sticker', 'document'])
async def wait_for_message(message):
    tel_id = message.chat.id
    if tel_id != DEVELOPER_ID and tel_id not in ADMINS:
        await bot.send_message(tel_id, '❌ У вас нет прав администратора')
        return

    message_counter = 0

    context = await UsersDbManager.get_context(tel_id, loop)
    class_name = context[13:]
    print('Test', class_name)
    all_users = await UsersDbManager.get_all_users(loop)
    filtered_users = []

    await UsersDbManager.update_context(tel_id, '0', loop)

    for u in all_users:
        if u.ege_math_base and class_name == 'ege_math_base':
            filtered_users.append(u)
        elif u.ege_math_pro and class_name == 'ege_math_pro':
            filtered_users.append(u)
        elif u.ege_physics and class_name == 'ege_physics':
            filtered_users.append(u)
        elif u.ege_history and class_name == 'ege_history':
            filtered_users.append(u)
        elif u.ege_social and class_name == 'ege_social':
            filtered_users.append(u)
        elif u.oge_physics and class_name == 'oge_physics':
            filtered_users.append(u)
        elif u.oge_lit and class_name == 'oge_lit':
            filtered_users.append(u)
        elif u.oge_history and class_name == 'oge_history':
            filtered_users.append(u)
        elif u.oge_math and class_name == 'oge_math':
            filtered_users.append(u)
        elif u.oge_social and class_name == 'oge_social':
            filtered_users.append(u)
        elif class_name == 'all':
            filtered_users.append(u)

    if message.text is not None:
        content = message.text
        for user in filtered_users:
            try:
                await bot.send_message(user.tel_id, content, parse_mode='HTML')
                if not user.is_using:
                    await UsersDbManager.update_is_using(user.tel_id, True, loop)
                message_counter += 1
            except Exception:
                print('User not found')
                await UsersDbManager.update_is_using(user.tel_id, False, loop)

    elif message.sticker is not None:
        sticker_file_id = message.sticker.file_id
        for user in filtered_users:
            try:
                await bot.send_sticker(user.tel_id, sticker_file_id)
                if not user.is_using and tel_id not in ADMINS and tel_id != DEVELOPER_ID:
                    await UsersDbManager.update_is_using(user.tel_id, True, loop)
                message_counter += 1
            except Exception:
                print('User not found')
                await UsersDbManager.update_is_using(user.tel_id, False, loop)

    elif message.photo is []:
        photo_file_id = message.photo[0].file_id
        for user in filtered_users:
            try:
                await bot.send_photo(user.tel_id, photo_file_id)
                if not user.is_using:
                    await UsersDbManager.update_is_using(user.tel_id, True, loop)
                message_counter += 1
            except Exception:
                print('User not found')
                await UsersDbManager.update_is_using(user.tel_id, False, loop)

    elif message.video is not None:
        video_file_id = message.video.file_id
        for user in filtered_users:
            try:
                await bot.send_video(user.tel_id, video_file_id)
                if not user.is_using:
                    await UsersDbManager.update_is_using(user.tel_id, True, loop)
                message_counter += 1
            except Exception:
                print('User not found')
                await UsersDbManager.update_is_using(user.tel_id, False, loop)

    elif message.document is not None:
        file_id = message.document.file_id
        for user in filtered_users:
            try:
                await bot.send_document(user.tel_id, file_id)
                if not user.is_using:
                    await UsersDbManager.update_is_using(user.tel_id, True, loop)
                message_counter += 1
            except Exception:
                int('User not found')
                await UsersDbManager.update_is_using(user.tel_id, False, loop)

    text = '''✅ Рассылка закончена
📩 {0} сообщений успешно доставлено
    '''.format(message_counter)

    await bot.send_message(tel_id, text, disable_notification=True)



'''

    Для пользователей

'''


@dp.callback_query_handler(lambda call: call.data == 'oge')
async def oge(call):
    tel_id = call.message.chat.id
    message_id = call.message.message_id

    kb = await mk.class_choose_oge(tel_id, loop)

    try:
        await bot.edit_message_text('Выбери предметы, которые ты будешь сдавать на ОГЭ', tel_id, message_id, reply_markup=kb)
    except exceptions.MessageNotModified:
        print('Message is not modified')


@dp.callback_query_handler(lambda call: call.data == 'ege')
async def ege(call):
    tel_id = call.message.chat.id
    message_id = call.message.message_id

    kb = await mk.class_choose_ege(tel_id, loop)

    try:
        await bot.edit_message_text('Выбери предметы, которые ты будешь сдавать на ЕГЭ', tel_id, message_id, reply_markup=kb)
    except exceptions.MessageNotModified:
        print('Message is not modified')


@dp.callback_query_handler(lambda call: call.data == 'back')
async def back(call):
    tel_id = call.message.chat.id
    message_id = call.message.message_id

    try:
        await bot.edit_message_text('Выбери экзамен', tel_id, message_id, reply_markup=mk.choose_exam())
    except exceptions.MessageNotModified:
        print('Message is not modified')


@dp.callback_query_handler(lambda call: call.data == 'ready')
async def ready(call):
    tel_id = call.message.chat.id
    message_id = call.message.message_id

    await bot.send_message(tel_id, '📝Хорошо, по этим предметам и буду присылать тебе полезную инфу. Если захочешь изменить выбор то нажми кнопку Изменить выбор👇', reply_markup=mk.change, disable_notification=True)
    await bot.delete_message(tel_id, message_id)


@dp.message_handler(lambda message: message.text == 'Изменить выбор')
async def change(message):
    await start(message)


@dp.callback_query_handler(lambda call: call.data.startswith('ege_math_base_'))
async def ege_math_base(call):
    tel_id = call.message.chat.id
    message_id = call.message.message_id

    switch_to = int(call.data[14:])
    await UsersDbManager.upd_ege_math_base(tel_id, switch_to, loop)

    kb = await mk.class_choose_ege(tel_id, loop)

    try:
        await bot.edit_message_text('Выбери предметы, которые ты будешь сдавать на ЕГЭ', tel_id, message_id,
                                    reply_markup=kb)
    except exceptions.MessageNotModified:
        print('Message is not modified')


@dp.callback_query_handler(lambda call: call.data.startswith('ege_math_pro_'))
async def ege_math_pro(call):
    tel_id = call.message.chat.id
    message_id = call.message.message_id

    switch_to = int(call.data[13:])
    await UsersDbManager.upd_ege_math_pro(tel_id, switch_to, loop)

    kb = await mk.class_choose_ege(tel_id, loop)

    try:
        await bot.edit_message_text('Выбери предметы, которые ты будешь сдавать на ЕГЭ', tel_id, message_id,
                                    reply_markup=kb)
    except exceptions.MessageNotModified:
        print('Message is not modified')


@dp.callback_query_handler(lambda call: call.data.startswith('ege_physics_'))
async def ege_physics(call):
    tel_id = call.message.chat.id
    message_id = call.message.message_id

    switch_to = int(call.data[12:])
    await UsersDbManager.upd_ege_physics(tel_id, switch_to, loop)

    kb = await mk.class_choose_ege(tel_id, loop)

    try:
        await bot.edit_message_text('Выбери предметы, которые ты будешь сдавать на ЕГЭ', tel_id, message_id,
                                    reply_markup=kb)
    except exceptions.MessageNotModified:
        print('Message is not modified')


@dp.callback_query_handler(lambda call: call.data.startswith('ege_history_'))
async def ege_history(call):
    tel_id = call.message.chat.id
    message_id = call.message.message_id

    switch_to = int(call.data[12:])
    await UsersDbManager.upd_ege_history(tel_id, switch_to, loop)

    kb = await mk.class_choose_ege(tel_id, loop)

    try:
        await bot.edit_message_text('Выбери предметы, которые ты будешь сдавать на ЕГЭ', tel_id, message_id,
                                    reply_markup=kb)
    except exceptions.MessageNotModified:
        print('Message is not modified')


@dp.callback_query_handler(lambda call: call.data.startswith('ege_social_'))
async def ege_social(call):
    tel_id = call.message.chat.id
    message_id = call.message.message_id

    switch_to = int(call.data[11:])
    await UsersDbManager.upd_ege_social(tel_id, switch_to, loop)

    kb = await mk.class_choose_ege(tel_id, loop)

    try:
        await bot.edit_message_text('Выбери предметы, которые ты будешь сдавать на ЕГЭ', tel_id, message_id,
                                    reply_markup=kb)
    except exceptions.MessageNotModified:
        print('Message is not modified')


@dp.callback_query_handler(lambda call: call.data.startswith('oge_math_'))
async def oge_math(call):
    tel_id = call.message.chat.id
    message_id = call.message.message_id

    switch_to = int(call.data[9:])
    await UsersDbManager.upd_oge_math(tel_id, switch_to, loop)

    kb = await mk.class_choose_oge(tel_id, loop)

    try:
        await bot.edit_message_text('Выбери предметы, которые ты будешь сдавать на ЕГЭ', tel_id, message_id,
                                    reply_markup=kb)
    except exceptions.MessageNotModified:
        print('Message is not modified')


@dp.callback_query_handler(lambda call: call.data.startswith('oge_physics_'))
async def oge_physics(call):
    tel_id = call.message.chat.id
    message_id = call.message.message_id

    switch_to = int(call.data[12:])
    await UsersDbManager.upd_oge_physics(tel_id, switch_to, loop)

    kb = await mk.class_choose_oge(tel_id, loop)

    try:
        await bot.edit_message_text('Выбери предметы, которые ты будешь сдавать на ЕГЭ', tel_id, message_id,
                                    reply_markup=kb)
    except exceptions.MessageNotModified:
        print('Message is not modified')


@dp.callback_query_handler(lambda call: call.data.startswith('oge_history_'))
async def oge_history(call):
    tel_id = call.message.chat.id
    message_id = call.message.message_id

    switch_to = int(call.data[12:])
    await UsersDbManager.upd_oge_history(tel_id, switch_to, loop)

    kb = await mk.class_choose_oge(tel_id, loop)

    try:
        await bot.edit_message_text('Выбери предметы, которые ты будешь сдавать на ЕГЭ', tel_id, message_id,
                                    reply_markup=kb)
    except exceptions.MessageNotModified:
        print('Message is not modified')


@dp.callback_query_handler(lambda call: call.data.startswith('oge_lit_'))
async def oge_lit(call):
    tel_id = call.message.chat.id
    message_id = call.message.message_id

    switch_to = int(call.data[8:])
    await UsersDbManager.upd_oge_lit(tel_id, switch_to, loop)

    kb = await mk.class_choose_oge(tel_id, loop)

    try:
        await bot.edit_message_text('Выбери предметы, которые ты будешь сдавать на ЕГЭ', tel_id, message_id,
                                    reply_markup=kb)
    except exceptions.MessageNotModified:
        print('Message is not modified')


@dp.callback_query_handler(lambda call: call.data.startswith('oge_social_'))
async def oge_social(call):
    tel_id = call.message.chat.id
    message_id = call.message.message_id

    switch_to = int(call.data[11:])
    await UsersDbManager.upd_oge_social(tel_id, switch_to, loop)

    kb = await mk.class_choose_oge(tel_id, loop)

    try:
        await bot.edit_message_text('Выбери предметы, которые ты будешь сдавать на ЕГЭ', tel_id, message_id,
                                    reply_markup=kb)
    except exceptions.MessageNotModified:
        print('Message is not modified')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)