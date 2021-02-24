import sqlite3

class DBConnector:

	def __init__(self, dbLocation):
		"""
		"""
		self.connection = sqlite3.connect(dbLocation)
		self.cursor = self.connection.cursor()


	def insert(self, q, params):
		"""
		"""
		result = {"data": [], "errors": ""}
		try:
			self.cursor.execute(q, params)
			self.connection.commit()
			result["data"].append("success")
		except Exception as e:
			result["errors"] = str(e)
		return result


	def selectMany(self, q, params):
		"""
		"""
		result = {"data": [], "errors": ""}
		try:
			result["data"] = self.cursor.execute(q, params).fetchall()
		except Exception as e:
			result["errors"] = str(e)
		return result


	def update(self, q, params):
		"""
		"""
		result = {"data": [], "errors": ""}
		try:
			self.cursor.execute(q, params)
			self.connection.commit()
			result["data"].append("success")
		except Exception as e:
			result["errors"] = str(e)
		return result


	def delete(self, q, params):
		"""
		"""
		result = {"data": [], "errors": ""}
		try:
			self.cursor.execute(q, params)
			self.connection.commit()
			result["data"].append("success")
		except Exception as e:
			result["errors"] = str(e)
		return result





