#!flask/bin/python
import psycopg2
import json as simplejson


# Queries Class
class dbQueries:
	def __init__(self):
		self.conn_string = "host='ec2-23-21-231-14.compute-1.amazonaws.com' dbname='d5o54rbsrkdid4' user='lyvemoibacnmbe' password='xxxx'"
		# print "Connecting to database\n	->%s" % (self.conn_string)
		self.conn = psycopg2.connect(self.conn_string)
		self.cursor = self.conn.cursor()
		# print "Connected!\n"
	
	def db_select(self, table):
		#~ self.cursor.execute("SELECT * FROM redditnew")
		self.cursor.execute("SELECT * FROM %s" % (table))
		# self.records = self.cursor.fetchall()
		# print 'query'
		# return self.records
		rows = self.cursor.fetchall()
		for row in rows:
			last_entry = row[1]
		return last_entry

	def db_insert(self, table, datas):
		self.datas = datas
		self.datas = simplejson.dumps(self.datas)
		# datasx = simplejson.dumps(datas)
		#~ self.cursor.execute("INSERT INTO redditnew (data) values (%s)", [self.datas])
		#~ self.cursor.execute("insert into %s (data) values (%s)", 
		#~ [table, simplejson.dumps({"datas": [{"feedSource": "redddiiitttnewwww", "feedProperties": "aadadad"}]})])
		# print datas
		self.cursor.execute("INSERT INTO %s (data) VALUES ('%s')" % (table, datas))
		self.conn.commit()
		
	def db_close(self):
		self.cursor.close()
		self.conn.close()
	
	def db_empty(self, table):
		self.cursor.execute("DELETE FROM %s" % (table))
		self.conn.commit()
		
	def db_getlastid(self, table):
		# self.cursor.execute("SELECT lastval() from %s" % (table))
		self.cursor.execute("SELECT lastval() from redditnew")
		self.records = self.cursor.lastrowid().fetchall()
		print 'lastid'
		return self.records

# EXAMPLE QUERIES
# b= {"datas": [{"feedSource": "redddiiitttnewwww", "feedProperties": "aadadad"}]}
# dbq = dbQueries()
# a = dbq.db_getlastid('reddit')
# print a
#~ dbq.db_empty('redditnew')
#~ dbq.db_insert("redditnew", b)
# a = dbq.db_select('reddit')
# print a 

# datas= {"datas": [{"feedSource": "redddiiitttnewwww", "feedProperties": "aadadad"}]}
# datas = {'datas': [{'date': '1426793021000.0'}]}
# datas_to_store = simplejson.dumps(datas)
# # print datas_to_store
# dbq = dbQueries()
# dbq.db_insert('reddit', datas_to_store)
# dbq.db_close()
# print 'reddit inserted'
