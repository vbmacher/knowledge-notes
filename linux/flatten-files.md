Files in the form:

    xx..xx/1/[..file..]
    yy..yy/2/[..file..]

we want to flatten them into something like:

    xx..xx_8080_[..file..]
    yy..yy_x86_[..file..]


It can be possible in one line in Linux:
 
      find ./*/1 -mindepth 1 -type f -print | sed "s^\./\(.*\)^\0 \1^" | sed  "s, \(.*\)/1/,\n\./\1_8080_," | parallel -N 2 mv


---------------

Or - files in format:

    xx..xx/...any depth../[file].java 

to format:

    xx..xx/[file].java


    find . -mindepth 1 -type f -print | sed -e "s^\./\([^/]*/\).*/\([^/]*java\)^\0\n./\1\2^" | parallel -N 2 xargs mv
