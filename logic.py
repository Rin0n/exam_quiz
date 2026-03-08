import sqlite3
import random

def create_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # users
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id     INTEGER PRIMARY KEY,
        name   TEXT,
        joined DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # questions
    c.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        topic          TEXT    NOT NULL,
        question       TEXT    NOT NULL,
        correct_answer TEXT    NOT NULL,
        wrong_answers  TEXT    NOT NULL
    )
    ''')

    # answers
    c.execute('''
    CREATE TABLE IF NOT EXISTS answers (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id     INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        is_correct  INTEGER NOT NULL,
        answered_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # shown
    c.execute('''
    CREATE TABLE IF NOT EXISTS shown (
        user_id     INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        shown_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, question_id)
    )
    ''')

    conn.commit()

    # Проверяем, пустая ли таблица
    c.execute("SELECT COUNT(*) FROM questions")
    count = c.fetchone()[0]

    if count == 0:
        fill_questions()

    conn.close()


def fill_questions():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    questions_data = [
        (
            "Физика",
            "Чему равна сила тока при напряжении 12В и сопротивлении 4 Ом?",
            "3 А",
            "2 А, 4 А, 6 А"
        ),
        (
            "Физика",
            "Что происходит при коротком замыкании?",
            "Сила тока резко возрастает",
            "Ток исчезает, Напряжение увеличивается, Сопротивление увеличивается"
        ),
        (
            "Информатика",
            "Какой тип данных используется для хранения текста в Python?",
            "str",
            "int, float, bool"
        ),
        (
            "Информатика",
            "Какой оператор используется для сравнения в Python?",
            "==",
            "!=, <, >" 
        ),
        ("Математика",
         "Чему равна площадь круга с радиусом 5?",
         "25π",
         "10π, 20π, 30π"
        ),
        ("Математика",
         "Какой из следующих чисел является простым?(4, 6, 7, 9)",
         "7",
         "4, 6, 9"
        )
    ]

    cursor.executemany('''
    INSERT INTO questions (topic, question, correct_answer, wrong_answers)
    VALUES (?, ?, ?, ?)
    ''', questions_data)

    conn.commit()
    conn.close()


def add_user(name, user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (name, id) VALUES (?, ?)', (name, user_id))
    conn.commit()
    conn.close()
    return user_id


def get_user_id(name):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE name = ?', (name,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def get_random_question(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
    SELECT q.id, q.topic, q.question, q.correct_answer, q.wrong_answers
    FROM questions q
    LEFT JOIN shown s 
        ON q.id = s.question_id AND s.user_id = ?
    WHERE s.question_id IS NULL
    ORDER BY RANDOM()
    LIMIT 1
    ''', (user_id,))

    row = c.fetchone()
    conn.close()

    if not row:
        return None

    question_id, topic, question_text, correct_answer, wrong_answers = row
    wrong_list = wrong_answers.split(', ')
    options = [correct_answer] + wrong_list
    random.shuffle(options)

    return {
        "id": question_id,
        "topic": topic,
        "question": question_text,
        "correct": correct_answer,
        "options": options
    }

def record_answer(user_id, question_id, is_correct):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute(
        'INSERT INTO answers (user_id, question_id, is_correct) VALUES (?, ?, ?)',
        (user_id, question_id, is_correct)
    )

    c.execute(
        'INSERT OR IGNORE INTO shown (user_id, question_id) VALUES (?, ?)',
        (user_id, question_id)
    )

    conn.commit()
    conn.close()

def shown_questions(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT question_id FROM shown WHERE user_id = ?', (user_id,))
    rows = c.fetchall()
    conn.close()
    return [row[0] for row in rows]

if __name__ == "__main__":
    create_table()