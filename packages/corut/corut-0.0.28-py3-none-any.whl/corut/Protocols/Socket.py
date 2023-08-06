#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Provides Socket protocol management.
"""

__author__ = 'ibrahim CÖRÜT'
__email__ = 'ibrhmcorut@gmail.com'

import time
import socket
import platform
from ..OS import try_except


class HostInformation:
    def __init__(self):
        self.os = None
        self.os_name = None
        self.host_ip_list = None

    @staticmethod
    def __get_host_ip_list(host_name):
        ip_list = []
        try:
            for ip in [i[4][0] for i in socket.getaddrinfo(host_name, None)]:
                if str(ip).split('.').__len__() == 4:
                    ip_list.append(ip)
            print(f'-------------> {host_name} IP list:{ip_list}')
        except Exception as error:
            print(error)
        return ip_list

    @try_except
    def __get_ip(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        print(f'-------------> {self.os_name} IP:{ip}')
        return ip

    @try_except
    def get_host_ip_addresses(self, host_name=None):
        self.os = platform.system()
        self.os_name = socket.gethostname().upper()
        if host_name:
            self.host_ip_list = self.__get_host_ip_list(host_name)
        else:
            self.host_ip_list = [self.__get_ip()]
        print(f'Computer Name:{self.os_name}/{self.os} OS -- Host IP List:{self.host_ip_list}')
        return self.host_ip_list


class Socket:
    def __init__(self):
        self.__socket = None
        self.__stream = None
        self.__timeout = 6
        self.__ip = None
        self.connect_status = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self, ip=None):
        if self.connect_status and ip and ip != self.__ip:
            self.disconnect()
        if not self.connect_status and ip:
            try:
                self.__socket = socket.socket()
                self.__stream = self.__socket.makefile('rwb', encoding='utf8')
                self.__socket.connect((ip, 12345))
                self.__socket.settimeout(self.__timeout)
                self.connect_status = True
                self.__ip = ip
                print(f':::::::::::> Socket Connected successfully IP:{ip}')
            except Exception as e:
                print(f"#########> Socket connection problem. Will try to reconnect to {ip}:{e}")
                self.disconnect()

    def reconnect(self, ip):
        print(f':::::::::::> Reconnecting to IP:{ip}')
        self.disconnect()
        self.connect(ip)

    @try_except
    def disconnect(self):
        if self.connect_status:
            self.__socket.shutdown(socket.SHUT_RDWR)
            self.__socket.close()
            print(':::::::::::> Socket connection was disconnected successfully')
        self.connect_status = False
        self.__ip = None

    def image_capture(self, name, layer):
        response = ''
        image_check = False
        data = error_message = None
        grab_image_timeout = time.time() + 90
        try:
            while not response.isdigit():
                if time.time() > grab_image_timeout:
                    print(':::::::::::> Socket Connection timeout interval exceeded.')
                    break
                self.__stream.write(("grab '%d'\r\n" % layer).encode())
                self.__stream.flush()
                response = self.__stream.readline().decode("utf-8").rstrip('\r\n')
            if response.isdigit():
                data = self.__stream.read(int(response))
                print(f":::::::::::> Grabbed Image:{name} --- Layer:{layer} --- IP:{self.__ip}")
            image_check = True
        except Exception as error:
            error_message = f'###########> Socket Image capture problem:{str(error)}'
            self.disconnect()
            data = None
        return image_check, data, error_message

    def send(self, command, command_name, func_name='testtool'):
        try:
            response = self.__stream.write(("%s '%s'\r\n" % (func_name, command)).encode())
            self.__stream.flush()
            print(f'{self.__ip} >> Socket ---> Send :::> {func_name} {command_name}')
            return response
        except Exception as error:
            print(f'###########> Socket command sender problem:{error}')
            self.disconnect()
            return None
