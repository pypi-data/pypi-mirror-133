#!/usr/bin/env python
import random
import re
import os
import subprocess
import sys
from codefast.utils import shell
import joblib
from collections import defaultdict
from functools import reduce
import codefast as cf
from getpass import getpass
from cryptography.fernet import Fernet
import base64
import json
from typing import List, Dict, Tuple, Union, Optional


class AccountLoader:
    __db = os.path.join(cf.io.dirname(), 'memory.joblib')
    __keys = ['REDIS_HOST', 'REDIS_PORT', 'REDIS_PASSWORD']

    @classmethod
    def decode_config_file(cls) -> dict:
        cf.info('decode config file and dump to memory')
        loc = os.path.join(cf.io.dirname(), 'data/redis.txt')
        text = cf.io.reads(loc).encode()
        passwd = getpass('Enter password: ').rstrip()
        passwd = base64.urlsafe_b64encode(passwd.encode() * 10)
        key = Fernet.generate_key()
        key = passwd.decode('utf-8')[:43] + key.decode('utf-8')[43:]
        f = Fernet(key.encode())
        return json.loads(f.decrypt(text).decode('utf-8'))

    @classmethod
    def query_secrets(cls) -> Tuple[str]:
        auth_path: str
        try:
            auth_path = os.path.join(cf.io.dirname(), 'data/cauth')
            cmd = auth_path + ' -a'
            xstr = subprocess.check_output(
                cmd, shell=True).decode('utf-8').strip()
            js = json.loads(xstr)
            return js['redis_host'], js['redis_port'], js['redis_pass']
        except json.decoder.JSONDecodeError:
            cf.io.copy(auth_path, '/tmp/cauth')
            cf.error('failed to decode json {}'.format(xstr))
            return None, None, None
        except Exception as e:
            cf.error('failed to query secrets: {}'.format(e))
            return None, None, None

    @classmethod
    def set_secrets(cls, secrets: Dict[str, str]) -> None:
        values = [secrets[k] for k in cls.__keys]
        joblib.dump(values, cls.__db)
