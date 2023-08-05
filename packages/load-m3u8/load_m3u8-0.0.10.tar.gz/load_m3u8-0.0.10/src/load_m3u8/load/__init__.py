# _*_coding:utf-8_*_
import binascii
import logging

import m3u8.parser
import requests
from Crypto.Cipher import AES

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
headers = {'User-Agent': user_agent}


def load_ts_done(feature):
    if feature.exception() is not None:
        logging.debug('load ts exception: %s', feature.exception())
    else:
        logging.debug('load ts result: %s', feature.result())


def load_ts(data):
    url, encrypt_key, ts_name = data
    try:
        ts_data = []
        if m3u8.parser.is_url(url):
            res = requests.get(url, headers=headers)
            if res is None or res.content is None:
                return 'exception end'
            ts_data = res.content
        else:
            with open(url, 'rb') as read:
                if read.readable():
                    ts_data = read.read()

        with open(ts_name, 'wb') as fp:
            if encrypt_key is None:
                fp.write(ts_data)
            else:
                if m3u8.parser.is_url(encrypt_key.uri):
                    aes_key = requests.get(encrypt_key.uri, headers=headers).content
                else:
                    with open(encrypt_key.uri, 'rb') as read:
                        if read.readable():
                            aes_key = read.read()
                fp.write(decrypt(ts_data, aes_key, encrypt_key.iv))
    except Exception as e:
        logging.exception('load failed')
        return f'{ts_name} exception: {str(e)}'
    return f'{ts_name} succeed'


def decrypt(content, key, iv):
    """
    M3U8 has the same AES-IV and key
    :param content: Encrypted content
    :param key: AES key
    :param iv: IV vector (Ignore)
    :return: Decrypt content
    """
    try:
        key = a2b_hex(key)
        iv = a2b_hex(key)
        cryptos = AES.new(key, AES.MODE_CBC, iv)
        return cryptos.decrypt(content)
    except Exception as e:
        logging.exception('decrypt failed')
        return content


def a2b_hex(data):
    if data is None:
        return None
    if isinstance(data, bytes):
        data = data.decode()
    if data[0:2] == '0x':
        data = binascii.a2b_hex(data[2:])
    if isinstance(data, str):
        data = data.encode()
    return data
