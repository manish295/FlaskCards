import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

class Database:

    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                database="flashCardDB",
                user="postgres",
                password="manish2005" 
            )
            self.cur = self.conn.cursor()
            self.cur.execute('''
                    CREATE TABLE IF NOT EXISTS users(
                        user_id serial PRIMARY KEY,
                        name TEXT NOT NULL,
                        password TEXT NOT NULL
                    );
            ''')
            self.cur.execute('''
                    CREATE TABLE IF NOT EXISTS sets(
                        set_id serial PRIMARY KEY,
                        user_id INT NOT NULL,
                        set_name TEXT NOT NULL,
                        community BOOLEAN NOT NULL,
                        FOREIGN KEY(user_id)
                            REFERENCES users(user_id)
                            ON DELETE CASCADE
                    );
            ''')
            self.cur.execute('''
                    CREATE TABLE IF NOT EXISTS cards(
                        card_id serial PRIMARY KEY,
                        set_id INT NOT NULL,
                        question TEXT NOT NULL,
                        answer TEXT NOT NULL,
                        FOREIGN KEY(set_id)
                            REFERENCES sets(set_id)
                            ON DELETE CASCADE
                    );
            
            ''')
            self.conn.commit()
        except Exception as err:
            print(err)
            self.close()

    def verify_password(self, user_name, password):
        try:
            self.cur.execute("SELECT user_id, password FROM users WHERE name = %(user_name)s", {'user_name': user_name})
            results = self.cur.fetchall()
            if len(results) == 0:
                print("User does not exist!")
                return False
            else:
                for pwd in results:
                    if check_password_hash(pwd[1], password):
                        return pwd[0]
                print("Incorrect password!")
                return False

        except Exception as err:
            print(err)
            self.close()

    def add_user(self, user_name, user_password):
        try:
            user_password = generate_password_hash(user_password)
            self.cur.execute("INSERT INTO users(name, password) VALUES(%(user_name)s, %(user_password)s)", {'user_name': user_name, 'user_password': user_password})
            self.conn.commit()
            
        except Exception as err:
            print(err)
            self.close()

    def add_set(self, user_id, set_name):
        try:
            self.cur.execute("INSERT INTO sets(user_id, set_name, community) VALUES(%(user_id)s, %(set_name)s, FALSE) RETURNING set_id, set_name", {'user_id': user_id, 'set_name': set_name})
            self.conn.commit()
            result = self.cur.fetchall()
            return result
        except Exception as err:
            print(err)
            self.close()

    def add_card(self, set_id, question, answer):
        try:
            self.cur.execute("INSERT INTO cards(set_id, question, answer) VALUES(%(set_id)s, %(question)s, %(answer)s) RETURNING card_id", {'set_id': set_id, 'question': question, 'answer': answer})
            self.conn.commit()
            result = self.cur.fetchall()
            return result
        except Exception as err:
            print(err)
            self.close()


    def get_sets(self, user_id):
        try:
            self.cur.execute("SELECT set_id, set_name, community FROM sets WHERE user_id = %(user_id)s ORDER BY set_id", {'user_id': user_id})
            results = self.cur.fetchall()
            if len(results) == 0:
                return None
            else:
                print(results)
                return results

        except Exception as err:
            print(err)
            self.close()

    def get_sets_community(self):
        try:
            self.cur.execute("SELECT set_id, set_name, community FROM sets WHERE community = TRUE")
            results = self.cur.fetchall()
            if len(results) == 0:
                return None
            else:
                return results
        except Exception as err:
            print(err)
            self.close()
        
    def get_cards(self, set_id):
        try:
            self.cur.execute("SELECT card_id, question, answer FROM cards WHERE set_id = %(set_id)s", {'set_id': set_id})
            results = self.cur.fetchall()
            if len(results) == 0:
                return None
            else:
                return results

        except Exception as err:
            print(err)
            self.close()

    def update_set_name(self, set_id, set_name):
        try:
            self.cur.execute("UPDATE sets SET set_name = %(set_name)s WHERE set_id = %(set_id)s", {'set_name': set_name, 'set_id': set_id})
            self.conn.commit()
        except Exception as err:
            print(err)
            self.close()
    
    def update_community(self, set_id, value):
        try:
            self.cur.execute("UPDATE sets SET community = %(value)s WHERE set_id = %(set_id)s", {'value': value, 'set_id': set_id})
            self.conn.commit()
        except Exception as err:
            print(err)
            self.close()
    
    def update_card(self, card_id, question, answer):
        try:
            self.cur.execute("UPDATE cards SET question = %(question)s, answer = %(answer)s WHERE card_id = %(answer)s", {'question': question, 'answer': answer, 'card_id': card_id})
            self.conn.commit()
        except Exception as err:
            print(err)
            self.close()

    def delete_set(self, set_id):
        try:
            self.cur.execute("DELETE FROM sets WHERE set_id = %(set_id)s", {'set_id': set_id})
            self.conn.commit()
        except Exception as err:
            print(err)
            self.close()

    def delete_card(self, card_id):
        try:
            self.cur.execute("DELETE FROM cards WHERE card_id = %(card_id)s", {'card_id': card_id})
            self.conn.commit()
        except Exception as err:
            print(err)
            self.close()

    def close(self):
        self.conn.close()