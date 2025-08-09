import os
from functools import lru_cache

from .__init__ import Database

from dotenv import load_dotenv
load_dotenv()

db = Database()


def get_version() -> str:
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT VERSION()')

        response = cursor.fetchone()
        print(f'[DB.INFO] {response}')

        return str(response)


def get_user_id(username: str) -> int:
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT user_id FROM correspondence WHERE user_name = %s;""", (username,))

        return int(cursor.fetchone()[0])


def update_username(user_id: int, username: str) -> None:
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT user_name FROM correspondence WHERE user_id = %s;""", (user_id,))
        current_username = cursor.fetchone()[0]
        if current_username != username:
            cursor.execute("""UPDATE correspondence SET user_name = %s WHERE user_id = %s;""", (username, user_id))
            print(f'[DB.INFO] Username {current_username} changed to {username}.') if os.getenv('DEBUG') else None


def update_correspondence(user_id: int, message_text: str, message_date: str, is_admin: bool, username: str = 'NULL') -> None:
    is_admin = 'true' if is_admin else 'false'
    with db.get_connection() as conn:
        cursor = conn.cursor()
        if username != 'NULL':
            update_username(user_id, username)

        query = """INSERT INTO correspondence (user_id, user_name, correspondence)
VALUES (
	%s,  -- user_id
	%s,  -- username
	
	-- создаём json стркутуру
	jsonb_build_object(
		'messages', jsonb_build_array(
			jsonb_build_object(
				'is_admin', %s,
				'text', %s,
				'date', %s
			)
		),
		'meta', jsonb_build_object(
			'count', 1,
			'username', %s,
			'user_id', %s
		)
	)
)
-- Если такая есть, то делаем апдейт
ON CONFLICT (user_id) DO UPDATE 
SET correspondence = 
-- Внутри CASE-END прописываются условия WHEN (условаие) THEN (действие) ELSE
	CASE 
	-- Если json нет, то создаём его
		WHEN correspondence.correspondence IS NULL THEN
			jsonb_build_object(
				'messages', jsonb_build_array(
					jsonb_build_object(
						'is_admin', %s,
						'text', %s,
						'date', %s
					)
				),
				'meta', jsonb_build_object(
					'count', 1,
					'username', %s,
					'user_id', %s
				)
			)
	-- Если есть, то перезаписываем
		ELSE
			jsonb_set(
				jsonb_insert(
					correspondence.correspondence::jsonb,
					'{messages, -1}',
					jsonb_build_object(
						'is_admin', %s,
						'text', %s,
						'date', %s
					),
					true
				),
				'{meta, count}',
				to_jsonb((correspondence.correspondence::jsonb->'meta'->>'count')::int + 1)
			)
			-- берём значение из meta/count в виде int, прибавляем 1 и всё это в jsonb (при помощи to_jsonb)
	END
RETURNING correspondence;
"""
        params = (
            user_id, username,
            is_admin, message_text, message_date,
            username, user_id,
            # Для случая когда correspondence IS NULL
            is_admin, message_text, message_date,
            username, user_id,
            # Для основного случая
            is_admin, message_text, message_date
        )

        try:
            cursor.execute(query, params)
            get_names.cache_clear()
            print('[DB.INFO] Successfully correspondence update.') if os.getenv('DEBUG') else None
        except Exception as e:
            print(f'[DB.ERROR] Query error, {e}')


def add_admin(user_id: int, username: str, is_admin: bool = True) -> None:
    with db.get_connection() as conn:
        cursor = conn.cursor()
        if is_admin:
            cursor.execute('INSERT INTO admins (user_id, user_name) VALUES (%s, %s)', (user_id, username))
        else:
            print(f'[DB.ERROR] User {username}, {user_id} is not admin.')


def get_admins() -> list:
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM admins')

        return cursor.fetchall()


@lru_cache(maxsize=None)
def get_names() -> list:
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, user_name FROM correspondence")

        return cursor.fetchall()


def get_count() -> int:
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM correspondence")

        return int(cursor.fetchone()[0])


def get_correspondence(user_id: int, quantity: int or str = 30):
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT correspondence.correspondence FROM correspondence WHERE user_id=%s', (user_id,))

        json = cursor.fetchall()[0][0]
        if quantity == 'all':
            quantity = json['meta']['count']
        else:
            quantity = json['meta']['count'] if json['meta']['count'] < quantity else quantity

    for message in json['messages'][json['meta']['count']-quantity:]:
        is_admin = True if message['is_admin'] == 'true' else False
        yield message['text'], message['date'], is_admin
