from random import choice
import telebot
from config import token
import datetime
from telegram import  ReplyKeyboardRemove,ParseMode, Update
#import telegram_bot_calendar
import telegramcalendar
import utils

bot = telebot.TeleBot(token)
day = 0
curr_mounth = 0
need_hour = 0
sheduler = {}
task="Запись"

RANDOM_TASKS = ['Написать Гвидо письмо', 'Выучить Python', 'Записаться на курс в Нетологию',
                'Посмотреть 4 сезон Рик и Морти']
#todos = dict()

HELP = '''
Список доступных команд:
* print  - напечать все задачи на заданную дату
* todo - добавить задачу
* random - добавить на сегодня случайную задачу
* help - Напечатать help
'''


def add_todo(date, task):
    date = date.lower()
    if sheduler.get(date) is not None:
        sheduler[date].append(task)
    else:
        sheduler[date] = [task]


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
    user_markup.row('/show') #Посмотреть еще ботов на сайте')
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

    # upd = bot.get_updates()
    # last_update = upd[-1]
    # date = last_update.message
    #print(date, message)
    #task = #input("Введите время") #' '.join([tail])
    # add_todo(date, task)
    # bot.send_message(message.chat.id, f'Задача {task} добавлена на дату {date}')


@bot.message_handler(commands=['DATE'])
def calendar_handler(message):
    #user_markup = telegram_bot_calendar.MONTH
    bot.send_message(message.from_user.id, "Please select a date: ",
                        reply_markup=telegramcalendar.create_calendar())


def inline_handler(bot,update):
    selected,date = telegramcalendar.process_calendar_selection(bot, update)
    if selected:
        bot.send_message(chat_id=update.callback_query.from_user.id,
                        text="You selected %s" % (date.strftime("%d/%m/%Y")),
                        reply_markup=ReplyKeyboardRemove())


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
                                               "у нас за 99 рублей в месяц (мы за ним присмотрим)).")
    elif message.text.isdigit():
        day = message.text
        # if data[0].isdigit():
        #     day = data[0]
        #     curr_mounth = data[1]


        bot.send_message(message.from_user.id, f"Если правильно понял, Вы хотите записаться на {day}")
        add_todo(day, task)
    else:
        answer = "Ничего не понятно. Хотите связаться с оператором?"
        bot.send_message(message.from_user.id, answer)



bot.polling(none_stop=True)
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
