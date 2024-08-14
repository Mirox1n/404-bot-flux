from telebot import types

import config
import telebot

TO_CHAT_ID = -1002237899357

bot = telebot.TeleBot("7468324581:AAGwdfqrMmER_2kOv4E5mShdLZpSN3IHtGg")

requests_queue = []


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,
                     "Здравствуйте!, {0.first_name}!\nЯ, бот который может связать вас с Администрацией Flux Project." .format(
                         message.from_user, bot.get_me()),
                     parse_mode='html')
    bot.register_next_step_handler(message, help_bot)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('СТАРТ')
    markup.add(itembtn1)
def help_bot(message):
    requests_queue.append((message.message_id, message.chat.id))
    bot.forward_message(TO_CHAT_ID, message.chat.id, message.message_id)
    markup_inline = types.InlineKeyboardMarkup([[
        types.InlineKeyboardButton(text='Ответить', callback_data=f'answer{message.chat.id}')
    ]])
    bot.send_message(TO_CHAT_ID, f"Действие:", reply_markup=markup_inline)
    bot.register_next_step_handler(message, help_bot)


@bot.message_handler(commands=["requests"], func=lambda m: int(m.chat.id) == int(TO_CHAT_ID))
def all_messages(message):
    bot.send_message(message.chat.id, "Доступные запросы:")
    for i, req in enumerate(requests_queue):
        bot.forward_message(TO_CHAT_ID, req[1], req[0])
        markup_inline = types.InlineKeyboardMarkup([[
            types.InlineKeyboardButton(text='Ответить', callback_data=f'answer{req[1]}')
        ]])
        bot.send_message(message.chat.id, f"Действие:", reply_markup=markup_inline)


def send_answer(message: types.Message, call, chat_id):
    bot.send_message(call.message.chat.id, "Ответ отправлен!")
    bot.send_message(chat_id, message.text)
    for i, req in enumerate(requests_queue):
        if int(req[1]) == int(chat_id):
            del requests_queue[i]


@bot.callback_query_handler(func=lambda call: True)
def answer_callback(call: types.CallbackQuery):
    if call.data.startswith("answer"):
        chat_id = int(call.data[6:])

        bot.send_message(call.message.chat.id, "Отправьте ответ на запрос")
        bot.register_next_step_handler(call.message, lambda msg: send_answer(msg, call, chat_id))


bot.polling(none_stop=True)