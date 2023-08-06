#!/usr/bin/python
# -*- coding: UTF-8 -*-

import hashlib


class GetSign(object):
    def __init__(self):
        pass

    def get_sign(self, token, params):
        sign = self.get_sign_str(params)
        sign = self.get_md5(sign).upper()
        sign = self.get_md5(sign+str(token))
        return sign.upper()

    def get_sign_str(self, params):
        sign = ''
        if type(params) == dict:
            sign = self.get_value_str(params)
        return sign

    def get_value_str(self, value):
        if type(value) == list:
            value = dict(zip(range(len(value)), value))
        if type(value) == dict:
            value = self.do_dict(value)
        return value

    def do_dict(self, dic):
        s = ''
        keys = sorted(dic)
        for key in keys:
            value = self.recursive(dic[key])
            s = s + str(key) + str(value)
        return s

    def recursive(self, value):
        if type(value) == dict:
            return self.get_value_str(value)
        if type(value) == list:
            return self.get_value_str(value)
        return value

    def get_md5(self, string):
        try:
            m = hashlib.md5()
            m.update(string.encode())
            dest = m.hexdigest()
            return dest
        except Exception as e:
            return False


create = GetSign()