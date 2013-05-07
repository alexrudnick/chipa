import functools
import pickle
import sqlite3

THEDB="/space/pickles/trainingdb"

@functools.lru_cache(maxsize=20)
def get_connection():
    conn = sqlite3.connect(THEDB)
    return conn

def save(word, thing):
    conn = get_connection()
    cursor = conn.cursor()
    pickled = pickle.dumps(thing)
    cursor.execute("insert INTO training VALUES(?, ?)", (word,pickled,))
    conn.commit()

def get_all(word):
    conn = get_connection()
    cursor = conn.cursor()
    res = cursor.execute("select pickle from training where word=?", (word,))
    retrieved = res.fetchall()
    if retrieved:
        out = []
        for item in retrieved:
            out.append(pickle.loads(item[0]))
        return out
    return None

def clear():
    """Delete all the instances in the db."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""delete from training""")
    conn.commit()

def main():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE if not exists
                      training(word STRING, pickle BLOB)""")
    conn.commit()

if __name__ == "__main__": main()
