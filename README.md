# Client

this is the client part of project, implemented by python

### Quick Start

Make sure you have python on your machine.

The client is started by  `python client.py` COMMAND.

Use `python client.py -h` to see the help.

```
$ python client.py -h
usage: client.py [-h] [-m MODE] [-s SERVER] [-f FPS] [-e ENCODERATE]

optional arguments:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  mode: run(with arm) or debug(without arm)
  -s SERVER, --server SERVER
                        server url
  -f FPS, --fps FPS     expected fps
  -e ENCODERATE, --encodeRate ENCODERATE
                        encoding rate(0-100, 100 for best)
```

### To run client

- Debug mode (without arm)

  ```
  python client.py -m debug
  ```

- Run mode

  ```
  python client.py -s "<your server ip>" -f 10 -e 20
  ```

### To start the production line

Make sure you link the USB of the production line. Then use:

```
python CenterController.py 1      # 1 to start, 0 to close
```

> Note: you might need to run serval times