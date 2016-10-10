https://www.freedesktop.org/software/systemd/man/systemd.unit.html


https://fedoramagazine.org/systemd-converting-sysvinit-scripts/



After : declares ordering (will not cause running them!), and describes that the services listed here should run first, (this unit will run *after* them).
Wants : declares which services should be run before this unit. If they fail, never mind.

KillMode : sets how systemd will stop the service. 
   - control-group: all remaining processes in the control group of this unit will be killed on unit stop
   - process      : only the main process itself is killed
   - mixed        : the SIGTERM signal (see below) is sent to the main process while the subsequent SIGKILL signal (see below) is sent to all remaining processes of the unit's control group
   - none         : no process is killed

Restart : determines how systemd manages the service if it stops unexpectedly. 
          (Configures whether the service shall be restarted when the service process exits, is killed, or a timeout is reached.)
          (When the death of the process is a result of systemd operation (e.g. service stop or restart), the service will not be restarted.)
          (Timeouts include missing the watchdog "keep-alive ping" deadline and a service start, reload, and stop operation timeouts.)

    https://www.freedesktop.org/software/systemd/man/systemd.service.html#Restart=

   - no          : 
   - on-success  : Clean exit code or signal
   - on-failure  : Unclean exit code, Timeout, Watchdog
   - on-abnormal : Unclean signal, Timeout, Watchdog
   - on-watchdog : Watchdog
   - on-abort    : Unclean signal
   - always      : Clean exit code or signal, Unclean exit code, Unclean signal, Timeout, Watchdog


[Service]
TimeoutStartSec=0
Restart=always
ExecStartPre=-/usr/bin/docker stop %n
ExecStartPre=-/usr/bin/docker rm %n
ExecStartPre=/usr/bin/docker pull redis
ExecStart=/usr/bin/docker run --rm --name %n redis

- The "-" at the start means systemd won’t abort if the command fails.
  -  can be put also on environment files

