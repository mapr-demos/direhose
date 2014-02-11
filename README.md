# direhose

This util traverses POSIX compliant filesystems and generates a UDP data stream 
out of the discovered file and directory information. The name `direhose` is a 
portmanteau word, combining *directory* and *firehose*.

## Dependencies

* Python 2.6+
* POSIX compliant file system

## Usage

Download/clone the repo and place it somewhere, such as `~/direhose`. Then you
can run it as follows:

    $ python direhose.py

If you don't provide an input, `direhose` will traverse the filesystem starting
from the current directory in depth-first order.

## License

[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).