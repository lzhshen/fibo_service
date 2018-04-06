#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import pytest
import subprocess
from application.cache import CacheMgr
from application.fibonacci import Fibonacci
import time

#sys.path.append(os.path.join(os.path.dirname(__file__), '../app'))
#sys.path.append('../app')

@pytest.fixture(scope="session", autouse=True)
def startmemcache(request):
    proc = subprocess.Popen("/usr/bin/memcached")
    request.addfinalizer(proc.kill)
    time.sleep(3)

@pytest.fixture(scope="function")
def cache_mgr(request):
    cache_mgr = CacheMgr()
    def teardown():
      cache_mgr.tearDown() 
    request.addfinalizer(teardown)

    return cache_mgr

def test_CacheMgr(cache_mgr):
  """ Test the get and set funcion """
  cache_mgr.set('key1', 'value1')
  val = cache_mgr.get('key1')
  assert val == 'value1'

  cache_mgr.set('key1', 'hello_world')
  val = cache_mgr.get('key1')
  assert val == 'hello_world'

  """ Test a key that is not the cache """
  val = cache_mgr.get('miss_key')
  assert val == None

def test_Fibonacci_get_number_from_cache(cache_mgr):
  """ Test the get_number function with valid parameter """
  cache_mgr.set(str(0), '0')
  cache_mgr.set(str(1), '1')
  cache_mgr.set(str(2), '1')
  cache_mgr.set(str(3), '2')
  cache_mgr.set(str(4), '3')
  cache_mgr.set(str(5), '5')
  cache_mgr.set(str(6), '8')

  fibo = Fibonacci(cache_mgr, 6)
  # generate the fibonacci number for the first time
  y = fibo.get_number(4)
  assert y == 3

  # get the fibonacci number from cache
  y = fibo.get_number(7)
  assert y == 13
