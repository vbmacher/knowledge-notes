
# In the packet

tcp.reassembled.data[4:4] contains 00:00:00:05
tcp.segment_data contains 00:00:00:05


- [offset:length] can be used

BUT! Do not rely on correct positions, TCP stream can
be split into several packets.

# What to do

Dump whole TCP stream as raw file (one side only, do not mix requests/responses)
And parse it then, either with custom tool or some hex editor..

