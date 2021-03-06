#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgi
import os
import time
import syslog
import re
import subprocess
import logger as log
import sendemail
import pickle
import config as conf
import fcntl

def save_data(data):
	if conf.DEBUG:
		print("%s/session.data" % conf.store_path)

	data_file=open("%s/session.data" % conf.store_path,"wb")
	if conf.DEBUG:
		print("DEBUG: try lock file for write")
	fcntl.flock(data_file.fileno(), fcntl.LOCK_EX)
	if conf.DEBUG:
		print("DEBUG: success lock file for write")
	if conf.DEBUG:
		print("DEBUG: data_file:", data_file)
		print("DEBUG: start sleep(10)")
		time.sleep(10)
		print("DEBUG: end sleep(10)")
	pickle.dump(data,data_file)
	data_file.close()

def load_data():
	tmp_data_file="%s/session.data" % conf.store_path
	data={}
	reset=False
	if os.path.exists(tmp_data_file):
		if conf.DEBUG:
			print("DEBUG: Загружаем файл промежуточных данных: '%s'" % tmp_data_file)
		data_file = open(tmp_data_file,'rb')
		if conf.DEBUG:
			print("DEBUG: try lock file for read")
		fcntl.flock(data_file.fileno(), fcntl.LOCK_EX)
		if conf.DEBUG:
			print("DEBUG: success lock file for write")
		data=pickle.load(data_file)
		data_file.close()
		if conf.DEBUG:
			print("DEBUG: Загрузили файл промежуточных данных: '%s'" % tmp_data_file)

		if not "date" in data:
			if conf.DEBUG:
				print("DEBUG: Битый файл сессии - сброс")
			reset=True
	else:
		if conf.DEBUG:
			print("DEBUG: Файл промежуточных данных не существует")
		reset=True
	if reset:
		if conf.DEBUG:
			print("DEBUG: Сброс промежуточных данных")
		data["date"]=time.strftime("%Y.%m.%d", time.localtime( time.time()))
		data["voit_descr"]=conf.voit_descr
		data["users"]={}

	return data


#============== main() ===================
#home_dir=os.path.expanduser("~/.time_logger")


# ========== main ==============
form = cgi.FieldStorage()

web_user_agent=os.getenv("HTTP_USER_AGENT")
web_user_addr=os.getenv("REMOTE_ADDR")
web_user_host=os.getenv("REMOTE_HOST")
web_user_name=os.getenv('AUTHENTICATE_SAMACCOUNTNAME')

print("""
<html>
<head>
<meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
<title>Результат выполнения</title>
</head>
<body>
""" )
try:
	voit = u"%s" % cgi.escape(form['voit'].value.decode('utf8'))
except:
	print("<h1>Вы НЕ ПРОГОЛОСОВАЛИ!</h1>")
	print("Необходимо выбрать хотя бы один вариант!")
	print("</body></html>")
	sys.exit(1)

voit_data=load_data()

if conf.DEBUG:
	print("web_user_name=%s" % web_user_name)
if web_user_name in voit_data["users"]:
	print("<h1>Ваше мнение учтено!</h1>")
	print("<p>Ранее Вы голосовали за: %s</p>" % voit_data["users"][web_user_name]["voit"].encode('utf8'))
	print("<p>Теперь Вы изменили свой выбор на: %s</p>" % voit.encode('utf8'))
	voit_data["users"][web_user_name]["voit"]=voit
	save_data(voit_data)
else:
	print("<h1>Ваше мнение учтено!</h1>")
	print("<p>Вы проголосовали за: %s</p>" % voit.encode('utf8'))
	voit_data["users"][web_user_name]={}
	voit_data["users"][web_user_name]["voit"]=voit
	save_data(voit_data)

print("</body></html>")

