import telebot
import sqlite3
import random
from logic import *
from config import TOKEN
token = TOKEN
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    add_user(name, user_id)
    bot.reply_to(message, f"Привет, {name}! Ты успешно зарегистрирован с ID {user_id}.")
    bot.send_message(message.chat.id, "Добро пожаловать в Quiz Bot! Я помогу тебе проверить свои знания в различных областях.")
    bot.send_message(message.chat.id, "Воспользуйся командой /help, чтобы узнать доступные команды.")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "Команды:\n/start - регистрация\n/question - получить случайный вопрос\n/help - показать это сообщение")

@bot.message_handler(commands=['question'])
def send_question(message):
    user_id = get_user_id(message.from_user.first_name)

    if not user_id:
        bot.reply_to(message, "Сначала зарегистрируйся через /start.")
        return
    question = get_random_question(user_id)
    if not question:
        bot.reply_to(message, "Вопросы закончились.")
        return

    markup = telebot.types.InlineKeyboardMarkup()
    for option in question["options"]:
        callback_data = f"answer|{question['id']}|{option}"
        markup.add(
            telebot.types.InlineKeyboardButton(
                text=option,
                callback_data=callback_data
            )
        )
    bot.send_message(
        message.chat.id,
        f" Тема: {question['topic']}\n\n{question['question']}",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("answer"))
def handle_answer(call):
    user_id = get_user_id(call.from_user.first_name)

    _, question_id, selected_answer = call.data.split("|")
    question_id = int(question_id)

    # Получаем правильный ответ из БД
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT correct_answer FROM questions WHERE id = ?", (question_id,))
    correct_answer = c.fetchone()[0]
    conn.close()
    is_correct = int(selected_answer == correct_answer)
    record_answer(user_id, question_id, is_correct)

    if is_correct:
        bot.answer_callback_query(call.id, "✅ Правильно!")
    else:
        bot.answer_callback_query(call.id, "❌ Неправильно!")

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

@bot.message_handler(commands=['shown'])
def shown(message):
    user_id = get_user_id(message.from_user.first_name)

    if not user_id:
        bot.reply_to(message, "Сначала зарегистрируйся через /start.")
        return
    shown_qs = shown_questions(user_id)
    if not shown_qs:
        bot.reply_to(message, "Пока не было показано ни одного вопроса.")
        return

    bot.reply_to(message, f"Показанные вопросы: {', '.join(map(str, shown_qs))}")
if __name__ == "__main__":  
    bot.polling()