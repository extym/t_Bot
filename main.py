from calendar import calendar
from random import choice
from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE
from telebot.types import ReplyKeyboardRemove, CallbackQuery
import telebot
from config import token
from datetime import datetime

# from telegram import  ReplyKeyboardRemove,ParseMode, Update
# #import telegram_bot_calendar
# import telegramcalendar


bot = telebot.TeleBot(token)
desire_day = None
desire_hour = None
now = datetime.now()
sheduler = {}
task = "Запись"

RANDOM_TASKS = ['Написать Гвидо письмо', 'Выучить Python', 'Записаться на курс в Нетологию',
                'Посмотреть 4 сезон Рик и Морти']
# todos = dict()

HELP = '''
Список доступных команд:
* print  - напечать все задачи на заданную дату
* todo - добавить задачу
* random - добавить на сегодня случайную задачу
* help - Напечатать help
'''


def check_busy(date, time):
    pass


def has_full_date():
    if desire_day is not None and desire_hour is not None:
        file = open("test.txt", "w")
        file.write(desire_day, desire_hour)
        file.close()
        return True
    else:
        return False


def add_todo(day, time):
    busy = False
    if (sheduler.get(day) is not None) and (time not in sheduler[day]):
        sheduler[day].append(time)
        file = open("test1.txt", "w")
        file.write(sheduler)
        file.close()
    # elif (sheduler.get(day) is not None) and (time in sheduler[day]):
    #     busy = True

    else:
        sheduler[day] = [time]


def log(message, answer):
    print("\n ---------")
    print(datetime.now())
    print("Сообщение от {0} {2}, (id = {2}) \n TEXT = {3}"
          .format(message.from_user.first_name, message.from_user.last_name, str(message.from_user.id), message.text))

    print(answer)


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('/start', '/stop', '/add')
    user_markup.row('Что может?', 'Как купить?', 'Где хранить?')
    user_markup.row('Купить такого бота', 'Get consult')
    user_markup.row('/show')  # Посмотреть еще ботов на сайте')
    bot.send_message(message.from_user.id, 'Добро пожаловать!', reply_markup=user_markup)


@bot.message_handler(commands=['stop'])
def handle_start(message):
    # hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, '..ta da')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, HELP)


# @bot.message_handler(commands=['random'])
# def random(message):
#     task = choice(RANDOM_TASKS)
#     add_todo('сегодня', task)
#     bot.send_message(message.chat.id, f'Задача {task} добавлена на сегодня')

@bot.message_handler(commands=['add'])
def add(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('/DATE', '/TIME')
    bot.send_message(message.chat.id, "Выберите ДАТУ или ВРЕМЯ для выбора времени: ", reply_markup=user_markup)


@bot.message_handler(commands=['TIME'])
def desire_hour(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('09:00', '10:00', '11:00', '12:00')
    user_markup.row('13:00', '14:00', '15:00', '16:00')
    user_markup.row('17:00', '18:00', '19:00', '20:00')
    bot.send_message(message.from_user.id, "Выберите удобное время: ", reply_markup=user_markup)
    # add_todo(desire_time)


calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_callback = CallbackData("desired_day", "action", "year", "month", "day")


@bot.message_handler(commands=['DATE'])
def calendar_date_choose(message):
    now = datetime.now()
    bot.send_message(
        message.from_user.id,
        "Selected date",
        reply_markup=calendar.create_calendar(
            name=calendar_callback.prefix,
            year=now.year,
            month=now.month,
        )
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_callback.prefix))
def callback_inline(call: telebot.types.CallbackQuery):
    name, action, year, month, day = call.data.split(calendar_callback.sep)
    desire_day = calendar.calendar_query_handler(bot=bot, call=call, name=name, action=action, year=year, month=month,
                                                 day=day)
    add_todo(desire_day, desire_hour)
    if action == 'DAY':
        bot.send_message(chat_id=call.from_user.id, text=f'Вы выбрали {desire_day.strftime("%d.%m.%Y")}',
                         reply_markup=telebot.types.ReplyKeyboardRemove())

    elif action == 'CANCEL':
        bot.send_message(chat_id=call.from_user.id, text='Отмена', reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(commands=['show'])
def print_(message):
    day = message.text.split(" ")[1].lower()
    if day in sheduler:
        tasks = ''
        for task in sheduler[day]:
            tasks += f'[ ] {task}\n'
    else:
        tasks = 'Такой даты нет'
    bot.send_message(message.chat.id, tasks)
    print("!---", sheduler)


@bot.message_handler(content_types=['text'])
def what_can(message):
    if message.text == 'Что может?':
        bot.send_message(message.from_user.id, 'Робот может информировать потенциальных клиентов и предлагать им ваши '
                                               'услуги. \n Информировать существующих клиентов и помогать им, '
                                               'например записаться на прием к специалисту (медику, парикмахеру, '
                                               'преподавателю). ')
    elif message.text == 'Как купить?':
        bot.send_message(message.from_user.id,
                         'Вы можете приобрести бота здесь, по ссылке https://brain-trust.ru/baybot , на сайте')
    elif message.text == 'Где хранить?':
        bot.send_message(message.from_user.id, "Робота можно поселить на домашнем компьютере, на стороннем хостинге, "
                                               "у нас за 299 рублей в месяц (мы за ним присмотрим)).")
    elif message.text == '09:00' or '10:00' or '11:00' or '12:00' or '13:00' or '14:00' \
            or '15:00' or '16:00' or '17:00' or '18:00' or '19:00' or '20:00':
        desire_hour = str(message.text)
        # if desire_day :
        # add_todo(desire_time)
        bot.send_message(message.from_user.id, f"Вы выбрали запись на  {desire_hour} часов.")

        if not has_full_date():
            bot.send_message(message.from_user.id, "Choose date", reply_markup=calendar.create_calendar(
            name=calendar_callback.prefix,
            year=now.year,
            month=now.month,
        ),)

        else:
            bot.send_message(message.from_user.id,
                             f"Если правильно понял, Вы хотите записаться на {desire_day}  {desire_hour}")
            add_todo(desire_day, desire_hour)
            print("!---", sheduler)
            print(add_todo(desire_day, desire_hour))
    else:
        answer = "Ничего не понятно. Хотите связаться с оператором?"
        bot.send_message(message.from_user.id, answer)


bot.polling(none_stop=True)
# import logging
# import time
# import sys
# while True:
#     try:
#       bot.polling(none_stop=True)
#     except:
#       print('bolt')
#       logging.error('error: {}'.format(sys.exc_info()[0]))
#       time.sleep(20)
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
