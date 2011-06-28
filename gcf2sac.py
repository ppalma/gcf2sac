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
        if event.name.split('.')[-1] == 'gcf' or event.name.split('.')[-1] == 'sac':
                date = event.name.split('_')[0]
                hour = event.name.split('_')[1][:4]
                component = event.name.split('.')[0][-1]
                station = event.pathname.split('/')[-2].lower()
                output = '%s_%s%s%s'%(date,hour,station,component)
                input = event.pathname
                folder = 'C%s'%date
                dest = config.get('FOLDER','destination')+'/'+folder

	        if event.name.split('.')[-1] == 'gcf':
                        fixedName = event.path+'/'+output+'.gcf'
                        os.rename(input,fixedName)
                        cmd = 'gcf2sac %s -o:%s'%(fixedName,dest)
                        a = os.spawnlp(os.P_WAIT,'gcf2sac','gcf2sac',fixedName,'-o:'+dest)

                else:
                        if not os.path.exists(dest):
                                os.system('mkdir %s'%dest)
                        cmd = 'cp  -v %s %s'%(event.pathname,dest)
                        os.spawnlp(os.P_WAIT, 'cp', 'cp',event.pathname, dest)

wm = pyinotify.WatchManager()
notifier = pyinotify.ThreadedNotifier(wm, Identity())


def on_loop(notifier):
    s_inst = notifier.proc_fun().nested_pevent()

def signal_handler(signal, frame):
	notifier.stop()
	sys.exit(0)

def main(now=''):
	print 'Loaded config file'
	signal.signal(signal.SIGINT, signal_handler)

	s = pyinotify.Stats()
	notifier.start()
	wm.add_watch(config.get('FOLDER','watch'), pyinotify.IN_CLOSE_WRITE, rec=True, auto_add=True)
	print 'watching %s'%config.get('FOLDER','watch')

	print 'Connecting'
	ftp = FTP(
       		config.get('FTP', 'address'),
        	config.get('FTP', 'user'),
        	config.get('FTP', 'passwd')
        	)
	ftp.cwd(config.get('FTP', 'folder'))
	print 'Loading Remote Tree'
	x=[]
	ftp.dir('-d','*/',lambda L:x.append(L.split()[-1]))
	remoteTree ={}
	for dir in x:
	        ftp.cwd(dir)
	        y = []
	        ftp.dir('-d','*/',lambda L:y.append(L.split()[-1]))
	        remoteTree[dir]=y
	        ftp.cwd('..')
	today = date.today()
	for dir in remoteTree:
	        for d in remoteTree[dir]:
	                output = '%s/%s%s'%(config.get('FOLDER','location'),dir,d)
	                match = "%s*"%((now,today.strftime('%Y%m%d'))[now is ''])
	                filter = '-R *_%s*'%((strftime("%H", gmtime()),'')[now is ''])
	                link = 'ftp://%s:%s@%s/%s/%s%s%s'%(
	                        config.get('FTP', 'user'),
	                        config.get('FTP', 'passwd'),
	                        config.get('FTP', 'address'),
	                        config.get('FTP', 'folder'),
	                        dir,
	                        d,
	                        match
	                        )
			cmd = 'wget -qnc -P %s %s %s'%(output,link,filter)
	                print cmd
	                #print output
	                os.popen(cmd)
	notifier.stop()


import getopt
if __name__ == "__main__":
	
 	try:
        	opts, args = getopt.getopt(
				sys.argv[1:], "hd:t:", ["help","date","time"],

			#	 "d", ["date"]
				)
 	except getopt.error, msg:
        	print msg
        	print "for help use --help"
        	sys.exit(2)
    # process options
	now = ''
	for o, a in opts:
        	if o in ("-h", "--help"):
            		print __doc__
            		sys.exit(0)
		elif o in ("-d","--date"):
			now = a
		elif o in ("-t","--time"):
			print "time %s"%a
		else:
			assert False, "unhandled option"
    # process arguments
   # for arg in args:
    #    print arg
	main(now)




#main()
	
