import sqlite3 as sq

def create_db():
    with sq.connect("notes.db") as con:
        cur = con.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS note (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            header TEXT NOT NULL,
            text TEXT NOT NULL,
            time_write TEXT NOT NULL
        )
        """)


def add_note(header, text, user_id, time_write):
    with sq.connect("notes.db") as con:
        cur = con.cursor()

        cur.execute(f'INSERT INTO note (user_id, header, text, time_write) VALUES (?, ?, ?, ?)',
            (user_id, header, text, time_write))
    

def show_notes(user_id):
    with sq.connect("notes.db") as con:
        cur = con.cursor()

    
        cur.execute(f"""SELECT id, header, text, time_write FROM note
        WHERE user_id={user_id}
        """)
        data_for_del = cur.fetchall()
        text = f'<b>Ваши заметки</b>\n\n'
        for data in data_for_del:

            text = text+f'''{data[1]} | {data[2]} | {data[3]} | /del{data[0]}\n'''
        return text

def count_list(user_id: int):
    with sq.connect("notes.db") as con:
        cur = con.cursor()
        sql_count = "SELECT COUNT(id) FROM note WHERE user_id = {}".format(
            user_id)
        cur.execute(sql_count)
        count = cur.fetchone()
        return count


def del_note(user_id, id):
    with sq.connect("notes.db") as con:
        cur = con.cursor()
        cur.execute(f"""DELETE FROM note
        WHERE id={id} AND user_id={user_id}""")

