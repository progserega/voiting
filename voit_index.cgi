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



#============== main() ===================
#home_dir=os.path.expanduser("~/.time_logger")
home_dir="/tmp/votes.data"

print ("""
<html>
<HEAD>
<META HTTP-EQUIV="CONTENT-TYPE" CONTENT="text/html; charset=utf-8">
<TITLE>Ваше мнение</TITLE>
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

<body><h1>Ваше мнение</h1>
""")
print("""
<form method=POST action="voit.cgi">
<div align="left">
<P><B>%s</B><br>
		""" % conf.voit_descr)

for variant_name in conf.voit_names:
	print ("""
<input type="radio" name="voit" value="%(variant_name)s">%(variant_name)s<br>
""" % {"variant_name":variant_name} )
print ("""
</div>

<P><input type=submit value="Голосовать">
</form>

<p>Посмотреть текущий результат высказанных мнений можно по ссылке:
<a target="_self" 
href="show_voiting.cgi"
>
ссылке
</a>.
</p>


</body></html>

		""")

