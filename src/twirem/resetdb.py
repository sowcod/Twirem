#-*- coding: utf-8 -*-

"""
Put file 'apikeys' on 'twirem' directory.
'apikeys' format
consumer key
consumer secret
"""

import os
import sys
import os.path

sys.path.append(os.path.abspath('..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'twirem.settings'

def clear_tables():
	from django.db import connection
	cursor = connection.cursor()
	cursor.execute('SHOW TABLES')
	for row in cursor:
		cursor.execute('DROP TABLE %s;' % row[0])

def syncdb():
	os.system('python manage.py syncdb')

def set_apikey():
	from twirem.main.models import ApiKeys

	apikeys = ApiKeys()

	with open('apikeys', 'r') as f:
		apikeys.ckey = f.readline().rstrip()
		apikeys.csecret = f.readline().rstrip()

	apikeys.save()

clear_tables()
syncdb()
set_apikey()

