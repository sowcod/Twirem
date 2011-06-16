#-*- coding: utf-8 -*-

"""
http://d.hatena.ne.jp/yoshifumi1975/20090516/p1
"""
import os
import sys
#import signal

import time
import logging
import logging.config

has_children = {}
PID_FILE='daemon.pid'

logging.config.fileConfig('log.conf')
logger = logging.getLogger('daemon')
os.environ['DJANGO_SETTINGS_MODULE'] = 'twirem.settings'

def main():
	daemonize()

	write_pid()

	#signal.signal(signal.SIGTERM, kill_all_children)

	while True:
		logger.debug('aaa')
		time.sleep(1)

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
