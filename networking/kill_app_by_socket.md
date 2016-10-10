# How to "close" socket manually

The idea is to kill application which has the socket.

```
sudo netstat -ap | grep :PORT
```

The `PORT` is the "gate" to the socket and to the application.
The command will print PID which is needed to be killed.

Example:

```
[vbmacher@nb-jakubco ~]$ sudo netstat -ap | grep :46964
udp        0      0 nb-jakubco.office:46964 0.0.0.0:*                           9536/java           
[vbmacher@nb-jakubco ~]$ sudo kill -9 9536
```
