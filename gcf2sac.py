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

def on_loop(notifier):
    s_inst = notifier.proc_fun().nested_pevent()

def signal_handler(signal, frame):
	notifier.stop()
	sys.exit(0)


config = ConfigParser.ConfigParser()
config.read('/opt/gcf2sac/gcf2sac.cfg')
print 'Loaded config file'
signal.signal(signal.SIGINT, signal_handler)

wm = pyinotify.WatchManager()
s = pyinotify.Stats()
notifier = pyinotify.ThreadedNotifier(wm, Identity())
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
                match = today.strftime('%Y%m%d')+'*'
                link = 'ftp://%s:%s@%s%s/%s%s%s'%(
                        config.get('FTP', 'user'),
                        config.get('FTP', 'passwd'),
                        config.get('FTP', 'address'),
                        '/TramaDatos',#config.get('FTP', 'folder'),
                        dir,
                        d,
                        match
                        )
		cmd = 'wget -qnc -P %s %s -R *_%s*'%(output,link,strftime("%H", gmtime()))
                print cmd
                os.popen(cmd)

