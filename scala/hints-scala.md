# Scala: postfix operations

`import scala.language.postfixOps`


# Scala: "1 second"

`import scala.concurrent.duration._`

# Scala: PartialFunction orElse

If partial function is not defined upon its argument, it implements `orElse` method, which
passes the argument to another partial function in this case.

# Scala: foldLeft, foldRight

/:   foldLeft
:\   foldRight

# Scala: Future.sequence - take OK results

Transform Seq[Future[T]] to Seq[Future[Try[T]]]. Then get the
Future.sequence of it and filter failed ones.

# Scala: sealed

- applies to: class, trait
- meaning: cannot be inherited from except the same source file

# String.toLowerCase

Always use locale! Prefer hardcoded one.
https://stackoverflow.com/questions/10336730/which-locale-should-i-specify-when-i-call-string-tolowercase

# Gradle import problems
  
If a class/something cannot be imported, refresh Gradle project. Last chance - clear gradle cache.

# How to refresh cache without blocking

- using: scaffeine
- requested behavior:
  - Always return something if there is something in the cache (never expire)
  - After each time period (e.g. a minute), refresh items asynchronously
     ===> result: will not ever block, just on the first load
  - When the first load is a failure, do not keep this failure during the refresh idle time, but try
    again upon new request immediately


  LoadingCache[..]
    .refreshAfterWrite(1 minute)
    .build(...)

  that's it!

# IntelliJ IDEA

- how to view opened source code in the project window?

  Right-click on the Project toolbar in the project window (top-left) -> Autoscroll from Source

# Akka: ? vs. !

? == ask
! == send one-way message

