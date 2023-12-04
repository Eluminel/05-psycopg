import psycopg2

class DbManager:
	def __init__(self, db_name, db_user):
		self.conn = psycopg2.connect(database=db_name, user=db_user)

	def create_tables(self):
		with self.conn.cursor() as cur:
			cur.execute("""
				CREATE TABLE IF NOT EXISTS users(
					id SERIAL PRIMARY KEY,
					name VARCHAR(40) NOT NULL, 
					surname VARCHAR(40) NOT NULL,
					email VARCHAR(40) NOT NULL
				);
				CREATE TABLE IF NOT EXISTS phone_numbers(
					id SERIAL PRIMARY KEY,
					phone_number VARCHAR(40),
					user_id INTEGER not null references users(id)
				);
			""")
		self.conn.commit()


	def create_user(self, name, surname, email):
		with self.conn.cursor() as cur:
			cur.execute("""
				INSERT INTO users(name, surname, email)
				VALUES
				(%s, %s, %s);
			""",(name, surname, email))
		self.conn.commit()


	def add_phone_number_to_user(self, user_id, phone_number):
		with self.conn.cursor() as cur:
			cur.execute(f"""
				INSERT INTO phone_numbers(phone_number, user_id)
				VALUES
				(%s, %s)
			""", (phone_number, user_id))
		self.conn.commit()

	def update_user(self, id, name=None, surname=None, email=None):
		if id is None:
			return
		sql_str = "UPDATE users SET"
		params = []
		if name is not None:
			params.append(f"name = '{name}'")
		if surname is not None:
			params.append(f"surname = '{surname}'")
		if email is not None:
			params.append(f"email = '{email}'")
		sql_query = sql_str + " " + ",".join(params) + f" WHERE id = {id};"

		with self.conn.cursor() as cur:
			cur.execute(sql_query)
		self.conn.commit()

	def delete_user(self, id):
		sql_query = f"DELETE FROM users WHERE id = {id};"

		with self.conn.cursor() as cur:
			cur.execute(sql_query)
		self.conn.commit()

	def delete_phone_by_user_id(self, id):
		sql_query = f"DELETE FROM phone_numbers WHERE user_id = {id}"

		with self.conn.cursor() as cur:
			cur.execute(sql_query)
		self.conn.commit()


	def find_user(self, name=None, surname=None, email=None):
		sql_str = "SELECT * FROM users WHERE"
		params = []
		if name is not None:
			params.append(f"name = '{name}'")
		if surname is not None:
			params.append(f"surname = '{surname}'")
		if email is not None:
			params.append(f"email = '{email}'")
		sql_query = sql_str + " " + ",".join(params) + ";"

		with self.conn.cursor() as cur:
			cur.execute(sql_query)
			result = cur.fetchall()
		self.conn.commit()
		return result

db = DbManager("personal_information_db","postgres")

# db.create_tables()
# db.create_user("Otto","Kornainen","cgafsdfdg@gdfg.ch")
# db.add_phone_number_to_user("1","78975")
# db.update_user(2, name="Victor")
# print(db.find_user(name="Victor"))
# db.delete_user(4)
# db.delete_phone_by_user_id(1)
db.conn.close()
