
http://ask.xmodulo.com/disable-ipv6-linux.html

/etc/sysctl.conf
  # to disable IPv6 on all interfaces system wide
  net.ipv6.conf.all.disable_ipv6 = 1

  # to disable IPv6 on a specific interface (e.g., eth0, lo)
  net.ipv6.conf.lo.disable_ipv6 = 1
  net.ipv6.conf.eth0.disable_ipv6 = 1

then; sudo sysctl -p /etc/sysctl.conf

sudo vi /etc/ssh/sshd_config
  AddressFamily inet
