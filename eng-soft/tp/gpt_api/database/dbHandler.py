from dotenv import load_dotenv
import sys
sys.path.append('../')
from modules.utils.forms import *
from modules.utils.utils import *
import os
load_dotenv()
import psycopg2

class DatabaseHandler:
    def __init__(self):
        self.conn_params = {
            "host": os.getenv('HOST'),
            "port": 5432,
            "database": os.getenv('DATABASE'), 
            "user": os.getenv('ACCESS_USERNAME'), 
            "password": os.getenv('PASSWORD') 
        }
        self._conn = None

        self._set_connection()

    def _get_connection(self):
        return psycopg2.connect(**self.conn_params)
    
    def _set_connection(self):
        self._conn = self._get_connection()
        if self._conn:
            return True
        else:
            return False


    def get_cursor(self, conn):
        '''
        This function returns a cursor object
        It also calls the error responser module if needed
        '''
        cursor = conn.cursor()
        
        if not conn or not cursor:
            raise Exception("Connection not established")
        
        return cursor

    def initialize_user(self, id):
        with self._conn as conn:
            with self.get_cursor(conn) as cursor:
                # Select user
                cursor.execute("SELECT * FROM iara.user WHERE id = %s;", (str(id),))
                if cursor.fetchone():
                    pass
                else:
                    # Insert user in every database
                    print(cursor)
                    cursor.execute("INSERT INTO iara.user (id) VALUES (%s);", (str(id),))
                    cursor.execute("INSERT INTO iara.last_messages (user_id) VALUES (%s);", (str(id),))                    
                    pass


    def insert_user(self, user:User) -> id:
        """
        This function inserts a user in the database

        Args:
            user (User): The user object to be inserted

        Returns:
            User: user with new info
        """
        with self._conn as conn:
            with self.get_cursor(conn) as cursor:
                cursor.execute("INSERT INTO iara.user (id, name) VALUES (%s, %s) RETURNING id;", (user.id, user.name))
                return User(id=cursor.fetchone()[0], name=user.name,)


    
    def update_user(self, user:User):
        """
        This function updates the user in the database

        Args:
            user (User): The user object to be updated

        Returns:
            (bool): True if the user was updated, False otherwise
        """
        with self._conn as conn:
            with self.get_cursor(conn) as cursor:
                updates = []
                values = []


                if user.name:
                    updates.append("name = %s")
                    values.append(user.name)
                

                if values:
                    values.append(user.id)
                    query = "UPDATE iara.user SET " + ", ".join(updates) + " WHERE id = %s RETURNING id;"
                    cursor.execute(query, values)
                    if cursor.fetchone():
                        return True
                    else:
                        return False
                return False
            


    def check_user_exists(self, user_id:str) -> bool:
        """
        Verifica se um usuário existe na tabela iara.user pelo ID.
        
        Args:
            user_id (str): O ID do usuário a ser verificado.
            
        Return: 
            (bool): True se o usuário existir, False caso contrário.
        """
        query = "SELECT EXISTS(SELECT 1 FROM iara.user WHERE id = %s)"
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(query, (user_id,))
                return cursor.fetchone()[0]
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False
                

    def select_user(self, id, **kwargs) -> User:
        """
        This function selects a user from the database

        Args:
            id (int): The id of the user to be selected
            kwargs: The columns to be selected

        Returns:
            User: The user object with the selected columns

        Excepts:
            ValueError: If the user has no id
        """

        name = kwargs.get('name', False)
        ctt_time = kwargs.get('ctt_time', False)
        confirmation_flag = kwargs.get('confirmation_flag', False)

        columns = []
        if name: columns.append('name')
        if ctt_time: columns.append('ctt_time')
        if confirmation_flag: columns.append('confirmation_flag')
        if not columns:
            columns = ['name', 'ctt_time', 'confirmation_flag']

        select_columns = ", ".join(columns)

        if id is None:
            raise ValueError("User has no id")

        with self._conn as conn:
            with self.get_cursor(conn) as cursor:
                # Assuming id is of type character varying or text in your database,
                # we can cast the id to text for the comparison.
                cursor.execute(f"SELECT {select_columns} FROM iara.user WHERE id = '{str(id)}';")
                results = cursor.fetchall()

                if results:
                    user = User(id=id)
                    record = results[0]
                    for idx, col in enumerate(columns):
                        setattr(user, col, record[idx])
                    return user

        return None


    def get_datetime(self, id):
        with self._conn as conn:
            with self.get_cursor(conn) as cursor:
                cursor.execute("SELECT lmdt FROM iara.last_messages WHERE user_id = %s;", (str(id),))
                result = cursor.fetchone()
                if result is None:
                    return None
                return result[0]
            
    #TODO: UNIFICAR ESSAS FUNÇÕES
            
    def make_ailm(self, id, ailm):
        with self._conn as conn:
            with self.get_cursor(conn) as cursor:
                try:
                    cursor.execute("SELECT * FROM iara.last_messages WHERE user_id = %s;", [id])
                    if cursor.fetchone():
                        cursor.execute("UPDATE iara.last_messages SET ailm = %s WHERE user_id = %s;", (ailm, id))
                    else:
                        cursor.execute("INSERT INTO iara.last_messages (user_id, ailm) VALUES (%s, %s);", (id, ailm))
                except Exception as e:
                    print("An error occurred:", e)

    def make_lm(self, id, lm):
        with self._conn as conn:
            with self.get_cursor(conn) as cursor:
                try:
                    cursor.execute("SELECT * FROM iara.last_messages WHERE user_id = %s;", [id])
                    if cursor.fetchone():
                        cursor.execute("UPDATE iara.last_messages SET lm = %s WHERE user_id = %s;", (lm, id))
                    else:
                        cursor.execute("INSERT INTO iara.last_messages (user_id, lm) VALUES (%s, %s);", (id, lm))
                except Exception as e:
                    print("An error occurred:", e)

    def make_current_time(self, id):
        with self._conn as conn:
            with self.get_cursor(conn) as cursor:
                try:
                    cursor.execute("SELECT * FROM iara.last_messages WHERE user_id = %s;", [id])
                    if cursor.fetchone():
                        cursor.execute("UPDATE iara.last_messages SET lmdt = CURRENT_TIMESTAMP WHERE user_id = %s;", [id])
                    else:
                        cursor.execute("INSERT INTO iara.last_messages (user_id) VALUES (%s);", [id])
                except Exception as e:
                    print("An error occurred:", e)
    # FIM DA UNIFICAÇÃO

    def update_last_message(self, id, ailm=None, lm=None, update_time=False):
        with self._conn as conn:
            with self.get_cursor(conn) as cursor:
                try:
                    cursor.execute("SELECT * FROM iara.last_messages WHERE user_id = %s;", [id])
                    if cursor.fetchone():
                        if ailm is not None:
                            cursor.execute("UPDATE iara.last_messages SET ailm = %s WHERE user_id = %s;", (ailm, str(id)))
                        if lm is not None:
                            cursor.execute("UPDATE iara.last_messages SET lm = %s WHERE user_id = %s;", (lm, str(id)))
                        if update_time:
                            cursor.execute("UPDATE iara.last_messages SET lmdt = CURRENT_TIMESTAMP WHERE user_id = %s;", [str(id)])
                    else:
                        insert_query = "INSERT INTO iara.last_messages (user_id"
                        values = [id]
                        if ailm is not None:
                            insert_query += ", ailm"
                            values.append(ailm)
                        if lm is not None:
                            insert_query += ", lm"
                            values.append(lm)
                        insert_query += ") VALUES (%s"
                        insert_query += ", %s" * (len(values) - 1)
                        insert_query += ");"
                        cursor.execute(insert_query, values)
                except Exception as e:
                    print("An error occurred:", e)


    # Protótipo de unificação

        
    def select_datetime(self, id):
        with self._conn as conn:
            with self.get_cursor(conn) as cursor:
                cursor.execute("SELECT lmdt FROM iara.last_messages WHERE user_id = %s;", (str(id),))
                return cursor.fetchone()[0]


    def get_last_message(self, id):
        with self._conn as conn:
            with self.get_cursor(conn) as cursor:
                cursor.execute("SELECT lm, ailm FROM iara.last_messages WHERE user_id = %s;", (str(id),))
                result = cursor.fetchone()
                if result is None:
                    return ''
                lm, ailm = result
                if lm is None:
                    lm = ""
                if ailm is None:
                    ailm = ""
                return "user: " + lm + '\n' + "ai: " + ailm


    def get_last_message_and_bool(self, id):
        with self._conn as conn:
            with self.get_cursor(conn) as cursor:
                # Modify the SQL query to also select the offerbool column
                cursor.execute("SELECT lm, ailm FROM iara.last_messages WHERE user_id = %s;", (str(id),))
                result = cursor.fetchone()

                if result is None:
                    return None, None
                lm, ailm = result
                if lm is None:
                    lm = ""
                if ailm is None:
                    ailm = ""
                # Return the values as required
                last_message = "last_message user: " + lm + '\n' + "last_message ai: " + ailm
                return last_message


    def set_bool(self, id, bool):
        """Set offer bool"""
        bool = [bool]
        with self._conn as conn:
            with self.get_cursor(conn) as cursor:
                cursor.execute("UPDATE iara.user SET confirmation_flag = %s WHERE id = %s RETURNING id;", (bool, str(id)))
                result = cursor.fetchone()
                if result is None:
                    cursor.execute("INSERT INTO iara.user (id, confirmation_flag) VALUES (%s, %s);", (str(id), bool))
                    return False
                else:
                    return True

    def remove_last_message(self, id):
        try:
            with self._conn as conn:
                with self.get_cursor(conn) as cursor:
                    cursor.execute("DELETE * FROM iara.last_messages WHERE user_id = %s;", (str(id),))
                    return True
        except:
            return False

    def select_all_users(self):
        with self._conn as conn:
            with self.get_cursor(conn) as cursor:
                cursor.execute("SELECT * FROM iara.user;")
                return cursor.fetchall()


# Example usage:
# user_with_reservation = get_user_and_reservation(db, 123)
        
if __name__ == "__main__":
    db = DatabaseHandler()
    last_message = input("$: ")
    ailm = "galo doido"
    db.set_bool("010101", True)