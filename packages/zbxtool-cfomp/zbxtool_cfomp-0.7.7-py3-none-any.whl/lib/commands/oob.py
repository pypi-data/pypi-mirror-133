#!/bin/env python3
# coding:utf-8
"""
    Mgnt Servers主机组内主机与其他主机组做序列号匹配,
    匹配上的把普通主机的inventory OOB IP address的值
    设置为 Mgnt Servers主机 snmp interface的地址
"""

import argparse
import logging
from zabbix_api import ZabbixAPIException

parser = argparse.ArgumentParser("Matching inventory OOB IP address")
parser.add_argument('-g', '--group_name', help='Specify a group name')
parser.set_defaults(handler=lambda args: main(args))

target_group = 'Mgnt_servers'

def main(args):

    zapi = args.zapi

    # 1.取所有的常规组, 即非自动发现的组
    plain_groups = zapi.hostgroup.get({
        'output': ['name'],
        'filter': {'flag': 0}
    })


    # 2.取 Mgnt_servers 组的序列号 对应的 oob_ip

    oob_hosts_results = {}

    try:
        target_gid = next(filter(lambda x:x['name'] == target_group, plain_groups))['groupid']
    except StopIteration:
        logging.error(f'未找到组{target_group}')
        exit(1)

    target_hosts = zapi.host.get({
        'output': ['hostid'],
        'selectInventory': ['serialno_a'],
        'selectInterfaces': ['type', 'main', 'ip'],
        'groupids': target_gid
    })

    for host in target_hosts:

        # 抓取'Mgnt servers'组内主机, type=2, main=1的接口ip
        oob_ip = ''.join([item['ip'] for item in filter(lambda i: i['type'] == '2' and i['main'] == '1', host['interfaces'])])
        serialno = host['inventory'].get('serialno_a')

        if oob_ip and serialno:
            oob_hosts_results[serialno] = oob_ip



    # 3. 获取除 Mgnt_servers 外的剩余组内 host, 匹配序列号

    if args.group_name: # 指定仅更新某个组
        other_grps = filter(lambda x:x['name'] == args.group_name, plain_groups)
    else:
        other_grps = filter(lambda x:x['name'] != target_group, plain_groups)
    other_grpids = [g['groupid'] for g in other_grps]
  
    hosts = zapi.host.get({
        'output': ['hostid', 'name'],
        'selectInventory': ['serialno_a'],
        'groupids': other_grpids,
        'withInventory': True
    })

    for host in hosts:

        serialno = host['inventory'].get('serialno_a')
        oob_ip = oob_hosts_results.get(serialno)

        # 匹配到序列号, 更新该host的inventory oob_ip字段
        if serialno and oob_ip:
            try:
                zapi.host.update({
                    'hostid': host['hostid'],
                    'inventory': {
                        'oob_ip': oob_ip
                    }
                })
                logging.info(f'update host:{host["name"]} success, oob_ip -> {oob_ip}')
            except ZabbixAPIException as err:
                logging.error(err)
