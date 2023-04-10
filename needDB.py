import sqlite3

def create_tables():
    conn = sqlite3.connect("needs_database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transcripts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            transcript TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS needs (
            id INTEGER PRIMARY KEY,
            need TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            need_id INTEGER,
            location TEXT,
            num_people INTEGER,
            demographics TEXT,
            effect INTEGER,
            FOREIGN KEY (user_id) REFERENCES transcripts (user_id),
            FOREIGN KEY (need_id) REFERENCES needs (id)
        )
    """)

    conn.commit()
    conn.close()

create_tables()




def insert_transcript(user_id, transcript):
    conn = sqlite3.connect("needs_database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transcripts (user_id, transcript) VALUES (?, ?)
    """, (user_id, transcript))

    conn.commit()
    conn.close()

def insert_need(need):
    conn = sqlite3.connect("needs_database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO needs (need) VALUES (?)
    """, (need,))

    conn.commit()
    need_id = cursor.lastrowid
    conn.close()

    return need_id

def insert_user_data(user_id, need_id, location, num_people, demographics, effect):
    conn = sqlite3.connect("needs_database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_data (user_id, need_id, location, num_people, demographics, effect)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, need_id, location, num_people, demographics, effect))

    conn.commit()
    conn.close()

# Example usage
user_id = 1
transcript = "I'm worried about affordable housing."
insert_transcript(user_id, transcript)

need = "affordable housing"
need_id = insert_need(need)

location = "New York"
num_people = 10
demographics = "Age: 25-34, Gender: Male"
effect = 4
insert_user_data(user_id, need_id, location, num_people, demographics, effect)
