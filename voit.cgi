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



def save_data(data):
	global home_dir
	if DEBUG:
		print("%s/session.data" % home_dir)

	data_file=open("%s/session.data" % home_dir,"wb")
	if DEBUG:
		print("DEBUG: data_file:", data_file)
	pickle.dump(data,data_file)
	data_file.close()

def load_data():
	tmp_data_file="%s/session.data" % home_dir
	data={}
	reset=False
	if os.path.exists(tmp_data_file):
		if DEBUG:
			print("DEBUG: Загружаем файл промежуточных данных: '%s'" % tmp_data_file)
		data_file = open(tmp_data_file,'rb')
		data=pickle.load(data_file)
		data_file.close()
		if DEBUG:
			print("DEBUG: Загрузили файл промежуточных данных: '%s'" % tmp_data_file)

		if not "date" in data:
			if DEBUG:
				print("DEBUG: Битый файл сессии - сброс")
			reset=True
		else:
			if data["date"] != time.strftime("%Y.%m.%d", time.localtime( time.time())):
				# Это файл не от сегодняшней сессии, сохраняем его в лог и сбрасываем:
				save_log(data)
				if DEBUG:
					print("DEBUG: Это файл не от сегодняшней сессии, сохраняем его в лог и сбрасываем")
				reset=True
	else:
		if DEBUG:
			print("DEBUG: Файл промежуточных данных не существует")
		reset=True
	if reset:
		if DEBUG:
			print("DEBUG: Сброс промежуточных данных")
		data["date"]=time.strftime("%Y.%m.%d", time.localtime( time.time()))
		data["log"]=[]
		data["stat"]={}
		data["result"]={}

	return data


#============== main() ===================
#home_dir=os.path.expanduser("~/.time_logger")
home_dir="/tmp/votes.data"


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
voit = u"%s" % cgi.escape(form['voit'].value.decode('utf8'))

print("<p>Вы проголосовали за: %s</p>" % voit.encode('utf8'))

print("Необходимо заполнить все поля")
print("</body></html>")

