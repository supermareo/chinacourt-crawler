# coding=utf-8
import redis

# 实现一个连接池
pool = redis.ConnectionPool(host='127.0.0.1', password='root')


def set(k, v):
    r = redis.Redis(connection_pool=pool)
    r.set(k, v)


def get(k):
    r = redis.Redis(connection_pool=pool)
    return r.keys(k + '*')


if __name__ == '__main__':
    l = get('一')
    for i in l:
        print(i.decode())
