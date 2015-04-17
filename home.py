#!flask/bin/python

from flask import Flask
from flask import jsonify
from flask.ext import restful
from flask.ext.restful import reqparse
from flask import request
from dbqueries import *
from crossdomain import *

app = Flask(__name__)
#api = restful.Api(app)
#
#@app.route('/api', methods=['GET', 'POST'])    
#def testpoint():
	#a ={'hello': 'uxxser'}
	#name = request.args.get('name', '')
    #return jsonify(name = name)
	#return a

def get_datas_to_ret(feed_name):
	dbq = dbQueries()
	a = dbq.db_select(feed_name)
	# print a 
	dbq.db_close()
	return a

@app.route('/')
@crossdomain(origin='*')
def index():
	searchword = request.args.get('key', '')
	return searchword

@app.route('/api')
@crossdomain(origin='*')
def hello():
	feed = request.args.get('feed', '')

	if feed == 'reddit':
		try:
			a = get_datas_to_ret('reddit')
			return jsonify(a)
		except:
			return jsonify(response = '0')
	elif feed == 'hltv':
		try:
			a = get_datas_to_ret('hltv')
			return jsonify(a)
		except:
			return jsonify(response = '0')
	else:
		return jsonify(response = 'No can do :(')


@app.route('/<r>')
def whereuat(r):
    return "Where u at ? {} ? Where did you get that ? :(".format(r)




if __name__ == '__main__':
    app.run()
    app.run(threaded=True)  
    

