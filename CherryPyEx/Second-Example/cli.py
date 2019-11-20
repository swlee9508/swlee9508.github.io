#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests

url = 'http://127.0.0.1:8080/file_upload'
files = {'ufile': open('saved.txt', 'rb')}

r = requests.post(url, files=files)

print(r)
print(r.text)
files.clear()