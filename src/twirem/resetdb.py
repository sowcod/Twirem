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

from twirem.main.models import ApiKeys

apikeys = ApiKeys()

with open('apikeys', 'r') as f:
	apikeys.ckey = f.readline().rstrip()
	apikeys.csecret = f.readline().rstrip()

apikeys.save()
