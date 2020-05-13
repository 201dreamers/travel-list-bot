import telebot
from telebot import types

from config.bot import TOKEN, COMMANDS_LIST, COMMANDS_DESCRIPTION, add_step
from bot_backend import db_get_chat, db_update_chat, db_get_places, \
    db_update_places, db_remove_places, get_step, place_exists


bot = telebot.TeleBot(TOKEN)


def create_main_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(
            text=command.capitalize(),
            callback_data=command
        )
        for command in COMMANDS_LIST
    ]
    keyboard.add(*buttons)

    return keyboard


def create_skip_stop_keyboard(skip=True):
    if skip:
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            types.InlineKeyboardButton(
                text='Пропустити',
                callback_data='skip'
            ),
            types.InlineKeyboardButton(
                text='Завершити',
                callback_data='stop'
            )
        )
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            types.InlineKeyboardButton(
                text='Завершити',
                callback_data='stop'
            )
        )
    return keyboard


def send_menu(message):
    bot.send_message(
            chat_id=message.chat.id,
            text='---------[Menu]---------',
            reply_markup=create_main_keyboard()
        )


def send_success_message(message, place_id):
    if place_exists(message, place_id):
        bot.send_message(
            chat_id=message.chat.id,
            text='Успішно додано',
            reply_markup=create_main_keyboard()
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text='Щось пішло не так...',
            reply_markup=create_main_keyboard()
        )


@bot.message_handler(commands=['start'])
def start_command_handler(message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Привіт, я збережу всі місця' +
        ' які ти б хотів відвідати в майбутньому.\n' +
        'Доступні комманди:\n' +
        '\n'.join([
            f"/{command.get('name')}, /{command.get('shortcut')} - " +
            f"{command.get('description')}"
            for command in COMMANDS_DESCRIPTION
        ]),
        reply_markup=create_main_keyboard()
    )


@bot.message_handler(
    func=lambda message: get_step(message.chat.id) == add_step.OFF,
    commands=['add', 'a']
)
def add_command_handler(message):
    db_update_chat(chat_id=message.chat.id, step=add_step.NAME)
    bot.send_message(
        chat_id=message.chat.id,
        text='Напишіть назву'
    )


@bot.message_handler(
    func=lambda message: get_step(message.chat.id) == add_step.NAME,
    content_types=['text']
)
def add_place_name_handler(message):
    place = db_update_places(message=message, bot=bot)

    db_update_chat(
        chat_id=message.chat.id,
        step=add_step.LOCATION,
        place_id=place.id
    )

    bot.send_message(
        chat_id=message.chat.id,
        text='Додайте геолокацію',
        reply_markup=create_skip_stop_keyboard()
    )


@bot.message_handler(
    func=lambda message: get_step(message.chat.id) == add_step.LOCATION,
    content_types=['location']
)
def add_location_handler(message):
    db_update_places(
        message=message,
        bot=bot,
        place_id=db_get_chat(message.chat.id).place.id
    )
    db_update_chat(
        chat_id=message.chat.id,
        step=add_step.PHOTO,
    )

    bot.send_message(
        chat_id=message.chat.id,
        text='Додайте фото',
        reply_markup=create_skip_stop_keyboard()
    )


@bot.message_handler(
    func=lambda message: get_step(message.chat.id) == add_step.PHOTO,
    content_types=['photo']
)
def add_photo_handler(message):
    db_update_places(
        message=message,
        bot=bot,
        place_id=db_get_chat(message.chat.id).place.id
    )
    db_update_chat(
        chat_id=message.chat.id,
        step=add_step.COMMENT
    )

    bot.send_message(
        chat_id=message.chat.id,
        text='Напишіть коментар',
        reply_markup=create_skip_stop_keyboard(skip=False)
    )


@bot.message_handler(
    func=lambda message: get_step(message.chat.id) == add_step.COMMENT,
    content_types=['text']
)
def add_comment_handler(message):
    db_update_places(
        message=message,
        bot=bot,
        place_id=db_get_chat(message.chat.id).place.id
    )
    db_chat = db_update_chat(
        chat_id=message.chat.id,
        step=add_step.OFF
    )

    send_success_message(
        message=message,
        place_id=db_chat.place.id
    )


@bot.message_handler(commands=['list', 'l'])
def list_command_handler(message):
    places = db_get_places(message.chat.id, -10)

    if places.all():
        for place in places.all():

            text_about = f'Назва: {place.name}'
            if place.comment:
                text_about += f'\nКоментар: {place.comment}'

            if place.photo_id:
                message_about = bot.send_photo(
                    chat_id=message.chat.id,
                    photo=place.photo_id,
                    caption=text_about
                )
            else:
                message_about = bot.send_message(
                    chat_id=message.chat.id,
                    text=text_about
                )

            if place.latitude and place.longitude:
                bot.send_location(
                    chat_id=message.chat.id,
                    latitude=place.latitude,
                    longitude=place.longitude,
                    reply_to_message_id=message_about.message_id
                )
        send_menu(message)
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text='Немає збережених локацій',
            reply_markup=create_main_keyboard()
        )


@bot.message_handler(commands=['reset', 'r'])
def reset_command_handler(message):
    db_remove_places(message)
    db_update_chat(
            chat_id=message.chat.id,
            step=add_step.OFF
        )
    if not db_get_places(message.chat.id, 0).all():
        bot.send_message(
            chat_id=message.chat.id,
            text='Успішно видалено',
            reply_markup=create_main_keyboard()
        )


@bot.message_handler(commands=['help', 'h'])
def help_command_handler(message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Доступні комманди:\n' +
        '\n'.join([
            f"/{command.get('name')}, /{command.get('shortcut')} - " +
            f"{command.get('description')}"
            for command in COMMANDS_DESCRIPTION
        ]),
        reply_markup=create_main_keyboard()
    )


@bot.callback_query_handler(func=lambda query: query.data in COMMANDS_LIST)
def main_query_handler(callback_query):
    message = callback_query.message
    data = callback_query.data

    if data == 'add':
        add_command_handler(message)
    if data == 'list':
        list_command_handler(message)
    if data == 'reset':
        reset_command_handler(message)
    if data == 'help':
        help_command_handler(message)


@bot.callback_query_handler(
    func=lambda query: get_step(query.message.chat.id) in (
        add_step.LOCATION,
        add_step.PHOTO,
        add_step.COMMENT
    )
)
def add_skip_query_handler(callback_query):
    message = callback_query.message
    data = callback_query.data

    if data == 'skip':
        step = get_step(message.chat.id)
        if step == add_step.LOCATION:
            add_location_handler(message)
        elif step == add_step.PHOTO:
            add_photo_handler(message)
        else:
            data = 'stop'

    if data == 'stop':
        db_chat = db_update_chat(
            chat_id=message.chat.id,
            step=add_step.OFF
        )
        send_success_message(
            message=message,
            place_id=db_chat.place.id
        )


@bot.message_handler(content_types=["text", "voice"])
def other_messages_handler(message):
    send_menu(message)


@bot.message_handler(content_types=['left_chat_member'])
def signout_messages_handler(message):
    print('left_chat_member')
    reset_command_handler(message)


bot.polling(none_stop=False)
