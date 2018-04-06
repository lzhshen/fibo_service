#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import pytest
from application.fibonacci import Fibonacci, ParamsError, CacheError
  
def test_get_number():
  """ Test the get_number function with valid parameter """
  fibo = Fibonacci()
  y = fibo.get_number(0)
  assert y == 0
  y = fibo.get_number(1)
  assert y == 1
  y = fibo.get_number(2)
  assert y == 1
  y = fibo.get_number(3)
  assert y == 2
  y = fibo.get_number(4)
  assert y == 3
  y = fibo.get_number(10)
  assert y ==55 

def test_get_number_invalid():
  """ Test the get_number function with invalid parameter """
  fibo = Fibonacci()
  with pytest.raises(ParamsError):
    y = fibo.get_number(-4)

def test_get_sequence_default():
  """ Test the get_sequence function with default 'offset' and 'limit' """
  fibo = Fibonacci()
  seq = fibo.get_sequence(0)
  assert seq == (0, )
  seq = fibo.get_sequence(1)
  assert seq == (0, 1)
  seq = fibo.get_sequence(2)
  assert seq == (0, 1, 1)
  seq = fibo.get_sequence(3)
  assert seq == (0, 1, 1, 2)
  seq = fibo.get_sequence(7)
  assert seq == (0, 1, 1, 2, 3, 5, 8, 13)

def test_get_sequence_with_offset():
  """ Test the get_sequence function with different 'offset' parameter """
  fibo = Fibonacci()
  seq = fibo.get_sequence(3, offset=0)
  assert seq == (0, 1, 1, 2)

  seq = fibo.get_sequence(3, offset=1)
  assert seq == (1, 1, 2)

  seq = fibo.get_sequence(3, offset=2)
  assert seq == (1, 2)

  seq = fibo.get_sequence(3, offset=3)
  assert seq == (2, )

  with pytest.raises(ParamsError):
    seq = fibo.get_sequence(3, offset=4)

  with pytest.raises(ParamsError):
    seq = fibo.get_sequence(3, offset=-1)

def test_get_sequence_with_limit():
  """ Test the get_sequence umber function with different 'limit' parameter """
  fibo = Fibonacci()

  seq = fibo.get_sequence(3, limit=1)
  assert seq == (0, )

  seq = fibo.get_sequence(3, limit=2)
  assert seq == (0, 1) 

  seq = fibo.get_sequence(3, limit=3)
  assert seq == (0, 1, 1) 

  seq = fibo.get_sequence(3, limit=4)
  assert seq == (0, 1, 1, 2) 

  seq = fibo.get_sequence(3, limit=5)
  assert seq == (0, 1, 1, 2) 

  with pytest.raises(ParamsError):
    seq = fibo.get_sequence(3, limit=0)

  with pytest.raises(ParamsError):
    seq = fibo.get_sequence(3, limit=-1)

def test_get_sequence_with_offset_and_limit():
  """ Test the get_sequence umber function with different 'offset' and 'limit' parameter """
  fibo = Fibonacci()

  seq = fibo.get_sequence(3, offset=0, limit=2)
  assert seq == (0, 1)

  seq = fibo.get_sequence(3, offset=1 , limit=2)
  assert seq == (1, 1) 

  seq = fibo.get_sequence(3, offset=2 , limit=2)
  assert seq == (1, 2) 

  seq = fibo.get_sequence(3, offset=3 , limit=2)
  assert seq == (2, ) 

  with pytest.raises(ParamsError):
    seq = fibo.get_sequence(3, offset=4 , limit=2)

def test_get_number_too_large():
  """ Test the get_number function with parameter larger than the max limit """
  # the max fibonacci number that we support is 8
  fibo = Fibonacci(max_fibo_layer=3) 
  y = fibo.get_number(8)
  assert y == 21
  with pytest.raises(ParamsError):
    y = fibo.get_number(9)

  # the max fibonacci number that we support is (math.pow(2, 10))
  fibo1 = Fibonacci() 
  y = fibo1.get_number(1024)
  assert y == 4506699633677819813104383235728886049367860596218604830803023149600030645708721396248792609141030396244873266580345011219530209367425581019871067646094200262285202346655868899711089246778413354004103631553925405243
  with pytest.raises(ParamsError):
    y = fibo.get_number(1025)

def test_get_number_with_cache():
  """ TODO: Test the get_number function with cache """
