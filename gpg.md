If the following error appears:

    Inappropriate ioctl for device

during GPG sign, run this:


    export GPG_TTY=$(tty)

https://github.com/keybase/keybase-issues/issues/1712