#! /usr/bin/python

import pyinotify
import os
import ConfigParser

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


config = ConfigParser.ConfigParser()
config.read('/opt/gcf2sac/gcf2sac.cfg')
wm = pyinotify.WatchManager()
s = pyinotify.Stats()
notifier = pyinotify.Notifier(wm, default_proc_fun=Identity(s), read_freq=5)
wm.add_watch(config.get('FOLDER','watch'), pyinotify.IN_CLOSE_WRITE, rec=True, auto_add=True)
print 'watching %s'%config.get('FOLDER','watch')
notifier.loop(callback=on_loop)



