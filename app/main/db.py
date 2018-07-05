
import psycopg2


class PostgresConnection(object):

    def __init__(self):
        self.connection = None

    def init_app(self, app):
        self.connection = psycopg2.connect(host="localhost", database="ride_my_way", user="postgres", password="")

        @app.teardown_appcontext
        def close_connection(response_or_exception):
            self.connection.close()
            return response_or_exception

    def get_cursor(self):
        if not self.connection:
            raise RuntimeError('Attempt to get_cursor on uninitialized connection')
        return self.connection.cursor()

    def commit(self):
        if not self.connection:
            raise RuntimeError('Attempt to get_cursor on uninitialized connection')
        self.connection.commit()

postgres_connection = PostgresConnection()
