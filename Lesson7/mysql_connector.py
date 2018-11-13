from mysql.connector import MySQLConnection, Error


class MySQLConnect:
    @staticmethod
    def connect():
        """
        :return: class DB connection or connection error
        """
        try:
            conn = MySQLConnection(
                host='127.0.0.1',
                database='lesson7',
                user='root',
            )
            return conn

        except Error as e:
            return e

    @staticmethod
    def select(query):
        """
        SELECT query
        :param query: string
        :return: dict by KEY or connection error
        """
        try:
            conn = MySQLConnect.connect()
            cursor = conn.cursor()
            cursor.execute(query)
            result = {}
            for row in cursor:
                result[row[0]] = row[1:]
            return result

        except Error as e:
            return e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def insert(query):
        """
        INSERT query
        :param query: string
        :return: error
        """
        try:
            connection = MySQLConnect.connect()
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

        except Error as error:
            return error

        finally:
            cursor.close()
            connection.close()


