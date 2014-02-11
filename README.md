# direhose

This util traverses POSIX compliant filesystems and generates a UDP data stream 
out of the discovered file and directory information. The name `direhose` is a 
portmanteau word, combining *directory* and *firehose*.

## Dependencies

* Python 2.6+
* POSIX compliant file system

## Usage

Download/clone the repo and place it somewhere, such as `~/direhose`. First you
want to edit `direhose.conf` to fit your needs and then you can run it as follows:

    $ python direhose.py [configuration file]

If you don't provide a config file, `direhose` will look for a `direhose.conf`
in the directory you're launching the script and if it doesn't find one there
it will revert to the following:

* default starting directory for the walk: the current directory
* default source type: send packages to stdout
* default source mode: send file/directory metadata only

## License

[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).


ToDo:

* network, data stream
* usage example