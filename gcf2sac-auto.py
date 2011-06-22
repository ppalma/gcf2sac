#!/usr/bin/env python


# Example: prints statistics.
#
import pyinotify
import os
import ConfigParser


#TODO: http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
class Identity(pyinotify.ProcessEvent):
    def process_default(self, event):
        # Does nothing, just to demonstrate how stuffs could trivially
        # be accomplished after having processed statistics.
	#print "%s  %s"%(event.pathname,event.name)
	date = event.name.split('_')[0] 
	hour = event.name.split('_')[1][:4]
	component = event.name.split('.')[0][-1] 
	station = event.pathname.split('/')[-2].lower()
	output = '%s_%s%s%s'%(date,hour,station,component)
	input = event.pathname
	folder = 'C%s'%date
	dest = config.get('FOLDER','detination')+'/'+folder
	
	if event.name.split('.')[-1] == 'gcf':
		fixedName = event.path+'/'+output+'.gcf'
		os.rename(input,fixedName)
		cmd = 'gcf2sac %s -o:%s'%(fixedName,dest)
		a = os.system(cmd)	
	else:
		if not os.path.exists(dest):
			os.system('mkdir %s'%dest)
		print dest
		cmd = 'cp  -v %s %s'%(event.pathname,dest)
		os.system(cmd)		
	#print 'Does nothing.'

def on_loop(notifier):
    # notifier.proc_fun() is Identity's instance
    s_inst = notifier.proc_fun().nested_pevent()
    #print repr(s_inst), '\n', s_inst, '\n'

def write_settings():
	
	config.add_section('FOLDER')
	config.set('FOLDER','detination','/home/user/COY2')
	config.set('FOLDER','watch','/home/user/ftpmirror')
	with open('gcf2sac-auto.cfg', 'wb') as configfile:
                config.write(configfile)

config = ConfigParser.ConfigParser()
config.read('gcf2sac-auto.cfg')
#write_settings()
wm = pyinotify.WatchManager()
s = pyinotify.Stats()
notifier = pyinotify.Notifier(wm, default_proc_fun=Identity(s), read_freq=5)
wm.add_watch(config.get('FOLDER','watch'), pyinotify.IN_CREATE, rec=True, auto_add=True)
notifier.loop(callback=on_loop)
