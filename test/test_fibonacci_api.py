#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import pytest
from flask import json
import application.main

@pytest.fixture()
def app(request):
  return application.main.app.test_client()

def test_with_default(app):
  """ Test the fibonacci api with valid 'n' parameter and default 'offset' and 'limit' parameters """
  response = app.get('/api/fibonacci/0')
  data = json.loads(response.data)
  assert response.status_code == 200
  assert data[u'results']['data'] == [0]

  response = app.get('/api/fibonacci/1')
  data = json.loads(response.data)
  assert response.status_code == 200
  assert data[u'results']['data'] == [0, 1]

  response = app.get('/api/fibonacci/2')
  data = json.loads(response.data)
  assert response.status_code == 200
  assert data[u'results']['data'] == [0, 1, 1]

  response = app.get('/api/fibonacci/3')
  data = json.loads(response.data)
  assert response.status_code == 200
  assert data[u'results']['data'] == [0, 1, 1, 2]
  assert data[u'results']['links']['next'] == 'n/a'
  assert data[u'results']['pagination'] == {'limit': 100, 'offset': 0, 'total':4}

def test_with_valid_offset(app):
  """ Test the fibonacci api with valid 'offset' parameter """
  response = app.get('/api/fibonacci/3?offset=')
  data = json.loads(response.data)
  assert response.status_code == 200
  assert data[u'results']['data'] == [0, 1, 1, 2]

  response = app.get('/api/fibonacci/3?offset=0')
  data = json.loads(response.data)
  assert response.status_code == 200
  assert data[u'results']['data'] == [0, 1, 1, 2]

  response = app.get('/api/fibonacci/3?offset=1')
  data = json.loads(response.data)
  assert response.status_code == 200
  assert data[u'results']['data'] == [1, 1, 2]

  response = app.get('/api/fibonacci/3?offset=2')
  data = json.loads(response.data)
  assert response.status_code == 200
  assert data[u'results']['data'] == [1, 2]

  response = app.get('/api/fibonacci/3?offset=3')
  data = json.loads(response.data)
  assert response.status_code == 200
  assert data[u'results']['data'] == [2]

def test_with_valid_limit(app):
  """ Test the fibonacci api with valid 'limit' parameter """
  response = app.get('/api/fibonacci/3?limit=')
  data = json.loads(response.data)
  assert response.status_code == 200
  assert data[u'results']['data'] == [0, 1, 1, 2]

  response = app.get('/api/fibonacci/3?limit=1')
  data = json.loads(response.data)
  assert response.status_code == 200
  assert data[u'results']['data'] == [0]

  response = app.get('/api/fibonacci/3?limit=2')
  data = json.loads(response.data)
  assert response.status_code == 200
  assert data[u'results']['data'] == [0, 1]

  response = app.get('/api/fibonacci/3?limit=3')
  data = json.loads(response.data)
  assert response.status_code == 200
  assert data[u'results']['data'] == [0, 1, 1]

  response = app.get('/api/fibonacci/3?limit=4')
  data = json.loads(response.data)
  assert response.status_code == 200
  assert data[u'results']['data'] == [0, 1, 1, 2]

  response = app.get('/api/fibonacci/3?limit=5')
  data = json.loads(response.data)
  assert response.status_code == 200
  assert data[u'results']['data'] == [0, 1, 1, 2]

def test_with_valid_offset_and_limit(app):
  """ Test the fibonacci api with both valid 'offset' and valid 'limit' parameter """
  response = app.get('/api/fibonacci/3?offset=1&limit=1')
  data = json.loads(response.data)
  assert response.status_code == 200
  assert data[u'results']['data'] == [1]
  assert data[u'results']['links']['next'] == '/api/fibonacci/3?offset=2&limit=1'
  assert data[u'results']['pagination'] == {'limit': 1, 'offset': 1, 'total':4}


  response = app.get('/api/fibonacci/3?offset=2&limit=2')
  data = json.loads(response.data)
  assert response.status_code == 200
  assert data[u'results']['data'] == [1, 2]

  response = app.get('/api/fibonacci/3?offset=3&limit=3')
  data = json.loads(response.data)
  assert response.status_code == 200
  assert data[u'results']['data'] == [2]

def test_with_invalid_n(app):
  """ Test the fibonacci api with invalid 'n' parameter"""
  response = app.get('/api/fibonacci/abc')
  data = json.loads(response.data)
  assert response.status_code == 404
  data = json.loads(response.data)
  assert u'message' in data

  response = app.get('/api/fibonacci/-123')
  data = json.loads(response.data)
  assert response.status_code == 404
  data = json.loads(response.data)
  assert u'message' in data

def test_with_invalid_offset(app):
  """ Test the fibonacci api with invalid 'offset' parameter """
  response = app.get('/api/fibonacci/3?offset=-1')
  data = json.loads(response.data)
  assert response.status_code == 403
  assert u'message' in data

  response = app.get('/api/fibonacci/3?offset=4')
  data = json.loads(response.data)
  assert response.status_code == 403
  assert u'message' in data

  response = app.get('/api/fibonacci/3?offset=a')
  data = json.loads(response.data)
  assert response.status_code == 403
  assert u'message' in data

def test_with_invalid_limit(app):
  """ Test the fibonacci api with invalid 'limit' parameter """
  response = app.get('/api/fibonacci/3?limit=0')
  data = json.loads(response.data)
  assert response.status_code == 403
  assert u'message' in data

  response = app.get('/api/fibonacci/3?limit=-1')
  data = json.loads(response.data)
  assert response.status_code == 403
  assert u'message' in data

  response = app.get('/api/fibonacci/3?limit=a')
  data = json.loads(response.data)
  assert response.status_code == 403
  assert u'message' in data
