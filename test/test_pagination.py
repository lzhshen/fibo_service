#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import pytest
from application.pagination import RespData

url_prefix = 'http://localhost/api/fibonacci'
  
def test_data_no_next_link():
  """ no next link """
  resp_data = RespData(n=5, offset=0, limit=100, fibo_seq=[0, 1, 1, 2, 3], url_prefix=url_prefix)
  data = resp_data.data()
  assert data['links']['next'] == 'n/a'
  assert data['pagination'] == {'limit': 100, 'offset': 0, 'total': 6} 
  assert data['data'] == [0, 1, 1, 2, 3]

def test_data_no_next_link():
  """ next link is available """
  resp_data = RespData(n=5, offset=0, limit=3, fibo_seq=[0, 1, 1, 2, 3], url_prefix=url_prefix)
  data = resp_data.data()
  next_url = "%s/%d?offset=%d&limit=%d" % (url_prefix, 5, 3, 3)
  assert data['links']['next'] == next_url 
  assert data['pagination'] == {'limit': 3, 'offset': 0, 'total': 6} 
  assert data['data'] == [0, 1, 1, 2, 3]
