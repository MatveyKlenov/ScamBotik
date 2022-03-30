import sqlite3


class Database1:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users2` (`user_id`) VALUES (?)", (user_id,))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users2` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def set_nickname(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute("UPDATE `users2` SET `nickname` = ? WHERE `user_id` = ?", (nickname, user_id,))

    def get_signup(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `signup` FROM `users2` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE `users2` SET `signup` = ? WHERE `user_id` = ?", (signup, user_id,))

    def set_password(self, user_id, user_pass):
        with self.connection:
            return self.cursor.execute("UPDATE `users2` SET `user_pass` = ? WHERE `user_id` = ?", (user_pass, user_id,))

    def get_talk(self, user_id):
        with self.connection:
            result2 = self.cursor.execute("SELECT `talk` FROM `users2` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result2:
                talk1 = str(row[0])
            return talk1

    def set_talk(self, user_id, talk):
        with self.connection:
            return self.cursor.execute("UPDATE `users2` SET `talk` = ? WHERE `user_id` = ?", (talk, user_id,))