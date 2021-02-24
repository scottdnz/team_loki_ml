import sqlite3


def selectQuery(cursor):
	q = "SELECT id, item, value FROM config WHERE item = ?"
	params = ("data_dir",)
	rows = cursor.execute(q, params).fetchall()
	print(rows)


if __name__ == "__main__":
	connection = sqlite3.connect("C:/Users/scott.davies/Documents/ws/py/team_loki_ml/data/ml_loki.db")

	print(connection.total_changes)

	cursor = connection.cursor()

	q = """insert into config
	(item, 
	value) 
	values 
	(?, 
	?)""";

	params = ("data_dir", "C:/Users/scott.davies/Documents/VBoxShared/202102/hackathon_data_2021",)

	result = cursor.execute(q, params)
	connection.commit()
	print("cursor.lastrowid: " + str(cursor.lastrowid))

	selectQuery(cursor)

	q = "update config set value = ? where item = ?"
	params = ("updated", "data_dir")
	cursor.execute(q, params)
	connection.commit()

	selectQuery(cursor)

	q = "delete from config where id > 0"
	cursor.execute(q, ())
	connection.commit()

	cursor.close()

	connection.close()