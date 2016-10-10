http://www.cs.columbia.edu/~hgs/rtp/faq.html
https://tools.ietf.org/html/rfc3550#section-5.3.1

The timestamp is used to place the incoming audio and video packets in the correct timing order
(playout delay compensation).

The sequence number is mainly used to detect losses. Sequence numbers increase by one for each
RTP packet transmitted, timestamps increase by the time "covered" by a packet. 

from RFC:
      The timestamp reflects the sampling instant of the first octet in
      the RTP data packet.  The sampling instant MUST be derived from a
      clock that increments monotonically and linearly in time to allow
      synchronization and jitter calculations (see Section 6.4.1).

for example:
  frequency = 8000Hz  (the linear clock)
  number_of_samples_in_previous_packet = this_timestamp - previous_timestamp

value:
  initial timestamp = random value
  next timestamp = initial timestamp + number of samples in the previous packet
  next next timestamp = previous timestamp + number of samples in the previous packet
  ...

for example:
  - packet with 20ms of audio sampled at 8kHz increases timestamp by 160
  - or 160 timestamp difference means 8000 Hz / 160 samples = 50 s^(-1) = 1/50 = 0.02s = 20ms
    or 160 / 8000 = 0.02s = 20ms
  - 20ms / 32 bytes = 0.625ms per byte
    


