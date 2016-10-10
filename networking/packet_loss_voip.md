https://en.wikipedia.org/wiki/Packet_loss_concealment

- for packet loss, PLC (packet loss concealment) technique can be used to mask its effects
- voip are UDP packets. they might not arrive, e.g. when server has full buffer and cannot
  accept more data

techniques:
  - zero insertion
  - waveform substitution: repeating a portion of already received speech
     ==> this is prolly used in decoder
  - model-based methods

