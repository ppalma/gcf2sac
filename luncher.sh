xterm -e "python /opt/gcf2sac/gcf2sac-auto.py" &
sleep 1s  
xterm -e "python /opt/gcf2sac/gcf2sac-manual.py" &
sleep 1s 
xterm -e "watch ls -lR /home/ppalma/Desktop/COY2"
