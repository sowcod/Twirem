#-*- coding: utf-8 -*-

"""
http://d.hatena.ne.jp/yoshifumi1975/20090516/p1
"""
import os
import sys
import time
#import signal

import logging
import logging.config
from twirem.crawler import ApiCrawler, DatabaseCrawler
from twirem.crawler import iconmanager

has_children = {}
PID_FILE='daemon.pid'

logging.config.fileConfig('log.conf')
logger = logging.getLogger('daemon')
os.environ['DJANGO_SETTINGS_MODULE'] = 'twirem.settings'
iconmanager.set_base_path('../icons')

def main():
	#daemonize()

	#write_pid()

	#signal.signal(signal.SIGTERM, kill_all_children)

	api_crawler = ApiCrawler(60)
	db_crawler = DatabaseCrawler(30)

	api_crawler.start()
	db_crawler.start()
	while True:
		time.sleep(10)

def write_pid():
	with open(PID_FILE, 'w') as f:
		f.write('%d' % os.getpid())

def daemonize():
	try:
		pid = os.fork()
		if pid > 0:
			sys.exit(0)
	
	except OSError, ex:
		raise Exception, "%s [%d]" % (ex.strerror, ex.errno)

	os.setsid()
	os.umask(0)
	#sys.stdin = open('
	sys.stdout = open('stdout.log', 'w')
	sys.stderr = open('stderr.log', 'w')

if __name__ == '__main__':
	main()
