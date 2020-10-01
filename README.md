# Redis-Keyspace-Stats

Using a good naming convention for your Redis keys is one of the most important design decisions you will make on any project
using Redis as a datastore for a large number of users.  Adding a keyspace at the start of your key names should be the first
item in that naming convention, e.g.  `key_space1::key_space2::etc`.    

It's very easy for keys to get out of control in Redis and start filling expensive ElasticCache clusters. Finding out which keys are causing the issue when you have millions in a database is not so easy, that is where this tool comes in. *Redis-Keyspace-Stats* allows you to get a breakdown of your key set by the keyspaces you have chosen. Running the following command:

```
python redis_keyspace_stats.py -H my-prod-redis.ohhhh.ng.0001.apse1.cache.amazonaws.com -d ::
```  

will give you something like:

```
Redis keyspace stats for: my-prod-redis.ohhhh.ng.0001.apse1.cache.amazonaws.com:6379<db0>
-------
Total Keys :  1556703
Total Bytes:  590423255

Server stats:
 Keystats: {'db0': {'keys': 1556703, 'expires': 683006, 'avg_ttl': 44915532}, 'db1': {'keys': 849224, 'expires': 849223, 'avg_ttl': 1922989590}}
 Used Memory: 809767312
 Used Memory For Dataset: 631003472
 Used Memory For Dataset: 78.34%
------------
Keyspace Stats:
-------
Prefix            Type      NoKeys       TotalBytes      AvgBytesPerKey         TotalItems     AvgItemsPerKey     AvgBytesPerItem
ID                set       701513        221521615                 316             701513                  1                 316
AH                hash          49        238868461             4874867            2565950              52366                  93
rw-check          str            1              559                 559                  1                  1                 559
OW                set       855140        130032620                 152           11984795                 14                  11
```

now it's very clear to see where all my data is being used up. I also now have some stats about the type and average size for keys and items in sets and hashes, useful information for sizing calculations based on user base projections.


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
