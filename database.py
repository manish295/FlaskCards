import psycopg2

class Database:

    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="flashCardDB",
            user="postgres",
            password="manish2005" 
        )
        self.cur = self.conn.cursor()
    
    def handle_user(self, user_name, user_password):
        try:
            self.cur.execute(f"SELECT user_id FROM users WHERE name = '{user_name}' AND password = '{user_password}'")
            results = self.cur.fetchall()
            if len(results) == 0:
                print("User does not exist! Adding now")
                self.add_user(user_name, user_password)
                return self.handle_user(user_name, user_password)

            else:
                print("User exists")
                return results

        except Exception as err:
            print(err)
            self.close()

    def add_user(self, user_name, user_password):
        try:
            self.cur.execute(f"INSERT INTO users(name, password) VALUES('{user_name}', '{user_password}')")
            self.conn.commit()
            
        except Exception as err:
            print(err)
            self.close()

    def add_set(self, user_id, set_name):
        try:
            self.cur.execute(f"INSERT INTO sets(user_id, set_name) VALUES('{user_id}', '{set_name}') RETURNING set_id, set_name")
            self.conn.commit()
            result = self.cur.fetchall()
            return result
        except Exception as err:
            print(err)
            self.close()

    def add_card(self, set_id, question, answer):
        try:
            self.cur.execute(f"INSERT INTO cards(set_id, question, answer) VALUES({set_id}, '{question}', '{answer}') RETURNING card_id")
            self.conn.commit()
            result = self.cur.fetchall()
            return result
        except Exception as err:
            print(err)
            self.close()


    def get_sets(self, user_id):
        try:
            self.cur.execute(f"SELECT set_id, set_name FROM sets WHERE user_id = {user_id}")
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
            self.cur.execute(f"SELECT card_id, question, answer FROM cards WHERE set_id = {set_id}")
            results = self.cur.fetchall()
            if len(results) == 0:
                return None
            else:
                return results

        except Exception as err:
            print(err)
            self.close()

    def delete_set(self, set_id):
        try:
            self.cur.execute(f"DELETE FROM sets WHERE set_id = {set_id}")
            self.conn.commit()
        except Exception as err:
            print(err)
            self.close()

    def delete_card(self, card_id):
        try:
            self.cur.execute(f"DELETE FROM cards WHERE card_id = {card_id}")
            self.conn.commit()
        except Exception as err:
            print(err)
            self.close()

    def close(self):
        self.conn.close()