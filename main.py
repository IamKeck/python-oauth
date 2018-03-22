#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import lib
import os

AT = os.environ["AT"]
AS = os.environ["AS"]
CK = os.environ["CK"]
CS = os.environ["CS"]

URL = "https://api.twitter.com/1.1/statuses/home_timeline.json"
METHOD = "GET"

param = [("count", "5"), ("exclude_replies", "false")]

auth_base = lib.create_auth_base(CK, AT)
hmac_key = lib.create_hmac_key(CS, AS)
signature = lib.create_signature(False, URL, param, auth_base, hmac_key)
auth_header = lib.create_auth_header(auth_base, signature)

r = Request(URL + "?" + urlencode(param))
r.add_header("Authorization", auth_header)

with urlopen(r) as f:
    print(f.read())







