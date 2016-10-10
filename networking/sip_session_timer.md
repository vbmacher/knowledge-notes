# RFC 4028

session-timer belongs to a keep-alive mechanism for SIP sessions (RFC-4028).
The keep-alive mechanism works: UAs send periodic re-INVITE or UPDATE requests.
The interval for the requests is defined by negotiation mechanism.


# Headers:

Session-Expires - duration of the session
Min-SE          - minimal allowed value for session expiration
422 response code: session duration was too small

The purpose of Min-SE header field is to prevent hostile proxies from setting 
arbitrarily short refresh intervals so that their neighbors are overloaded.


After several INVITE/422 iterations, the request eventually arrives
   at the UAS.  The UAS can adjust the value of the session interval as
   if it were a proxy; when done, it places the final session interval
   into the Session-Expires header field in a 2xx response.


Session-Expires header field also contains a 'refresher' parameter,
   which indicates who is doing the refreshing -- the UA that is
   currently the UAC, or the UA that is currently the UAS.
Proxies on the path then can't change it hence.

From the Session-Expires header field in the response, both UAs know
   that a session timer is active, when it will expire, and who is
   refreshing.

The refresh requests sent once the session is established are
   processed identically to the initial requests, as described above.
   This means that a successful session refresh request will extend the
   session, as desired.

