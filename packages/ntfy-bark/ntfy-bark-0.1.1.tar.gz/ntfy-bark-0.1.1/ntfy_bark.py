# -*- coding: utf-8 -*-
#
# Copyright (c) 2022~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys

import requests

def notify(title, message,  # for ntfy
           push_url,        # for bark
           timeout=30,
           **_):            # ignore other args

    body = {
        'title': title,
        'body': message,
    }

    response = requests.post(push_url, json=body, timeout=timeout)

    response.raise_for_status()

    resp_body = response.json()

    if resp_body.get('code') != 200:
        print(resp_body.get('message', response.text), file=sys.stderr)
        return 1
