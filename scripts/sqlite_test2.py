from lib.DBConnector import DBConnector


if __name__ == "__main__":
	dbFileLocation = "C:/Users/scott.davies/Documents/ws/py/team_loki_ml/data/ml_loki.db"
	conn = DBConnector(dbFileLocation)

	# Insert query
	q = """insert into config
	(item, 
	value) 
	values 
	(?, 
	?)""";
	params = ("data_dir", "C:/Users/scott.davies/Documents/VBoxShared/202102/hackathon_data_2021",)
	result = conn.insert(q, params)
	print(result)


	# Select query
	q = "SELECT id, item, value FROM config WHERE item = ?"
	params = ("data_dir",)
	result = conn.selectMany(q, params)
	print(result)


	# Update query
	q = "update config set value = ? where item = ?"
	params = ("updated", "data_dir")
	result = conn.update(q, params)
	print(result)


	# Delete query
	q = "delete from config where id > ?"
	params = (0,)
	result = conn.delete(q, params)
	print(result)



