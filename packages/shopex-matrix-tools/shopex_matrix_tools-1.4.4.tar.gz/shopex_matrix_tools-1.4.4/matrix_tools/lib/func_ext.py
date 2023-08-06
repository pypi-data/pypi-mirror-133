#!/usr/bin/python
# -*- coding: UTF-8 -*-
# requests 中文文档 https://docs.python-requests.org/zh_CN/latest/user/advanced.html#blocking-or-nonblocking


import requests
import time
import hashlib
import socket
import uuid
from requests import adapters
from . get_sign import create

requests.adapters.DEFAULT_RETRIES = 3  # 默认超时重连次数, requests可以对同一个host保持长连接
requests.adapters.DEFAULT_POOLSIZE = 30  # 默认连接池大小（协程数尽量不要超过此大小）
requests.adapters.DEFAULT_POOLBLOCK = True  # 当超过限制时，由pool_block参数决定是否阻塞等待。


mac_addr = uuid.uuid1().hex[-12:]


def shopex_request(url, method='post', req_type='json', data='', **kwargs):
    sys_log_tag = kwargs.pop('sys_log_tag', 'matrix')
    try:
        if method == 'post':
            if req_type == 'json':  # json格式提交请求
                r = requests.post(url, json=data, **kwargs)
            elif req_type == 'form':  # 表单格式提交请求
                r = requests.post(url, data=data, **kwargs)
        elif method == 'get':
            r = requests.get(url, **kwargs)
        else:
            r = requests.post(url, data=data)
        r.raise_for_status()
        return 'succ', r.text
    except requests.exceptions.HTTPError as e:
        write_log("{}_{}".format(url, str(e)), method=sys_log_tag)
        if r.status_code >= 500:
            return 'fail', str(e)
        return 'dams', str(e)
    except requests.exceptions.ConnectTimeout as e:
        write_log("{}_{}".format(url, str(e)), method=sys_log_tag)
        return 'fail', str(e)
    except Exception as e:
        write_log("{}_{}".format(url, str(e)), method=sys_log_tag)
        return 'fail', str(e)


def write_log(msg, method):
    import syslog
    syslog.openlog(method, syslog.LOG_LOCAL0)
    syslog.syslog(syslog.LOG_INFO, msg)


def str2sec(src_str, format='%Y-%m-%d %H:%M:%S', float_num=False):
    try:
        time_tuple = time.strptime(src_str, format)
        timestamp = time.mktime(time_tuple)
        return float_num and timestamp or int(timestamp)
    except Exception as e:
        return ''


def sec2str(format='%Y-%m-%d %H:%M:%S', sec=None, gmtime=False):
    try:
        func = time.gmtime if gmtime else time.localtime
        return time.strftime(format, func(sec))
    except Exception as e:
        return ''


def get_shopex_b2c_sign_str(_token_str, data):
    _sign_str = ''
    for key in sorted(data):
        _sign_str += str(data[key])

    _sign_str += _token_str
    _sign_str = get_md5(_sign_str.strip()).lower()

    return _sign_str


def get_md5(string):
    """
    md5加密
    :param string:
    :return:
    """
    try:
        m = hashlib.md5()
        m.update(string.encode('utf-8'))
        dest = m.hexdigest()
        return dest
    except Exception as e:
        return False


def get_uuid():
    """
    生成全局唯一id(长度32)
    生成规则： 时间戳(8个16进制位)+机器IP(8个16进制位)+随机生成的唯一序列(16个16进制位)
    """
    random_uuid = '%s%s%s' % (timestamp2hex(time.time()), ip2hex(local_ip), generate_id()[8:-8])

    return random_uuid


def get_local_ip():
    ip = socket.gethostbyname(socket.gethostname())
    return ip


def ip2hex(ip_address):
    """ip串转换为16进制串"""
    return ''.join(['%02x' % int(i) for i in ip_address.split('.')])


def timestamp2hex(timestamp):
    """时间戳转换为16进制串"""
    return '%08x' % int(timestamp)


def generate_id():
    local_time = "%0.8f" % time.time() + uuid.uuid4().hex
    msg_str = '%s%s' % (mac_addr, local_time)
    return get_md5(msg_str)


local_ip = get_local_ip()


def filter_map(params):
    keys = list(params.keys())  # python3中dict.keys()是个迭代器
    for key in keys:
        if not params.get(key):
            params.pop(key)


def get_matrix_sign_str(_token_str, data):
    sign = create.get_sign(_token_str, data)
    return sign