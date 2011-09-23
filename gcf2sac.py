#! /usr/bin/python

import pyinotify
import os,string
import ConfigParser
import datetime
import signal
import sys
from datetime import date
from ftplib import FTP
from time import gmtime, strftime

config = ConfigParser.ConfigParser()
config.read('/opt/gcf2sac/gcf2sac.cfg')
	


class Identity(pyinotify.ProcessEvent):
    def process_default(self, event):
	print event.name
	if event.name.split('.')[-1] == 'gcf' or event.name.split('.')[-1] == 'sac':
       # if event.name.split('.')[-1] == 'gcf':
                date = event.name.split('_')[0]
                hour = event.name.split('_')[1][:4]
                component = event.name.split('.')[0][-1]
                station = event.pathname.split('/')[-2].lower()
                output = '%s_%s%s%s'%(date,hour,station,component)
                input = event.pathname
                folder = 'C%s'%date
                dest = config.get('FOLDER','sacdest')+'/'+folder
		
		print ' date %s\n hour %s\n comp %s\n station %s\n output %s\n input %s\n folder %s\n dest %s'%(date,hour,component,station,output,input,folder,dest)
	        if event.name.split('.')[-1] == 'gcf':
                        fixedName = event.path+'/'+output+'.gcf'
                        os.rename(input,fixedName)
                        a = os.spawnlp(os.P_WAIT,'gcf2sac','gcf2sac',fixedName,'-o:'+dest)
		if event.name.split('.')[-1] == 'sac':	
                        if not os.path.exists(dest):
                                os.system('mkdir %s'%dest)
 #                       cmd = 'cp  -v %s %s'%(event.pathname,dest)
                        os.spawnlp(os.P_WAIT, 'mv', 'mv',event.pathname, dest)

wm = pyinotify.WatchManager()
notifier = pyinotify.ThreadedNotifier(wm, Identity())


def on_loop(notifier):
    s_inst = notifier.proc_fun().nested_pevent()

def signal_handler(signal, frame):
	print "Exiting"
	notifier.stop()
	sys.exit(0)

import time
def main():
	print "PID main :",os.getpid()
	print 'Loaded config file'
	signal.signal(signal.SIGINT, signal_handler)

	s = pyinotify.Stats()
	notifier.start()
	wm.add_watch(config.get('FOLDER','watch'), pyinotify.IN_CLOSE_WRITE, rec=True, auto_add=True)
	print 'watching %s'%config.get('FOLDER','watch')
	while(True):
		time.sleep(1)


import sys, os
def daemonize ():

        try: 
                pid = os.fork()
                if pid > 0:
                        print 'Parent ending'
                        sys.exit(0)   # Exit first parent.
		print "PID :",os.getpid()
        except OSError, e: 
                sys.stderr.write ("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror) )
                sys.exit(1)
	
	# Decouple from parent environment.
	os.chdir("/") 
	os.umask(0) 
	os.setsid() 

	# Do second fork.
	try: 
		pid = os.fork() 
		if pid > 0:
			sys.exit(0)   # Exit second parent.
		print "PID :",os.getpid()
	except OSError, e: 
		sys.stderr.write ("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror) )
		sys.exit(1)

import getopt
if __name__ == "__main__":
	
 	try:
        	opts, args = getopt.getopt(
				sys.argv[1:], "hd:t:b", ["help","date","time"],

				)
 	except getopt.error, msg:
        	print msg
        	print "for help use --help"
        	sys.exit(2)
	for o, a in opts:
        	if o in ("-h", "--help"):
            		print __doc__
            		sys.exit(0)
		elif o in ("-b","--background"):
			print "Running in background"
			daemonize()
			main()
		else:
			assert False, "Unhandled option"
 	main()

