import string
from calendar import calendar
from random import choice

# from telegram import message

from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE
from telebot.types import ReplyKeyboardRemove, CallbackQuery
import telebot
from config import token
from datetime import datetime

# from telegram import  ReplyKeyboardRemove,ParseMode, Update
# #import telegram_bot_calendar
# import telegramcalendar


bot = telebot.TeleBot(token)
desire_day = 'proxy_day'
desire_hour = None
now = datetime.now()
sheduler = {}
date = {}
book = {}
customer = dict(name=None, last_name=None, phone=None, nickname=None)
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

user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
user_markup.row('09:00', '10:00', '11:00', '12:00')
user_markup.row('13:00', '14:00', '15:00', '16:00')
user_markup.row('17:00', '18:00', '19:00', '20:00')


class Booking:
    def __init__(self, time, name, lastname, phone, user_id):
        self.time = time
        self.name = name
        self.lastname = lastname
        self.phone = phone
        self.user_id = user_id


    # if customer[time] is None:
    #     customer[time] = desire_hour
    # if customer[name] is None:
    #     customer["name"] = name
    # if customer[lastname] is None:
    #     customer["lastname"] = lastname
#     # if customer[phone] is None:
    #     customer[phone] = customer_phone


def log(message, answer):
    print("\n ---------")
    print(datetime.now())
    print("Сообщение от {0} {2}, (id = {2}) \n TEXT = {3}"
          .format(message.from_user.first_name, message.from_user.last_name, str(message.from_user.id), message.text))

    print(answer)

def sheduler_write(string):
    file = open("test.txt", "a")
    file.write(str(string) + '\n')
    file.write('\n')
    file.close()


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('/start', '/stop', '/add')
    user_markup.row('Что может?', 'Как купить?', 'Где хранить?')
    user_markup.row('Купить такого бота', 'Get consult')
    user_markup.row('/show')  # Посмотреть еще ботов на сайте')
    bot.send_message(message.from_user.id, 'Добро пожаловать!', reply_markup=user_markup)

desire_day = None
desire_hour = None

#Проверка
# def check_full_date(day, time):
#     book = dict(time, customer)
#     date = dict(day, book)
#     if  date.get(day) is not None:
#         date[day].append(time)
#     elif date.get(day) == "proxy_day":
#         date.update("proxy_day", desire_hour)
#     else:
#         # date[day] = desire_day
#         # date [time] = desire_hour
#         date[day] = [time]
#     sheduler_write(date)
#     return date



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
def chose_desire_hour(message):
    bot.send_message(message.from_user.id, "Выберите удобное время: ", reply_markup=user_markup)
    # add_todo(desire_time)


calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_callback = CallbackData("desired_day", "action", "year", "month", "day")



@bot.message_handler(commands=['DATE'])
def calendar_date_choose(message):
    now = datetime.now()
    bot.send_message(
        message.from_user.id,
        "Select date",
        reply_markup=calendar.create_calendar(
            name=calendar_callback.prefix,
            year=now.year,
            month=now.month,
        )
    )

# Add day to sheduler for booking
def add_day(day, book):
    if day is not None:
        print(day, desire_day)
    #     sheduler[day].append(desire_day)
    # else:
        sheduler[day] = [desire_day]
    file = open("test1.txt", "w")
    file.write(str(sheduler))
    file.close()

@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_callback.prefix))
def callback_inline(call: telebot.types.CallbackQuery):
    name, action, year, month, day = call.data.split(calendar_callback.sep)
    d_day = calendar.calendar_query_handler(bot=bot, call=call, name=name, action=action, year=year, month=month,
                                            day=day)
    if action == 'DAY':
        bot.send_message(chat_id=call.from_user.id, text=f'Вы выбрали {d_day.strftime("%d.%m.%Y")}',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        global desire_day
        desire_day = d_day.strftime("%d.%m.%Y")
        global date
        date = add_day(desire_day, book)
        print("11", date)
        sheduler_write(date)
        if desire_hour is None:  # check_busy(desire_day, desire_hour):
            bot.send_message(chat_id=call.from_user.id, text="Выберите удобное время: ", reply_markup=user_markup)
            print("111", sheduler)

    elif action == 'CANCEL':
        bot.send_message(chat_id=call.from_user.id, text='Отмена', reply_markup=telebot.types.ReplyKeyboardRemove())



# Create booking to desire time for customer to desire day
def add_book(time, customer):
    if time is not None:
        date.update(desire_hour)
        date[desire_day][desire_hour] = customer
    else:
        date[time] = [desire_day]
        date[desire_day][desire_hour] = customer
    file = open("test1.txt", "w")
    file.write(str(date))
    file.close()



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
    print("2", sheduler)


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
        global desire_hour
        desire_hour = str(message.text)
        print("444", date, desire_day)

        date[desire_day] = desire_hour

        print("1212121", type(date), date, sheduler)


        bot.send_message(message.from_user.id, f"Вы выбрали запись на  {desire_hour} часов.")
        customer["name"] = message.from_user.username #first_name.from_user
        add_day(desire_day, desire_hour)
        print("3", sheduler, customer)
        if  date[desire_day] == "proxy_day": #not check_full_date():
            bot.send_message(message.from_user.id, "Choose date", reply_markup=calendar.create_calendar(
                name=calendar_callback.prefix,
                year=now.year,
                month=now.month,
            ), )

        else:
            bot.send_message(message.from_user.id,
                             f"Если правильно понял, Вы хотите записаться на {desire_day}  {desire_hour}")
            add_book(desire_hour, customer)
        print("3", sheduler)
        print("4", add_book())
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
