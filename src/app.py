#!/usr/bin/env python
# coding:utf-8

from flask import request
from flask import make_response
import socket
from flask import Flask, jsonify
import logging.config

#from os import path
#log_file_path = path.join(path.dirname(path.abspath(__file__)), '../config/logging.conf')
#logging.config.fileConfig(log_file_path)

app = Flask(__name__)

app.config.from_object('config')
logging.config.fileConfig(app.config.get('LOG_CONF'))
logger = logging.getLogger('App')


@app.route('/')
def hello_world():
    print('step1')
    return 'Hello World!'


@app.route('/index', methods=['POST', 'GET'])
def index():
    db=app.config.get('DB')
    #db = pymysql.connect("localhost", "mysqldb", "mysql", "mysqldb")
    cursor = db.cursor()
    print('step2:', db)
    if not request:
        return make_response(jsonify({'msg': 'request is null'}), 400)
        print('not request')
    try:
        keyid = request.values.get('key_id')
        print(type(keyid), keyid)

    except Exception as ex:
        return make_response(jsonify({'msg': 'request is null'}), 400)

    sql = "SELECT * FROM EMPLOYEE WHERE FIRST_NAME = '%s'" % (keyid)

    print('step3', sql)
    try:
        cursor.execute(sql)
        row = cursor.fetchone()
        print('step5', row)
        fname = row[0]
        lname = row[1]
        age = row[2]
        sex = row[3]
        income = row[4]
        print("fname=%s,lname=%s,age=%s,sex=%s,income=%s" % \
              (fname, lname, age, sex, income))
        db.commit()
    except:
        db.rollback()
        print('step5')

    return make_response(jsonify(
        {'errmsg': 'ok', 'keyid': keyid.strip(), 'fname': fname, 'lname': lname, 'age': age, 'income': income, }), 200)


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    app.run(host=ip, port=5003,debug = app.config.get("DEBUG"))
