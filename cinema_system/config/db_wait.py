import os
import time

import psycopg


for _ in range(30):
    try:
        with psycopg.connect(
            dbname=os.getenv('POSTGRES_DB', 'cinema_db'),
            user=os.getenv('POSTGRES_USER', 'cinema_user'),
            password=os.getenv('POSTGRES_PASSWORD', 'cinema_pass'),
            host=os.getenv('POSTGRES_HOST', 'db'),
            port=os.getenv('POSTGRES_PORT', '5432'),
        ):
            print('Database ready')
            break
    except Exception:
        print('Waiting for database...')
        time.sleep(2)
else:
    raise RuntimeError('Database is not available.')
