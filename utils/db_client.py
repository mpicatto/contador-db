import psycopg2

class DBConnectionAdapter:
    def __init__(self):
        self.connection = None
        self.db_config = {
            "dbname": "aettaazd",
            "user": "aettaazd",
            "host": "lallah.db.elephantsql.com",
            "password": "GVm0q1OiOKCKUvs6AZfqx5QxagPw218F",
        }

    def __enter__(self):
        if self.connection is None:
            try:
                self.connection = psycopg2.connect(**self.db_config)
            except psycopg2.DatabaseError as e:
                raise e
        return self.connection

    def __exit__(self, *args, **kwargs):
        self.connection.close()