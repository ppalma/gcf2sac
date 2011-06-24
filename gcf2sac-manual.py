
#!/usr/bin/python


# Example: prints statistics.
#
import pyinotify
import os,string
import ConfigParser
import datetime
from datetime import date
from ftplib import FTP

import glob
print 'Init'
config = ConfigParser.ConfigParser()
config.read('/opt/gcf2sac/gcf2sac.cfg')
print 'Config Loaded'

print 'Connecting'
ftp = FTP(
	config.get('FTP', 'address'),
	config.get('FTP', 'user'),
	config.get('FTP', 'passwd')
	)
ftp.cwd(config.get('FTP', 'folder'))
print 'Connected'

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

#print remoteTree
today = date.today()
# today.strftime('%Y%m%d')


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
#		os.spawnlp(os.P_WAIT,'wget','wget -q --protocol-directories'+output,link,'')#'-P %s'%output)	
	#	print('Walking on %s%s, Match %s'%(dir,d,link))
		#os.system('wget -qnc -P %s %s'%(output,link))
		cmd = 'wget -qnc -P %s %s'%(output,link)
		print cmd
		os.popen(cmd)
		

