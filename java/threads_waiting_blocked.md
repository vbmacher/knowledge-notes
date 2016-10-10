http://stackoverflow.com/questions/15680422/difference-between-wait-and-blocked-thread-states

# What is the difference between WAITING and BLOCKED state?

A thread goes to wait state once it calls wait() on an Object. This is called Waiting State. Once a thread reaches waiting state, it will need to wait till some other thread notify() or notifyAll() on the object.

Once this thread is notified, it will not be runnable. It might be that other threads are also notified(using notifyAll) or the first thread has not finished his work, so it is still blocked till it gets its chance. This is called Blocked State.

Once other threads have left and its this thread chance, it moves to Runnable state after that it is eligible pick up work based on JVM threading mechanism and moves to run state.

-----

In the BLOCKED state, a thread is about to enter a synchronized block, but there is another thread currently running inside a synchronized block on the same object. The first thread must then wait for the second thread to exit its block.

In the WAITING state, a thread is waiting for a signal from another thread. This happens typically by calling Object.wait(), or Thread.join(). The thread will then remain in this state until another thread calls Object.notify(), or dies.





