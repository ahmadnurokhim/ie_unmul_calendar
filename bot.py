import telebot
import gcal

authorized_users = []
session_status = {}
with open('auth_users.txt', 'r') as f:
    authorized_users = f.readlines()

bot = telebot.TeleBot('6083862705:AAELCK86PSVUgsq1rspyJJmWPyIGnxQLOd8')

@bot.message_handler(commands=['help', 'start'])
def welcome(msg: telebot.types.Message):
    welcome_text = "Welcome! This is a bot to help IE Unmul Student scheduling event using Google Calendar"
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("How to Access the Calendar", callback_data="cal_access"))
    markup.add(telebot.types.InlineKeyboardButton("Add Seminar/Sidang", callback_data="add_sem_sid"))
    markup.add(telebot.types.InlineKeyboardButton("Add Event", callback_data="add_event"))
    markup.add(telebot.types.InlineKeyboardButton("Request to be Authorized User", callback_data="req_auth_user"))
    
    bot.send_message(chat_id=msg.chat.id, text=welcome_text, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda cb: cb.data == "cal_access")
def cal_access(call: telebot.types.CallbackQuery):
    bot.send_message(call.from_user.id, r"To subscribe the Google calendar, [Click Here](https://calendar.google.com/calendar/u/2?cid=NTA5YTc0ODYwYTFjYTM2ZjAyZGYyNTc0NjNlODk5ZTA2Y2QzMTQwMDljOGFmY2E4YTIxNzJhMGNiZTdiNjc4MEBncm91cC5jYWxlbmRhci5nb29nbGUuY29t)", parse_mode='Markdown')
    bot.send_message(call.from_user.id, r"To view the public calendar, [Click Here](https://calendar.google.com/calendar/embed?src=509a74860a1ca36f02df257463e899e06cd314009c8afca8a2172a0cbe7b6780%40group.calendar.google.com&ctz=Asia%2FSingapore)", parse_mode='Markdown')

@bot.callback_query_handler(func=lambda cb: cb.data == "req_auth_user")
def req_auth_user(call: telebot.types.CallbackQuery):
    bot.send_message()

@bot.callback_query_handler(func=lambda cb: cb.data == "add_sem_sid")
def add_sem_sid(call: telebot.types.CallbackQuery):
    if str(call.from_user.id) not in authorized_users:
        bot.send_message(call.from_user.id, "You're not authorized")
        return
    bot.send_message(call.from_user.id, "Send me the event in the following format:")
    bot.send_message(call.from_user.id, '''\
📌 [SEMINAR PROPOSAL SKRIPSI]

Your Name
1900000000
Senin, 06 Februari 2023
13.00 - 14.30 wite
di Ruang I.A2, Gedung I, Fakultas Teknik

Your Thesis Title (Desc)

🎓 Lecturer 1
🎓 Lecturer 2
🎓 Lecturer 3
🎓 Lecturer 4
''')

@bot.callback_query_handler(func=lambda cb: cb.data == "add_event")
def add_sem_sid(call: telebot.types.CallbackQuery):
    if str(call.from_user.id) not in authorized_users:
        bot.send_message(call.from_user.id, "You're not authorized")
        return
    bot.send_message(call.from_user.id, "Send me the event in the following format: NAME_AGE")


@bot.message_handler(func=lambda msg: True)
def reply_msg(msg: telebot.types.Message):
    if str(msg.from_user.id) not in authorized_users:
        bot.reply_to(msg, "You're not authorized"+msg.from_user.id)
        return
    if msg.text[0] != "📌":
        return

    creds = gcal.quickstart()
    try:
        event_name, date_start, date_end, location, desc = gcal.get_event_details(msg.text)
        gcal.add_event(creds, event_name, date_start, date_end, location, desc)
        bot.reply_to(msg, f"Event created ({event_name})")
    except Exception as e:
        bot.reply_to(msg, f"Can't add event: {e}")
        

bot.infinity_polling()