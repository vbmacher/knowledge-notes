# How to send a packet using UDP in Linux

```
echo -n "hello" | nc -4u --send-only HOST PORT
```

# How to receive a packet using UDP in Linux

- on localhost only

```
nc --recv-only -ul PORT
```



