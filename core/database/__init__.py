import os
import psycopg2.pool
from contextlib import contextmanager

from dotenv import load_dotenv
load_dotenv()


class Database:
    def __init__(self):
        self.pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST')
        )

    @contextmanager
    def get_connection(self):
        conn = self.pool.getconn()
        try:
            yield conn

        except Exception as e:
            print(f'[INIT.DB.ERROR] Yield error: {e}')

        finally:
            try:
                conn.commit()
                self.pool.putconn(conn)
                print('[INIT.DB.INFO] Commit successfully.') if os.getenv('DEBUG') else None

            except Exception as e:
                print(f'[INIT.DB.ERROR] Commit or putconn error: {e}')
