import functools
import pickle
import sqlite3

THEPICKLESTORE="pickledb"

## @functools.lru_cache(maxsize=20)
def get_connection():
    conn = sqlite3.connect(THEPICKLESTORE)
    return conn

def save(key, thing):
    conn = get_connection()
    cursor = conn.cursor()
    pickled = pickle.dumps(thing)
    cursor.execute("REPLACE INTO pickles VALUES(?, ?)", (key,pickled,))
    conn.commit()

def get(key):
    conn = get_connection()
    cursor = conn.cursor()
    res = cursor.execute("select pickle from pickles where key=?", (key,))
    retrieved = res.fetchone()
    if retrieved:
        return pickle.loads(retrieved[0])
    return None

def main():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE if not exists
                      pickles(key STRING PRIMARY KEY, pickle BLOB)""")
    ## item = {"foo":"bar", "hello":"hello"}
    ## item2 = set(list(range(100)))
    ## save('item', item)
    ## save('item2', item2)
    ## print(item2 == get('item2'))
    ## print(item == get('item'))

if __name__ == "__main__": main()
