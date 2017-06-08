#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
import json
import random
import platform
import requests as req
from lxml import etree
from subprocess import Popen, PIPE


class FreeVpn(object):
    """This is a script to update the free shadowsocks account automatically."""

    def __init__(self, *args):
        self.vpnhead = {"auth": "false", "timeout": 10}
        self.vpnkey = ['server', 'server_port', 'password', 'method', "remarks"]
        self.vpnprocess = {"https://get.freevpnss.me": "self.first_vpn", "http://isx.tn/": "self.second_vpn"}
        self.vpnlist = list()
        for _, item in enumerate(args):
            self.vpnlist.append(item)

        self.header = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"]
        self.headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'User-Agent': random.choice(self.header)}

    def start_update(self):
        if platform.system() == 'Windows':
            sub = os.popen("tasklist /svc").readlines()
            for _, i in enumerate(sub):
                if "Shadowsocks.exe" in i.strip(" \r\n"):
                    try:
                        os.system("taskkill /f /im Shadowsocks.exe")
                    except Exception as e:
                        raise e
        else:
            pass
        for url, func in self.vpnprocess.items():
            tree = self.gethtml(url)
            eval(func)(tree)
        self.update_config()
        self.start_shadowsock()


    def update_config(self):
        confpath = "gui-config.json"
        if os.path.exists(confpath):
            pass
        else:
            confpath = "Shadow/" + confpath

        with open(confpath, 'r') as f:
            content = json.load(f)
        content["configs"] = self.vpnlist
        new = json.dumps(content, sort_keys=True, indent=4, separators=(',', ': '))
        new = new.replace('"false"', 'false')
        with open(confpath, 'w') as f:
            f.write(new)


    def start_shadowsock(self):
        try:
            Popen("Shadowsocks.exe", stdout=PIPE, stderr=PIPE)
        except Exception as e:
            raise e
        else:
            if platform.python_version_tuple()[0] == "3":
                input("Shadowsocks is running with new config, please ENTER to exit:")
            else:
                raw_input("Shadowsocks is running with new config, please ENTER to exit:")


    def gethtml(self, vpnurl):
        try:
            res = req.get(vpnurl, headers=self.headers)
            res.encoding = "utf-8"
            if res.status_code == req.codes.ok:
                tree = etree.HTML(res.text)
            else:
                tree = None
            return tree
        except Exception as e:
            return None


    def first_vpn(self, tree):
        if tree != None:
            panels = tree.xpath('//div[@class="panel-body"]')
            for _, panel in enumerate(panels):
                if panel.xpath('p[2]/text()')[0].find("freevpnss") == -1:
                    self.parse_info(panel.xpath('p/text()'))


    def second_vpn(self, tree):
        if tree != None:
            panels = tree.xpath('//div[@class="hover-text"]')
            for _, panel in enumerate(panels):
                if panel.xpath('string(h4[last()])').find("auth") == -1:
                    self.parse_info(map(panel.xpath, ["string(h4[%s])" % x for x in range(1, 5)]))


    def parse_info(self, items):
        tmp = [self.strsplit(x)[-1] for x in items if self.strsplit(x)[0]]
        if "" not in tmp:
            tmp.append(tmp[2])
            vpndict = dict(self.vpnhead)
            vpndict.update(zip(self.vpnkey, tmp))
            self.vpnlist.append(vpndict)


    def strsplit(self, item):
        if platform.python_version_tuple()[0] == "2":
            item = item.encode("utf-8")
        if item.find(":") != -1:
            res = item.split(":")[-1]
            flag = True
        elif item.find("：") != -1:
            res = item.split("：")[-1]
            flag = True
        else:
            res = item
            flag = False
        return flag, res.strip()


if __name__ == '__main__':

    # If you have other fixed shadowsocks account, you may just place it into the arguement fixed_vpn, and the update procedure will keep it whenever updating.
    """
    fixed_vpn = {
        "server": "server_host",
        "server_port": 4000,
        "password": "passwd",
        "method": "encrypt_type",
        "remarks": "remarks",
        "auth": "false",
        "timeout": 10
    }
    freevpn = FreeVpn(fixed_vpn)
    """
    freevpn = FreeVpn()
    freevpn.start_update()