# direhose

This util traverses POSIX compliant filesystems and generates a data stream 
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

## Example sessions

The below examples assume that the configuration is set to `source_type=network`.

### Echo sink

In one terminal launch the echo sink like so:

    [~/Documents/repos/direhose/sinks] $ ./echo_sink.sh
    Listening on port 7654 for packages from direhose ...

Then, in a second terminal go:
      
    [~/Documents/repos/direhose] $ python direhose.py      

... and have a look at the first terminal again:

    [~/Documents/repos/direhose/sinks] $ ./echo_sink.sh
    Listening on port 7654 for packages from direhose ...
    {"package_ts": "2014-02-12T14:40:44.372021", "name": "/Users/mhausenblas2/Documents/repos/direhose", "last_modification": 1392188354.0, "size": 272}
    {"package_ts": "2014-02-12T14:40:44.372177", "name": "/Users/mhausenblas2/Documents/repos/direhose/.DS_Store", "last_modification": 1392215394.0, "size": 12292}
    {"package_ts": "2014-02-12T14:40:44.372272", "name": "/Users/mhausenblas2/Documents/repos/direhose/direhose.conf", "last_modification": 1392215382.0, "size": 1770}
    ...

### Modification time histogram sink

In one terminal launch the modification time histogram sink like so:

    [~/Documents/repos/direhose/sinks] $ python work_histo.py
    Listening for incoming data on port 7654
      
Then, in a second terminal go:
      
    [~/Documents/repos/direhose] $ python direhose.py      

... and have a look at the first terminal again:

    [~/Documents/repos/direhose/sinks] $ python work_histo.py
    Listening for incoming data on port 7654
    ............................................................................
    ............................................................................
    ......................................
    Data received, generating histogram ...
     0h: ******                                                                           (497)
     1h: **                                                                               (157)
     2h: *                                                                                (15)
     4h: *                                                                                (17)
     5h: **                                                                               (155)
     6h: *******                                                                          (568)
     7h: ******************************************************************************** (6020)
     8h: **                                                                               (216)
     9h: ***                                                                              (253)
    10h: ***********************************                                              (2640)
    11h: ***********************************************                                  (3563)
    12h: *******                                                                          (597)
    13h: ********************************************************************             (5182)
    14h: ********************                                                             (1545)
    15h: ***************************                                                      (2038)
    16h: *************                                                                    (983)
    17h: **********                                                                       (811)
    18h: *******                                                                          (530)
    19h: ****                                                                             (368)
    20h: ****************                                                                 (1256)
    21h: *                                                                                (108)
    22h: ***                                                                              (261)
    23h: *                                                                                (25)

In the output you see, for example that 5182 files or directories have been
modified in the hour starting at 13:00.

### Size distribution sink

TBD

### File extension table sink

TBD

## Configuration

The default config file [direhose.conf](direhose.conf) looks as follows:

    ############################################################################
    # The 'start_dir' setting defines from where direhose starts the walk.
    # It defaults to the current directory, that is, the directory from where
    # the script is launched.
    start_dir=.

    ############################################################################
    # The 'source_type' setting defines how package are sent by direhose.
    # You can choose between local or network delivery. Supported values are:
    #
    #  * local ... send packages to stdout
    #  * network ... send packages using UDP, where HOST:PORT can be specified,
    #                which defaults to 127.0.0.1:7654 if not specified.
    #
    # Examples:
    #
    #   source_type=local
    #
    #   source_type=network
    #   network_host=192.168.20.1
    #
    #   source_type=network
    #   network_host=192.168.20.1
    #   network_port=8001
    #
    source_type=network

    ############################################################################
    # The 'source_mode' setting defines what the package content is about.
    # You can choose between metadata-only, data-only or metadata & data combined. 
    # Supported values are:
    #
    #  * metadata ... send only file/directory metadata (name, size, etc.)
    #  * data     ... send only file data - TBD
    #  * metadata ... send first file/directory metadata and then the data - TBD
    #
    # Examples:
    #
    #   source_mode=metadata
    #
    #   source_mode=data
    #
    #   source_mode=metadata+data
    #
    source_mode=metadata


## License

[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).
