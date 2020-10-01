# Redis-Keyspace-Stats

It's best practice to use


## Usage

```
$ python redis_keyspace_stats.py --help

optional arguments:
  -h, --help     show this help message and exit
  -d DELIMITER   Keyspace delimeter used  (default :)
  -H HOST        Redis host for connection
  -P PORT        Redis port for connection  
  -m MATCH       Match pattern to use for scaning keyspace
  -s SCAN_COUNT  Number of items per scan command cursor (default 5000)  
  -D DB          Redis database to use (default 0)
  -t             Performs a test run on first 10 keys.  
```




## Docker

To run the tool via docker you use the following:

```
docker run --rm redis-keyspace-stats:latest python redis_keyspace_stats.py --help
```

example:
```
docker run --rm redis-keyspace-stats:latest python redis_keyspace_stats.py -H host.docker.internal -P 36379 -t -m AH:*
```

*Note:* On Docker For Mac, you need to use the `host.docker.internal` hostname to access ports on the host machine.


### Build

To build the container use the following:
```
docker build -t redis-keyspace-stats .
```
