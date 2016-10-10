http://www.cyberciti.biz/tips/linux-core-dumps.html

Don't forget to update also {{kernel.core_pattern}} in file {{/etc/sysctl.conf}},
because instead core dumps will be sent to automatic bug reporting tool.


http://stackoverflow.com/questions/2065912/core-dumped-but-core-file-is-not-in-current-directory

[/proc/sys/kernel/]core_pattern is used to specify a core dumpfile pattern name.

If the first character of the pattern is a '|', the kernel will treat the rest of the pattern
as a command to run. The core dump will be written to the standard input of that program instead
of to a file.

https://fedorahosted.org/abrt/wiki
https://github.com/abrt/abrt/wiki/ABRT-Project

