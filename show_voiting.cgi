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
import sys
import fcntl

def load_data():
	tmp_data_file="%s/session.data" % conf.store_path
	data={}
	reset=False
	if os.path.exists(tmp_data_file):
		if conf.DEBUG:
			print("DEBUG: Загружаем файл промежуточных данных: '%s'" % tmp_data_file)
		try:
			data_file = open(tmp_data_file,'rb')
			if conf.DEBUG:
				print("DEBUG: try lock file for read")
		except:
		 	print("error open file")
		try:
			fcntl.flock(data_file.fileno(), fcntl.LOCK_EX)
			if conf.DEBUG:
				print("DEBUG: success lock file for read")
		except:
		 	print("error lock file")
		 	sys.exit(1)
		data=pickle.load(data_file)
		data_file.close()
		if conf.DEBUG:
			print("DEBUG: Загрузили файл промежуточных данных: '%s'" % tmp_data_file)

		if not "date" in data:
			if conf.DEBUG:
				print("DEBUG: Битый файл сессии - сброс")
			reset=True
		else:
			if data["date"] != time.strftime("%Y.%m.%d", time.localtime( time.time())):
				# Это файл не от сегодняшней сессии, сохраняем его в лог и сбрасываем:
				save_log(data)
				if conf.DEBUG:
					print("DEBUG: Это файл не от сегодняшней сессии, сохраняем его в лог и сбрасываем")
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

voit_data=load_data()

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
<title>Голосование</title>
</head>
<body>
""" )
# Подсчёт:
result={}
for user in voit_data["users"]:
	voit=voit_data["users"][user]["voit"]
	if voit in result:
		result[voit]+=1
	else:
		result[voit]=1
print("""
		<h1>Результаты голосования:</h1>
		<TABLE BORDER>
		<TR>    
				<TH COLSPAN=19>%(name)s</TH>
		</TR>
		<TR>
				<TH COLSPAN=1>№</TH>
				<TH COLSPAN=1>Вариант</TH>
				<TH COLSPAN=1>Количество проголосовавших</TH>
		</TR>
		""" % {"name":conf.voit_descr})
index=1
for var in result:
	print("""<TR>
		 <TD>%(index)d</TD>
		 <TD>%(var)s</TD>
		 <TD>%(num)d</TD>
		 </TR>""" % {\
		 "index":index, \
		 "var":var.encode('utf8'),\
		 "num":result[var]\
		 })
	index+=1
			
print("</TABLE>")
print("</body></html>")

