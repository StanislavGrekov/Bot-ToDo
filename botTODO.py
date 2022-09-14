import telebot

token = ' '

bot = telebot.TeleBot(token)

HELP = """
Команды:
help - напечатать справку по программе (например: /help).\n
add - добавить задачу в список (например: /add 15.09.2022 Купи хлеб).\n
show - напечатать добавленные задачи на соответствующую дату (например: /show 15.09.2022).\n
showall - покажет Вам все даты с соответствующими задачами (например: /showall).\n
today - добавление задачи на дату Сегодня (например: /today Помой машину).\n
clearing - удаление всех записей (например: /clearing).\n """

tasks = {}

def add_todo(date, task):
    '''
    Функция добавляет в словарь дату и задачу
    '''
    if date in tasks:
        tasks[date].append(task)
    else:
        tasks[date] = []
        tasks[date].append(task)

@bot.message_handler(commands=['help'])
def help(message):
    '''
    Функция печатает справку
    '''
    bot.send_message(message.chat.id, HELP)

@bot.message_handler(commands=['add'])
def add(message):
    '''
    Функция обрабатывает введенный текст, выполняет функцию add_todo и отправляет сообщения
    в канал чата
    '''
    command = message.text.split(maxsplit = 2)
    date = command[1].lower()
    task = command[2]
    if len(date) <=3 or len(task) <=3:
        text = 'Вы ввели некорректные значения!\nДлина даты или задачи меньше 3 символов.'
        bot.send_message(message.chat.id, text)
    else:
        add_todo(date,task)
        text = 'На дату: ' + date.upper() + ', Добавлена задача: ' + task
        bot.send_message(message.chat.id, text)
        print(tasks)

@bot.message_handler(commands=['show'])
def show(message):
    '''
    Функция выводит в канал чата задачи по указанной дате
    '''
    command = message.text.split(maxsplit=1)
    date = command[1].lower()
    print(date)
    if date in tasks:
        text = 'На дату '+date.upper()+', есть следующие задачи:'+'\n'
        bot.send_message(message.chat.id, text)
        for task in tasks[date]:
            text = '- '+task+'\n'
            bot.send_message(message.chat.id, text)

    else:
        text = 'Задач на эту дату нет!'
        bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['today'])
def random_add(message):
    '''
    Функция выводит в канал чата задачи по дате Сегодня
    '''
    command = message.text.split(maxsplit = 1)
    task = command[1]
    date = 'сегодня'
    if len(task) <= 3:
        text = 'Вы ввели некорректные значения!\nДлина задачи меньше 3 символов.'
        bot.send_message(message.chat.id, text)
    else:
        add_todo(date, task)
        text = 'На дату: ' + date.upper() + ', Добавлена задача: ' + task
        bot.send_message(message.chat.id, text)
        print(tasks)

@bot.message_handler(commands=['showall'])
def showall(message):
    '''
    Функция покажет все задачи по датам из словаря
    '''
    for date, task in tasks.items():
        date = str(date)
        text = 'На дату: '+date.upper()+', есть следующие задачи:\n'
        bot.send_message(message.chat.id, text)
        for element in task:
            text = '- ' + element + '\n'
            bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['clearing'])
def clearing(message):
    '''
    Функция очистит словарь
    '''
    tasks.clear()
    text = 'Все записи удалены!'
    bot.send_message(message.chat.id, text)
    print(tasks)

#Постоянное обращение к серверам телеграмма
bot.polling(none_stop = True)