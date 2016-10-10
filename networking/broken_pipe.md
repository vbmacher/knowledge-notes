# what causes the broken pipe error?

- reason: peer side closed the socket but we sent data to it
- it takes time (2 minutes by default) to detect that the socked was closed
- if we send small amount of data (MTU) they will be cached and we don't need to get this error

http://stackoverflow.com/questions/4584904/what-causes-the-broken-pipe-error