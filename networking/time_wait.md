http://www.fromdual.com/huge-amount-of-time-wait-connections

http://vincent.bernat.im/en/blog/2014-tcp-time-wait-state-linux.html

http://serverfault.com/questions/329845/how-to-forcibly-close-a-socket-in-time-wait

http://benohead.com/tcp-about-fin_wait_2-time_wait-and-close_wait/


Time-wait and prerecording:
---------------------------

The sockets are in the state for some time (2 * maximum segment lifetime). The time can be obtained this way:

```
cat /proc/sys/net/ipv4/tcp_fin_timeout
```

which is usually 60 seconds.
The next test tries to connect to the same port, and if the socket is in TIME-WAIT state, it cannot be reused (if `SO_REUSEADDR` parameter is not enabled - which was not).

My solution is to directly use new ServerSocket(0) for the RMI registry - before each test (not before the class), and since the port 0 is forbidden, the kernel will immediately
find "free" port and assign it to the socket. So I have the guarantee of having always free port for the test. These sockets after finished test are often left in the `TIME_WAIT` state:

I have checked it during build using:

```
[root@builder51-32 ~]# ss -tan | grep TIME-WAIT | wc -l
172
```

but it does not matter much, since after 60 seconds they start to disappear. Maximum number connections can be obtained from:

```
[root@builder51-32 ~]# cat /proc/sys/net/ipv4/ip_local_port_range
32768   61000
```

which means (61000- 32768) = 28232 connections, it should be enough.
