import config
import dbworker
from def_for_bot import (zapis_on_bt_end, zapis_data, get_russian_date_info, get_available_times,
                         make_available_times_keyboard, bulk_safe_delete_message)
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import time
from datetime import datetime
from threading import Lock
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import datetime
from telebot import types
import time
from datetime import date, time
from datetime import datetime
from requests import post
from telebot.apihelper import ApiTelegramException
import datetime
from telebot import types
from collections import defaultdict
from bs4 import BeautifulSoup
import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sqlite3
import config
from enum import Enum


BSH_API_URL = 'https://baltshina.ru/zapis/?shag=1&mas=1'
bot = telebot.TeleBot('8348470380:AAF3FYu-0SJu1v0UXuyjQSBXTbzuRIZICKg')




db_file = "database.db"

class States(Enum):
    S_START = "0"
    S_TART = "1"
    S_ENTER_DATA = "2"
    S_ENTER_TOTAL = "3"
    S_ENTER_TIME = "4"
    S_ENTER_TEL = "5"
    S_ENTER_NAME = "6"
    S_ENTER_N_AME = "7"

    S_SEND_PIC = "8"
    S_SEND_PIC_OUT = "9"
    CANCEL = "10"


def init_db():
    with sqlite3.connect(config.db_file) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_states (
                user_id TEXT PRIMARY KEY,
                state TEXT NOT NULL
            )
        ''')
        conn.commit()



def get_current_state(user_id):
    with sqlite3.connect(config.db_file) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT state FROM user_states WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()

        if row:
            return row[0]
        else:
            return config.States.S_START.value



def set_state(user_id, value):
    with sqlite3.connect(config.db_file) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT OR REPLACE INTO user_states (user_id, state) VALUES (?, ?)', (user_id, value))
            conn.commit()
            return True
        except Exception as e:

            print(f"Ошибка при сохранении состояния: {e}")
            return False



init_db()



service = Service(ChromeDriverManager().install())
options = Options()
def zapis_on_bt_end(t_ime, day, name_master, user_name, phone):
    pass
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    #
    #
    #
    #
    # # browser = webdriver.Chrome(service=service, options=options)
    # browser = webdriver.Chrome(service=service, options=chrome_options)
    # # Открытие веб-страницы
    # browser.get('https://baltshina.ru/zapis/?shag=1&mas=1')
    # # Явное ожидание для поиска элементов
    # wait = WebDriverWait(browser, 20)
    # # Телефон и имя
    # elem1 = wait.until(EC.visibility_of_element_located((By.NAME, 'name')))
    # elem2 = wait.until(EC.visibility_of_element_located((By.NAME, 'tel')))
    # elem1.clear()
    # elem1.send_keys(user_name)  # Ваше имя
    # elem2.clear()
    # elem2.send_keys(phone)  # Ваш телефон
    # # Число
    # TARGET_DAY = day
    # if TARGET_DAY < datetime.date.today().day:
    #     NEXT_MONTH_BUTTON_XPATH = "//a[@title='Next']"
    #     next_month_button = wait.until(EC.element_to_be_clickable((By.XPATH, NEXT_MONTH_BUTTON_XPATH)))
    #     next_month_button.click()
    #     time.sleep(0.7)
    # day_link = browser.find_element(By.XPATH, f"//div[@id='datepicker-inline']//a[text()='{TARGET_DAY}']")
    # day_link.click()
    # # Время и мастер
    # TARGET_MASTER = name_master
    # TARGET_TIME = t_ime
    # time_radio_xpath = (
    #     f"//div[@id='interval'][.//h2[text()='{TARGET_MASTER}']]"
    #     f"/div/label[contains(., '{TARGET_TIME}')]"
    #     f"/input[@type='radio' and @name='timei' and not(@disabled)]"
    # )
    # time_slot_radio = wait.until(EC.element_to_be_clickable((By.XPATH, time_radio_xpath)))
    # time_slot_radio.click()
    # print(f"Время {TARGET_TIME} для мастера {TARGET_MASTER} выбрано.")
    # # Кнопка записаться
    # submit_button = wait.until(
    #     EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Записаться']"))
    # )
    # submit_button.click()
    # print("Кнопка 'Записаться' нажата.")
    # # time.sleep(10)
    # browser.quit()


def zapis_data():
    today = datetime.date.today()
    keyboard = types.InlineKeyboardMarkup()
    for i in range(7):
        date = today + datetime.timedelta(days=i)
        day, month = get_russian_date_info(date)
        button = types.InlineKeyboardButton(f"{date.day} {month} ({day})", callback_data=f"button{i}")
        keyboard.add(button)
    return keyboard


def get_russian_date_info(selected_date):
    # Получаем сегодняшнюю дату
    today = datetime.date.today()

    # Получаем индекс дня недели (0 - понедельник, 6 - воскресенье)
    day_of_week_index = selected_date.weekday()

    # Массив дней недели на русском
    days_of_week_russian = [
        "понедельник",  # 0
        "вторник",     # 1
        "среда",       # 2
        "четверг",     # 3
        "пятница",      # 4
        "суббота",     # 5
        "воскресенье"  # 6
    ]


    # Получаем название дня недели на русском
    day_of_week_russian = days_of_week_russian[day_of_week_index]

    # Получаем индекс месяца
    month_index = selected_date.month

    # Массив названий месяцев на русском
    months_russian = [
                "января",   # 1
                "февраля",  # 2
                "марта",    # 3
                "апреля",   # 4
                "мая",      # 5
                "июня",     # 6
                "июля",     # 7
                "августа",  # 8
                "сентября", # 9
                "октября",  # 10
                "ноября",   # 11
                "декабря"   # 12
            ]

    # Получаем название месяца на русском
    month_name_russian = months_russian[month_index - 1]
    # Проверяем, является ли выбранная дата сегодняшней или завтрашней
    if selected_date == today:
        return "сегодня", month_name_russian
    elif selected_date == today + datetime.timedelta(days=1):
        return "завтра", month_name_russian

    return day_of_week_russian, month_name_russian




def get_available_times(date: date):
    response = post(
        "https://baltshina.ru/zapis/interval.php",
        data=f"date={date.isoformat()}^&id=1",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    inter = response.json()["inter"]
    if "Нет свободных мест" in inter:
        return []


    soup = BeautifulSoup(inter, 'html.parser')
    available_times = defaultdict(list)
    employee_divs = soup.find_all('div', style="width: 150px;float: left;")
    for employee_div in employee_divs:
        name = employee_div.find('h2').text.strip()
        labels = employee_div.find_all('label')
        for label in labels:
            if any(map(lambda x: "background-color:#C00" in x, label.get_attribute_list("style"))):
                continue
            time_text = label.get_text(strip=True)
            input_element = label.find('input')
            if input_element:
                time_value = input_element['value']
                available_times[name].append(time_text)
    print('Данные с сайта успешно спарсины функцией get_available_times')
    print(available_times)
    return available_times




def make_available_times_keyboard(employe_name: str, available_times: list[str]):
    if available_times:
        markup = types.InlineKeyboardMarkup()
        buttons = []
        for available_time in available_times:
            button = types.InlineKeyboardButton(text=available_time, callback_data=f'time_{available_time}_{employe_name}')
            buttons.append(button)
        for i in range(0, len(buttons), 2):
            markup.row(*buttons[i:i + 2])
        return markup






def safe_delete_message(bot, chat_id, msg_id):
    try:
        bot.delete_message(chat_id, msg_id)
    except ApiTelegramException as error:
        if "delete not found" not in error.description:
            raise



def bulk_safe_delete_message(bot, chat_id, msg_ids):
    for msg_id in msg_ids:
        safe_delete_message(bot, chat_id, msg_id)







scheduler = BackgroundScheduler()
scheduler.start()  # запустить один раз при старте приложения


def send_reminder(chat_id, time):
    try:
        if dbworker.get_current_state(chat_id) != config.States.CANCEL.value:
            keyboard_cancel = types.InlineKeyboardMarkup()
            button_back = types.InlineKeyboardButton(f"❌ Отменить запись ❌", callback_data="cancel")
            keyboard_cancel.row(button_back)

            bot.send_message(chat_id,
                             f"❗ Напоминание ❗\n\nВы записаны на шиномонтаж через 4 часа ({time})✔️\n\n*📍 Адрес: ул. Цветочная д. 18*\n\nЕсли вы хотите отменить запись, пожалуйста, позвоните по любому номеру:\n☎️ (812)611-10-66\n (812)324-40-99\n\n\nМы вас ждем!"
                             , reply_markup=keyboard_cancel)
            print("Отправленно в чат")
        else:
            print(f'НАПОМИНАНИЕ ОТМЕНЕНО! {time}')
    except Exception as e:
        print("Ошибка отправки:", e)


def schedule_with_aps(chat_id, appointment_time, time_total, hours_before=24):
    reminder_time = appointment_time - datetime.timedelta(hours=hours_before)
    scheduler.add_job(send_reminder, 'date', run_date=reminder_time, args=[chat_id, time_total])
    print("APScheduler: напоминание запланировано на", reminder_time)


class FSMStorage:
    _data_lock = Lock()

    def __init__(self):
        self._data = {}

    def get_data(self, user_id, chat_id) -> dict:
        with self._data_lock:
            return self._data.get((user_id, chat_id), {}).copy()

    def set_data(self, user_id, chat_id, data) -> None:
        with self._data_lock:
            self._data[(user_id, chat_id)] = data

    def add_data(self, user_id, chat_id, key, value) -> None:
        with self._data_lock:
            if (user_id, chat_id) not in self._data:
                self._data[(user_id, chat_id)] = {}
            self._data[(user_id, chat_id)][key] = value


fsm_storage = FSMStorage()


@bot.message_handler(commands=['start'])
def start(message):
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', message.chat.id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("Запись на шиномонтаж")
    keyboard.add(button1)
    bot.send_message(message.chat.id,
                     '🌟 Привет! 👋\n\n🚗 Я помогу вам записаться на шиномонтаж к опытным специалистам! \n\n🛠️ Нажмите кнопку "Записаться на шиномонтаж", чтобы начать.',
                     reply_markup=keyboard)
    dbworker.set_state(message.chat.id, config.States.S_TART.value)


@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    state = dbworker.get_current_state(message.chat.id)
    if state == config.States.S_SEND_PIC_OUT.value:
        bot.send_message(message.chat.id,
                         'Вы уже записались на шиномонтаж.\nЕсли вам нужно записать еще одну машину нажмите "Записаться на шиномонтаж"')

    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = KeyboardButton("Запись на шиномонтаж")
        keyboard.add(button1)
        bot.send_message(message.chat.id,
                         'Что ж, если появится желаение записаться на шиномонтаж, нажми кнопку "Запись на шиномонтаж", чтобы начать.',
                         reply_markup=keyboard)
        dbworker.set_state(message.chat.id, config.States.S_TART.value)


@bot.message_handler(func=lambda message: message.text == "Запись на шиномонтаж")
def handle_message(message):
    state = dbworker.get_current_state(message.chat.id)
    if state == config.States.S_SEND_PIC_OUT.value:
        bot.send_message(message.chat.id, "Я очень рад, что вы снова выбрали нас!",
                         reply_markup=types.ReplyKeyboardRemove())

    else:
        bot.send_message(message.chat.id, "Прекрасно! Давайте начнем!", reply_markup=types.ReplyKeyboardRemove())

    msg = bot.send_message(message.chat.id, "🗓 Выберите день для записи 🗓", reply_markup=zapis_data())
    fsm_data = fsm_storage.get_data(
        message.chat.id,
        message.from_user.id,
    )
    fsm_data.setdefault("delete_messages_ids", []).append(msg.id)
    fsm_storage.set_data(
        message.chat.id,
        message.from_user.id,
        fsm_data,
    )

    dbworker.set_state(message.chat.id, config.States.S_ENTER_DATA.value)


@bot.callback_query_handler(func=lambda call: call.data.startswith('button'))
def callback_query(call):
    fsm_data = fsm_storage.get_data(
        call.message.chat.id,
        call.from_user.id,

    )
    bulk_safe_delete_message(bot, call.message.chat.id, fsm_data.pop("delete_messages_ids", []))
    bot.answer_callback_query(call.id)
    today = datetime.date.today()
    button_days = {
        "button0": 0,
        "button1": 1,
        "button2": 2,
        "button3": 3,
        "button4": 4,
        "button5": 5,
        "button6": 6
    }
    target_date = today + datetime.timedelta(days=button_days[call.data])
    print(target_date)
    print("!!!!!!!!!!!!")
    delete_messages_ids = []
    delete_messages_id = []
    all_available_time = get_available_times(target_date)
    fsm_data = {
        "selected_day": target_date.day,
        "delete_messages_ids": delete_messages_ids,
        "delete_messages_id": delete_messages_id,
        "all_time": all_available_time,
        "selected_total": target_date
    }
    selected_date = fsm_data["selected_total"]
    day, month = get_russian_date_info(selected_date)

    if not get_available_times(target_date):
        msg = bot.send_message(call.message.chat.id,
                               f'К сожалению на {target_date.day} {month} нет свободных мест. 🙁\n----------------------------------------------------------------\n\nПожалуйста, выберите другой день:',
                               reply_markup=zapis_data())
        delete_messages_ids.append(msg.id)
    else:
        msg = bot.send_message(call.message.chat.id, f'Свободные мастера на {target_date.day} {month}:')
        delete_messages_ids.append(msg.message_id)

        for employe_name, available_times in all_available_time.items():
            msg = bot.send_message(call.message.chat.id, employe_name + '👨🏽‍🔧',
                                   reply_markup=make_available_times_keyboard(employe_name, available_times))
            delete_messages_ids.append(msg.message_id)

        keyboard_end = types.InlineKeyboardMarkup()
        button_back = types.InlineKeyboardButton('🔙 Назад', callback_data="end_button")
        keyboard_end.add(button_back)
        msg = bot.send_message(call.message.chat.id, 'Во сколько вам было бы удобнее?', reply_markup=keyboard_end)
        delete_messages_ids.append(msg.message_id)

    fsm_storage.set_data(
        call.message.chat.id,
        call.from_user.id,
        fsm_data,
    )

    dbworker.set_state(call.message.chat.id, config.States.S_ENTER_TIME.value)


# ________________________________ ПЕРВАЯ КНОПКА НАЗАД___(back)________________________________
@bot.callback_query_handler(func=lambda call: call.data == 'end_button')
def handle_end_button(call):
    fsm_data = fsm_storage.get_data(
        call.message.chat.id,
        call.from_user.id,
    )
    bulk_safe_delete_message(bot, call.message.chat.id, fsm_data.pop("delete_messages_ids", []))
    bulk_safe_delete_message(bot, call.message.chat.id, fsm_data.pop("delete_messages_id", []))
    bot.answer_callback_query(call.id)
    msg = bot.send_message(call.message.chat.id, "🗓 Выберите день для записи 🗓", reply_markup=zapis_data())

    fsm_data.setdefault("delete_messages_ids", []).append(msg.id)

    fsm_storage.set_data(
        call.message.chat.id,
        call.from_user.id,
        fsm_data,
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('time_'))
def handle_time_selection(call):
    bot.answer_callback_query(call.id)
    fsm_data = fsm_storage.get_data(
        call.message.chat.id,
        call.from_user.id,
    )
    bulk_safe_delete_message(bot, call.message.chat.id, fsm_data.get("delete_messages_ids", []))
    selected_time = call.data[5:10]
    fsm_data["selected_time"] = selected_time
    fsm_data["selected_name_master"] = call.data[call.data.rfind('_') + 1:]

    keyboard_end = types.InlineKeyboardMarkup()
    button_next = types.InlineKeyboardButton('✅ Подтвердить', callback_data="next_button")
    keyboard_end.add(button_next)
    button_back = types.InlineKeyboardButton('❌ Назад', callback_data="end_button1")
    keyboard_end.add(button_back)

    time.sleep(0.2)
    msg = bot.send_message(call.message.chat.id, f'⌚️ Вы выбрали время {selected_time} ⌚️', reply_markup=keyboard_end)
    fsm_data.setdefault("delete_messages_id", []).append(msg.id)

    fsm_storage.set_data(
        call.message.chat.id,
        call.from_user.id,
        fsm_data,
    )

    dbworker.set_state(call.message.chat.id, config.States.S_ENTER_TOTAL.value)


@bot.callback_query_handler(func=lambda call: call.data == 'next_button' or call.data == 'end_button1')
def handle_time_selection(call):
    try:
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      reply_markup=None)
    except telebot.apihelper.ApiTelegramException as e:
        # Игнорируем только конкретную ошибку "message is not modified"
        if "message is not modified" in str(e):
            print("Клавиатура уже удалена — пропускаем")
        else:
            raise  # пробросить другие ошибки

    # bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    time.sleep(0.3)
    if call.data == 'next_button':
        # fsm_data = fsm_storage.get_data(
        #     call.message.chat.id,
        #     call.from_user.id,
        #
        # )
        # bulk_safe_delete_message(bot, call.message.chat.id, fsm_data.pop("delete_messages_ids", []))
        # print(fsm_data.pop("delete_messages_ids", []), '@@@')
        bot.answer_callback_query(call.id)
        time.sleep(0.15)
        bot.send_message(call.message.chat.id, f'📲 Напишите ваш телефон:')
        dbworker.set_state(call.message.chat.id, config.States.S_ENTER_TEL.value)



    elif call.data == 'end_button1':
        bot.answer_callback_query(call.id)
        fsm_data = fsm_storage.get_data(
            call.message.chat.id,
            call.from_user.id,

        )
        bulk_safe_delete_message(bot, call.message.chat.id, fsm_data.pop("delete_messages_ids", []))
        bulk_safe_delete_message(bot, call.message.chat.id, fsm_data.pop("delete_messages_id", []))

        bot.answer_callback_query(call.id)

        all_t = fsm_data["all_time"]

        for employe_name, available_times in all_t.items():
            msg1 = bot.send_message(call.message.chat.id, employe_name + '👨🏽‍🔧',
                                    reply_markup=make_available_times_keyboard(employe_name, available_times))
            fsm_data.setdefault("delete_messages_ids", []).append(msg1.id)

        keyboard_end = types.InlineKeyboardMarkup()
        button_back = types.InlineKeyboardButton('Назад к выбору даты', callback_data="end_button")
        keyboard_end.add(button_back)
        msg = bot.send_message(call.message.chat.id, 'Выберите другое время', reply_markup=keyboard_end)
        fsm_data.setdefault("delete_messages_ids", []).append(msg.id)

        fsm_storage.set_data(
            call.message.chat.id,
            call.from_user.id,
            fsm_data,
        )

        dbworker.set_state(call.message.chat.id, config.States.S_ENTER_TIME.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_TEL.value)
def user_entering_tel(message):
    if (message.text.startswith('+') and message.text[1:].isdigit()) or message.text.isdigit():
        fsm_data = fsm_storage.get_data(
            message.chat.id,
            message.from_user.id,
        )

        fsm_data['input_phone'] = message.text
        fsm_storage.set_data(
            message.chat.id,
            message.from_user.id,
            fsm_data,
        )
        keyboard_end = types.InlineKeyboardMarkup()
        button_back = types.InlineKeyboardButton('✅ Подтвердить', callback_data="YES_button")
        keyboard_end.row(button_back)
        button_next = types.InlineKeyboardButton('❌ Изменить', callback_data="next_button")
        keyboard_end.add(button_next)

        time.sleep(0.15)
        msg = bot.send_message(message.chat.id, "Подтвердите ваш номер телефона", reply_markup=keyboard_end)
        fsm_data.setdefault("delete_messages_ids", []).append(msg.id)

        fsm_storage.set_data(
            message.chat.id,
            message.from_user.id,
            fsm_data,
        )
        dbworker.set_state(message.chat.id, config.States.S_SEND_PIC.value)
    else:
        bot.send_message(message.chat.id, "🚩 что-то пошло не так, попробуйте еще раз!")
        return


@bot.callback_query_handler(func=lambda call: call.data == ('YES_button'))
def get_phone_input(call):
    bot.answer_callback_query(call.id)
    fsm_data = fsm_storage.get_data(
        call.message.chat.id,
        call.from_user.id,
    )

    bulk_safe_delete_message(bot, call.message.chat.id, fsm_data.pop("delete_messages_ids", []))
    time.sleep(0.2)
    bot.send_message(call.message.chat.id, 'Прекрасно! 📝 Напишите ваше имя:')

    dbworker.set_state(call.message.chat.id, config.States.S_ENTER_NAME.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_NAME.value)
def get_name_input(message):
    fsm_data = fsm_storage.get_data(
        message.chat.id,
        message.from_user.id,
    )
    input_name = message.text
    fsm_data['input_name'] = input_name
    fsm_storage.set_data(
        message.chat.id,
        message.from_user.id,
        fsm_data,
    )

    print(fsm_data['selected_time'], 'selected_time')

    keyboard_end = types.InlineKeyboardMarkup()
    button_back = types.InlineKeyboardButton('✅ Подтвердить', callback_data="END_button")
    keyboard_end.row(button_back)
    button_next = types.InlineKeyboardButton('❌ Изменить', callback_data="next_name_button")
    keyboard_end.add(button_next)
    time.sleep(0.15)
    msg = bot.send_message(message.chat.id, "Подтвердите ваше имя:", reply_markup=keyboard_end)
    fsm_data.setdefault("delete_messages_ids", []).append(msg.id)

    fsm_storage.set_data(
        message.chat.id,
        message.from_user.id,
        fsm_data,
    )

    dbworker.set_state(message.chat.id, config.States.S_SEND_PIC.value)


@bot.callback_query_handler(func=lambda call: call.data == 'next_name_button' or call.data == 'END_button')
def handle_time_selection(call):
    fsm_data = fsm_storage.get_data(
        call.message.chat.id,
        call.from_user.id,
    )
    bulk_safe_delete_message(bot, call.message.chat.id, fsm_data.pop("delete_messages_ids", []))

    if call.data == 'next_name_button':
        bot.answer_callback_query(call.id)
        msg = bot.send_message(call.message.chat.id, "📝 Напишите ваше имя:")
        dbworker.set_state(call.message.chat.id, config.States.S_ENTER_NAME.value)

    else:
        bot.answer_callback_query(call.id)

        selected_date = fsm_data["selected_total"]
        day, month = get_russian_date_info(selected_date)

        keyboard_end = types.InlineKeyboardMarkup()
        button_back = types.InlineKeyboardButton(f"☑ Подтвердить запись", callback_data="confirmation_button")
        keyboard_end.row(button_back)

        button_back = types.InlineKeyboardButton(f"❌ Отменить запись", callback_data="not_confirmation_button")
        keyboard_end.row(button_back)

        bot.send_message(call.message.chat.id, f"🚨 Остался последний шаг! 🚨\n\n🗒 Проверьте данные:\n\n"
                                               f"👨🏽‍🔧 мастер {fsm_data['selected_name_master']}\n"
                                               f"🗓 {fsm_data['selected_day']} {month} ({day})\n"
                                               f"🕒 {fsm_data['selected_time']}", reply_markup=keyboard_end)

        dbworker.set_state(call.message.chat.id, config.States.S_SEND_PIC.value)


@bot.callback_query_handler(func=lambda call: call.data in ['confirmation_button', 'not_confirmation_button'])
def handle_zapis(call):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("Запись на шиномонтаж")
    keyboard.add(button1)

    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    bot.answer_callback_query(call.id)

    if call.data == 'confirmation_button':
        fsm_data = fsm_storage.get_data(
            call.message.chat.id,
            call.from_user.id,
        )

        msg = bot.send_message(call.message.chat.id, "Ожидайте...")
        fsm_data.setdefault("delete_messages_ids", []).append(msg.id)

        date_str = fsm_data["selected_total"].strftime("%Y-%m-%d")
        appointment_str = f'{date_str} {fsm_data["selected_time"]}'
        appointment_time = datetime.datetime.strptime(appointment_str, "%Y-%m-%d %H:%M")

        fsm_storage.add_data(call.from_user.id, call.message.chat.id, "data_total", appointment_time)
        time = fsm_data["selected_time"]

        # ----------------------------------------------------

        # appointment_time = datetime.datetime(2025, 11, 23, 19, 35   )  # Воскресенье, 16:00
        # schedule_with_aps(call.message.chat.id, appointment_time, time)

        # -------------------------------

        schedule_with_aps(call.message.chat.id,
                          fsm_storage.get_data(call.from_user.id, call.from_user.id)["data_total"], time)

        zapis_on_bt_end(
            fsm_data['selected_time'],
            fsm_data['selected_day'],
            fsm_data['selected_name_master'],
            fsm_data['input_name'],
            fsm_data['input_phone'],
        )

        keyboard_cancel = types.InlineKeyboardMarkup()
        button_back = types.InlineKeyboardButton(f"❌ Отменить запись ❌", callback_data="cancel")
        keyboard_cancel.row(button_back)

        selected_date = fsm_data["selected_total"]
        day, month = get_russian_date_info(selected_date)

        bulk_safe_delete_message(bot, call.message.chat.id, fsm_data.pop("delete_messages_ids", []))

        bot.send_message(
            call.message.chat.id,

            f"       ✔️ Запись подтверждена! ✔️\n\n"
            f"{fsm_data['input_name']}, Cпасибо за ваш выбор Baltshina 🛞 \n\n"
            f"✅ Вы записались:\n"
            f"     ▫️ Шиномонтаж\n\n"
            f""
            f"к мастеру {fsm_data['selected_name_master']}\n"
            f"👉 на {fsm_data['selected_day']} {month} ({day}) в {fsm_data['selected_time']}\n\n"
            f""
            f"*Baltshina*. Выполняем работу качественно.\n"
            f"ПН-ПТ: 9.30-18.00 \nСБ-ВС: 9.30-16.00\n\n"
            f""
            f"*Адрес: ул. Цветочная д. 18*\n"
            f"☎️ (812)611-10-66\n"
            f"    (812)324-40-99\n"
            f"📍наш caйт и on-line запись 24/7⬇\n"
            f"*https://baltshina.ru/zapis/?shag=1&mas=1\n\n\n\n"

            f""
            f""
            f"⭐️ Поддержка @kiriltyre ⭐️\n\n\n"
            f""
            f"Мы вас ждем!\n\n", reply_markup=keyboard)

        bot.send_message(call.message.chat.id, 'Чтобы отменить запись нажмите ниже', reply_markup=keyboard_cancel)

        # fsm_storage.set_data(
        #     call.message.chat.id,
        #     call.message.from_user.id,
        #     fsm_data,
        # )

        dbworker.set_state(call.message.chat.id, config.States.S_SEND_PIC_OUT.value)

    else:

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = KeyboardButton("Запись на шиномонтаж")
        keyboard.add(button1)
        bot.send_message(call.message.chat.id,
                         '✅ Запись отменена. ✅\n\nЕсли появится желаение записаться на шиномонтаж, нажми кнопку "Запись на шиномонтаж", чтобы начать.',
                         reply_markup=keyboard)
        dbworker.set_state(call.message.chat.id, config.States.S_TART.value)


@bot.callback_query_handler(func=lambda call: call.data == 'cancel' and dbworker.get_current_state(
    call.message.chat.id) != config.States.CANCEL.value)
def handle_cancel(call):
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    bot.answer_callback_query(call.id)
    fsm_data = fsm_storage.get_data(
        call.message.chat.id,
        call.from_user.id,
    )
    selected_date = fsm_data["selected_total"]
    day, month = get_russian_date_info(selected_date)

    bot.send_message(call.message.chat.id,
                     '❌ Запись отменена. ❌\n\nЕсли появится желаение записаться на шиномонтаж, нажми кнопку "Запись на шиномонтаж", чтобы начать.')
    # bot.send_message(303325895, f"❌ Запись отменена ❌ \n\n\n{fsm_data['selected_day']} {month} ({day}) в {fsm_data['selected_time']}\n\nДанные клиента:\nНомер телефона: {fsm_data['input_phone']}\nИмя: {fsm_data['input_name']}\n\nВозможно, запись уже отменена, проверь⬇⬇⬇\n{'https://baltshina.ru/zapis/?shag=1&mas=1'}")
    # bot.send_message(1814986681, f"❌ Запись отменена ❌ \n\n\n{fsm_data['selected_day']} {month} ({day}) в {fsm_data['selected_time']}\n\nДанные клиента:\nНомер телефона: {fsm_data['input_phone']}\nИмя: {fsm_data['input_name']}\n\nВозможно, запись уже отменена, проверь⬇⬇⬇\n{'https://baltshina.ru/zapis/?shag=1&mas=1'}")
    # bot.send_message(1501918078, f"❌ Запись отменена ❌ \n\n\n{fsm_data['selected_day']} {month} ({day}) в {fsm_data['selected_time']}\n\nДанные клиента:\nНомер телефона: {fsm_data['input_phone']}\nИмя: {fsm_data['input_name']}\n\nВозможно, запись уже отменена, проверь⬇⬇⬇\n{'https://baltshina.ru/zapis/?shag=1&mas=1'}")

    dbworker.set_state(call.message.chat.id, config.States.CANCEL.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.chat.id) in [config.States.S_SEND_PIC.value,
                                                                         config.States.S_TART.value,
                                                                         config.States.S_ENTER_DATA.value,
                                                                         config.States.S_ENTER_TIME.value,
                                                                         config.States.S_ENTER_TOTAL.value,
                                                                         config.States.S_SEND_PIC_OUT.value])
def get_name_input(message):
    bot.delete_message(message.chat.id, message.message_id)
    # bot.reply_to(message, 'Похоже вам что-то непонятно. Нажмите /help')


# Запуск бота
bot.infinity_polling()
