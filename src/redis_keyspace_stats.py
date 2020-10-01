import redis
import argparse

parser = argparse.ArgumentParser(description='Scan all keys in redis database, extracting stats for keyspaces based on a delimeter.')
parser.add_argument('-H', dest='host', action='store', type=str, help='Redis host for connection', default='localhost')
parser.add_argument('-P', dest='port', action='store', type=int, help='Redis port for connection', default=6379)
parser.add_argument('-D', dest='db', action='store', type=int, help='Redis database to use (default 0)', default=0)
parser.add_argument('-d', dest='delimiter', action='store', type=str, help='Keyspace delimeter used (default :)', default=':')
parser.add_argument('-s', dest='scan_count', action='store', type=int, help='Number of items per scan command cursor', default=500)
parser.add_argument('-t', dest='test', action='store_true', help='Performs a test run on first 10 matching keys.', default=False)
parser.add_argument('-m', dest='match', action='store', help='Match pattern to use for scaning keyspace, e.g. AH*', default='*')
args = parser.parse_args()

cache = redis.StrictRedis(host=args.host, port=args.port, db=args.db)

max_keys = 100000000  # 100M
if args.test:
    max_keys = 10

key_counts = dict()
mem_sum = dict()
key_item_counts = dict()
key_type = dict()
redis_mem_stats = cache.info(section='memory')
redis_key_count = cache.info(section='keyspace')

i = 0
bytes = 0
for key in cache.scan_iter(match=args.match, count=args.scan_count):
    key_str = key.decode()
    pipe = cache.pipeline()
    pipe.memory_usage(key_str)
    pipe.type(key_str)
    key_info = pipe.execute()

    if key_info[1].decode() == 'hash':
        key_len = cache.hlen(key_str)
    elif key_info[1].decode() == 'set':
        key_len = cache.scard(key_str)
    else:
        key_len = 1

    if args.test:
        print(key_str, ' type:', key_info[1].decode(), ' num_items:', key_len, ' num_bytes:', key_info[0])


    prefix = key_str.split(args.delimiter)[0]
    if prefix in key_counts:
        key_counts[prefix] += 1
        key_item_counts[prefix] += key_len
        mem_sum[prefix] += key_info[0]
    else:
        key_counts[prefix] = 1
        key_item_counts[prefix] = key_len
        mem_sum[prefix] = key_info[0]
        key_type[prefix] = key_info[1].decode()
    i += 1
    bytes += key_info[0]

    if i/10000 == 0:
        print("Gathered stats on {} keys...".format(i))

    if i > max_keys:
        print("Max keys reached, exiting.")
        break


print('')
print('Redis keyspace stats for: {}:{}<db{}>'.format(args.host, args.port, args.db))
print('-------')
print('Total Keys : ', i)
print('Total Bytes: ', bytes)
print('')
print('Server stats:')
print(' Keystats:', redis_key_count)
print(' Used Memory:', redis_mem_stats['used_memory'])
print(' Used Memory For Dataset:', redis_mem_stats['used_memory_dataset'])
print(' Used Memory For Dataset:', redis_mem_stats['used_memory_dataset_perc'])
print('------------')
print('Keyspace Stats:')
print('---------------')
print('{:<20}{:>10}{:>15}{:>25}{:>20}{:>20}{:>20}{:>20}'.format('Prefix', 'Type', 'NoKeys', 'TotalBytes', 'AvgBytesPerKey', 'TotalItems', 'AvgItemsPerKey', 'AvgBytesPerItem'))

for k in key_counts:
    if key_counts[k] > 0:
        avg_size = int(round(mem_sum[k]/key_counts[k]))
        avg_item_key = int(round(key_item_counts[k]/key_counts[k]))
        avg_item_size = int(round(mem_sum[k]/key_item_counts[k]))
    print('{:<20}{:>10}{:>15}{:>25}{:>20}{:>20}{:>20}{:>20}'.format(k, key_type[k], key_counts[k], mem_sum[k], avg_size, key_item_counts[k], avg_item_key,avg_item_size))
