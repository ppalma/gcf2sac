#!/usr/bin/env python


# Example: prints statistics.
#
import pyinotify
import os
import ConfigParser
class Identity(pyinotify.ProcessEvent):
    def process_default(self, event):
        # Does nothing, just to demonstrate how stuffs could trivially
        # be accomplished after having processed statistics.
	#print "%s  %s"%(event.pathname,event.name)
	date = event.name.split('_')[0] 
	hour = event.name.split('_')[1][:4]
	component = event.name.split('.')[0][-1] 
	station = event.pathname.split('/')[-2].lower()
	output = '%s_%s%s%s.sac'%(date,hour,station,component)
	input = event.pathname
	folder = 'C%s'%date
	cmd = 'gcf2sac %s %s -o:%s/%s'%(input,output,config.get('FOLDER','detination'),folder)
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
