#xterm -e "python /opt/gcf2sac/gcf2sac-auto.py" &
#sleep 1s  
#xterm -e "python /opt/gcf2sac/gcf2sac-manual.py" &
#sleep 1s 
#xterm -e "watch ls -lR /home/ppalma/Desktop/COY2"

xterm -e watch ls -lR $(cat /opt/gcf2sac/gcf2sac.cfg  | grep watch | awk -F' = ' '{ print $2 }' | awk -F'gcf' '{print $1}') &
xterm -e /opt/gcf2sac/gcf2sac.py -b
