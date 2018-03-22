# -*- coding: utf-8 -*-
import hashlib
import random
from datetime import datetime
from urllib.parse import quote
from base64 import b64encode
import hmac
from hashlib import sha1


def _my_quote(string):
    return quote(string, safe="")


def create_auth_base(consumer, token, nonce=None, timestamp=None):
    nonce_val = nonce or hashlib.md5(str(random.random()).encode("ascii")).hexdigest()
    timestamp_val = timestamp or str(datetime.now().timestamp()).split(".")[0]
    return [
        ("oauth_consumer_key", consumer),
        ("oauth_nonce", nonce_val),
        ("oauth_signature_method", "HMAC-SHA1"),
        ("oauth_timestamp", timestamp_val),
        ("oauth_token", token),
        ("oauth_version", "1.0")
    ]


def create_hmac_key(consumer_secret, access_secret):
    return quote(consumer_secret) + "&" + quote(access_secret)


def create_signature(is_method_post, url, param, auth_base, hmac_key):
    auth_param = param + auth_base
    quoted_param = [(_my_quote(k), _my_quote(v)) for k, v in auth_param]
    sorted_param = sorted(quoted_param, key=lambda t: t[0])
    auth_str = "&".join([k + "=" + v for k, v in sorted_param])

    method = "POST" if is_method_post else "GET"

    auth_base = method + "&" + _my_quote(url) + "&" + quote(auth_str)
    return b64encode(hmac.new(hmac_key.encode("ascii"), auth_base.encode("ascii"), digestmod=sha1).digest()).decode()


def create_auth_header(auth_base, signature):
    auth_base_sorted = sorted(auth_base + [("oauth_signature", signature)], key=lambda t: t[0])
    return "OAuth " + ", ".join([_my_quote(k) + '="' + _my_quote(v) + '"' for k, v in auth_base_sorted])
