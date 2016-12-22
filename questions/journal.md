Journaling filesystems (such as Ext3 or ReiserFS) are now being used by default by most Linux distributions.
No secure deletion program that does filesystem-level calls can sanitize files on such filesystems, because
sensitive data and metadata can be written to the journal, which cannot be readily accessed. Per-file secure
deletion is better implemented in the operating system.


