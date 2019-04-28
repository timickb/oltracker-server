import sqlite3

class Database():
    def __init__(self):
        self.conn = sqlite3.connect('user.db')
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute("CREATE TABLE interests (user_token text, subject text)")
        except:
            print('Database table already exists, skipping creation')
    
    def update_data(self, user_token, subject, flag):
        self.cursor.execute("SELECT * FROM interests WHERE user_token='{}' AND subject='{}'".format(user_token, subject))
        data = self.cursor.fetchall()
        if len(data) == 0:
            if flag:
                self.cursor.execute("INSERT INTO interests VALUES('{}', '{}')".format(user_token, subject))
                self.conn.commit()
                print('[Database] Inserted: {}, {}'.format(user_token, subject))
        else:
            if not flag:
                self.cursor.execute("DELETE FROM interests WHERE user_token='{}' AND subject='{}'".format(user_token, subject))
                print('[Database] Deleted: {}, {}'.format(user_token, subject))
                self.conn.commit()
