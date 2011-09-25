#! /usr/bin/python

import pygtk
pygtk.require('2.0')
import gtk
import pynotify
import pyinotify
import signal,os,sys,string
import ConfigParser
from daemonize import daemonize
import gobject


config = ConfigParser.ConfigParser()
config.read('/opt/gcf2sac/fnd.cfg')

gobject.threads_init()

class Identity(pyinotify.ProcessEvent):
    def process_default(self, event):
	print event.name
	if pynotify.init("My Application Name"):
		n = pynotify.Notification("New File Added ", event.name)
		n.set_timeout(int(config.get('FOLDER','ntimeout')))
		n.set_urgency(pynotify.URGENCY_LOW)
		n.show()

def on_loop(notifier):
    s_inst = notifier.proc_fun().nested_pevent()

def signal_handler(signal, frame):
       	notifier.stop()


class FolderNotify:
	def __init__(self):
		self.statusIcon = gtk.StatusIcon()
    		self.statusIcon.set_from_stock(gtk.STOCK_GOTO_BOTTOM)
		self.statusIcon.set_visible(True)
		self.statusIcon.set_tooltip("Watching %s"%config.get('FOLDER','watch'))

		self.menu = gtk.Menu()
		
		self.menuItem = gtk.ImageMenuItem(gtk.STOCK_REFRESH)
    		self.menuItem.connect('activate', self.refresh_cb, self.statusIcon)
    		self.menu.append(self.menuItem)
    		
		self.menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
    		self.menuItem.connect('activate', self.quit_cb, self.statusIcon)
    		self.menu.append(self.menuItem)

    		self.statusIcon.connect('popup-menu', self.popup_menu_cb, self.menu)
    		self.statusIcon.set_visible(1)

		self.wm = pyinotify.WatchManager()
		self.notifier = pyinotify.ThreadedNotifier(self.wm, Identity())
		
		self.wm.add_watch(config.get('FOLDER','watch'),
					pyinotify.IN_CLOSE_WRITE,
					rec=True,auto_add=True)		

		self.notifier.start()
		gtk.gdk.threads_enter()
    		gtk.main()
		gtk.gdk.threads_leave()

  	def quit_cb(self, widget, data = None):
        	print "Exiting cb"
        	self.notifier.stop()
    		gtk.main_quit()

	def refresh_cb(self, widget, data = None):
		pass

 	def popup_menu_cb(self, widget, button, time, data = None):
    		if button == 3:
			if data:
				data.show_all()
				data.popup(None, None, gtk.status_icon_position_menu,
					3, time, self.statusIcon)

if __name__=="__main__":
	daemonize(config.get('DAEMON','stdin'),
                                        config.get('DAEMON','stdout'),
                                        config.get('DAEMON','stderr'))
	
	fn = FolderNotify()
