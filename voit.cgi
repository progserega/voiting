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

print ("""
<html>
<HEAD>
<META HTTP-EQUIV="CONTENT-TYPE" CONTENT="text/html; charset=utf-8">
<TITLE>Голосование</TITLE>
<META NAME="GENERATOR" CONTENT="OpenOffice.org 3.1  (Linux)">
<META NAME="AUTHOR" CONTENT="Сергей Семёнов">
<META NAME="CREATED" CONTENT="20100319;10431100">
<META NAME="CHANGEDBY" CONTENT="Сергей Семёнов">
<META NAME="CHANGED" CONTENT="20100319;10441400">
<STYLE TYPE="text/css">
<!--
@page { size: 21cm 29.7cm; margin: 2cm }
P { margin-bottom: 0.21cm }
-->
</STYLE>

<style>
.normaltext {
}
</style>
<style>
.ele_null {
color: red; /* Красный цвет выделения */
}
</style>
<style>
.selected_node {
color: green; /* Зелёный цвет выделения */
background: #D9FFAD;
font-size: 150%;
}
</style>

</HEAD>

<body><h1>Добавление нового пользователя в домен</h1>

<form method=POST action="voit.cgi">
<P><B>Фамилия:</B>
<P><input type=text name=user_familia>

<P><B>Имя:</B>
<P><input type=text name=user_name>

<P><B>Отчество:</B>
<P><input type=text name=user_otchestvo>

<P><B>Описание (отдел, район. Например: '(ШРЭС) инженер 2-й категории'):</B>
<P><input type=text name=user_description>

		""")

