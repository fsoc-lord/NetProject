import sqlite3


def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        """
DELETE FROM users;

    """
    )
    conn.commit()
    conn.close()
    
init_db()