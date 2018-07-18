#coding=utf-8

import time
import hashlib
import pickle
 
# 用装饰器实现缓存
cache = {}

def is_obsolete(entry,duration):
    """判断是否过期"""
    d = time.time()-entry['time']
    return d>duration
   
def compute_key(function,args,kwargs):
    key = pickle.dumps((function.__name__,args,kwargs))
    return hashlib.sha1(key).hexdigest()
 
def memoize(duration=10):
    def _memorize(function):
        def __memorize(*args,**kwargs):
            key = compute_key(function,args,kwargs)
            # key存在且未过期
            if key in cache and not is_obsolete(cache[key],duration):
                print('we got a winner')
                return cache[key][ 'value']
           
            result = function(*args,**kwargs)
            cache[key] = { 'value':result, 'time':time.time()}
            return result
        return __memorize
    return _memorize

@memoize()
def complex(a,b):
    time.sleep(2)
    return a+b

complex(1,2)