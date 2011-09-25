xterm -e "watch ls /mnt/seismData/gcf -lR" & 
xterm -e "watch ls /mnt/seismData/sac -lR" &

xterm -e "tail -f $( cat /opt/gcf2sac/gcf2sac.cfg  | grep stdout | awk -F' = ' '{ print $2 }')" &
xterm -e "tail -f $( cat /opt/gcf2sac/gcf2sac.cfg  | grep sterr | awk -F' = ' '{ print $2 }')" &
