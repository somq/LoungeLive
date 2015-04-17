#!flask/bin/python

import os
try: 
  import simplejson as json
except:
  import json
import requests
from flask import Flask
from flask import jsonify
from random import randint

app = Flask(__name__)

# Retrieve data from db
getFromdb()

@app.route("/")
def api():
    return jsonify(datas=hltvDatas)
	
if __name__ == '__main__':
    app.run()
    app.run(threaded=True)  
    
    
    
    