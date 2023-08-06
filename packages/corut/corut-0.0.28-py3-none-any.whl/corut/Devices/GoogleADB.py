#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
It is aimed to integrate Google adb Tool into an application made/will made
with Python and to provide ease of use.
"""

__author__ = 'ibrahim CÖRÜT'
__email__ = 'ibrhmcorut@gmail.com'

import threading
from ppadb.client import Client as _Client
from .. import print_error
from ..DateTime import add_date_time_to_line
from ..OS import get_path_home, join_directory, try_except, get_platform
from ..ParallelProcessing import ThreadWithReturnValue
from ..Shell import run_cmd


class Client:
    def __init__(self):
        self.__adb_path = self.get_path()
        self.__client = None
        self.__device = None
        self.__lock = None
        self.__reader_status_pause = False
        self.__reader_status = False
        self.__thread = None
        self.data = None
        self.device = None
        self.devices = None

    @staticmethod
    def get_path():
        if get_platform() == 'windows':
            return join_directory([get_path_home(), '.Corut', 'GoogleADB', 'adb.exe'])
        else:
            return 'adb'

    @try_except
    def get_devices(self):
        print(f'Google ADB Application Path:{self.__adb_path}')
        run_cmd(f'{self.__adb_path} version')
        self.devices = ['None']
        for device in run_cmd(f'{self.__adb_path} devices').splitlines():
            if '\tdevice' in device:
                self.devices.append(device.strip('\tdevice').strip(':5555'))
        print(f'Google Devices List:{self.devices}')
        return self.devices

    def get_usb_directories(self):
        directories = []
        data = self.shell('ls -l /storage').split('\n')
        if data:
            for line in data:
                if (
                        not (str(line).endswith(' self') or str(line).endswith(' emulated')) and
                        str(line).startswith('drwxrwx')
                ):
                    directories.append(f'/storage/{line.split()[-1]}')
        print(f':::::::::::> ADB {self.device} ---> USB Directories:{directories}')
        return directories

    def connect(self, device=None):
        self.device = self.device if device is None else device
        if self.device:
            try:
                self.__client = _Client(host='127.0.0.1', port=5037)
                print(f'{self.__adb_path} Version:%s' % self.__client.version())
                if self.device.replace('.', '').isdigit() and len(self.device.split('.')) == 4:
                    self.__client.remote_connect(self.device, 5555)
                    self.device = f'{self.device}:5555'
                self.__device = self.__client.device(device)
                print(f':::::::::::> ADB {self.device} ---> Connected successfully')
            except ConnectionRefusedError as error:
                print(f':::::::::::> ADB {self.device} ---> CONNECTION ERROR! :::>{error}')
            except Exception as error:
                print_error(error, locals())
                self.disconnect()

    def disconnect(self):
        self.__reader_status = False
        if self.__thread:
            self.__thread.stop()
        if self.device:
            run_cmd(f'{self.__adb_path} disconnect {self.device}')
            print(f':::::::::::> ADB {self.device} ---> Connection was disconnected successfully')
        self.__device = None

    def shell(self, command):
        result = None
        try:
            print(f':::::::::::> ADB {self.device} ---> Shell Command:{command}')
            self.__device = self.__client.device(self.device)
            result = str(self.__device.shell(command))
        except Exception as error:
            print(f':::::::::::> ADB {self.device} ---> SHELL ERROR! :::>{error}')
        return result

    def pull(self, source, target):
        status = True
        try:
            self.__device = self.__client.device(self.device)
            self.__device.pull(source, target)
            message = f':::::::::::> ADB {self.device} ---> Pull Source:{source} | Target:{target}'
        except Exception as error:
            message = f':::::::::::> ADB {self.device} ---> PULL ERROR! :::> {error}'
            status = False
        print(message)
        return status, message

    def push(self, source, target):
        status = True
        try:
            self.__device = self.__client.device(self.device)
            self.__device.push(source, target)
            message = f':::::::::::> ADB {self.device} ---> Push Source:{source} | Target:{target}'
        except Exception as error:
            message = f':::::::::::> ADB {self.device} ---> PUSH ERROR! :::> {error}'
            status = False
        print(message)
        return status, message

    def install_or_uninstall(self, process, package):
        status = True
        try:
            self.__device = self.__client.device(self.device)
            if str(process).lower() == 'install':
                self.__device.install(package, test=True, reinstall=True)
            if str(process).lower() == 'uninstall':
                self.__device.uninstall(package)
            message = f':::::::::::> ADB {self.device} ---> {str(process).title()}ed >>> {package}'
        except Exception as error:
            message = f':::::::::::> ADB {self.device} ---> INSTALL/UNINSTALL ERROR! :::> {error}'
            status = False
        print(message)
        return status, message

    def grab_image(self, path):
        status = True
        try:
            self.__device = self.__client.device(self.device)
            result = self.__device.screencap()
            with open(path, "wb") as fp:
                fp.write(result)
                message = f':::::::::::> ADB {self.device} ---> Capture image successfully: {path}'
        except Exception as error:
            message = f':::::::::::> ADB {self.device} ---> GRAB IMAGE ERROR! :::> {error}'
            status = False
        print(message)
        return status, message

    def start_log_reader(self):
        try:
            self.__reader_status = True
            self.__thread = ThreadWithReturnValue(
                target=self.__start_log_reader,
                name=f'ADB LOGCAT {self.device}',
                daemon=True
            )
            self.__thread.start()
        except (KeyboardInterrupt, SystemExit) as error:
            print(f':::::::::::> ADB {self.device} ---> START LOG READER ERROR!:{error}')
            self.disconnect()

    def __start_log_reader(self):
        if self.device:
            self.__device = self.__client.device(self.device)
            self.__device.shell("logcat -c")
            self.__device.shell("logcat", handler=self.dump_logcat)

    def dump_logcat(self, connection):
        self.__lock = threading.Lock()
        self.data = [f'<::::::: Logcat Log Read Start :::::::> {self.device}\n']
        print(f':::::::::::> ADB {self.device} ---> Logcat Reader Started')
        stream = connection.socket.makefile('rwb', encoding='utf8')
        while self.__reader_status:
            try:
                if not self.__reader_status_pause:
                    line = stream.readline()
                    if len(line) > 0:
                        self.__lock.acquire()
                        self.data.append(
                            add_date_time_to_line(
                                line.rstrip().decode(encoding='UTF-8', errors='ignore')
                            )
                        )
                        self.__lock.release()
            except Exception as error:
                print(f':::::::::::> ADB {self.device} ---> DUMP LOGCAT ERROR!:{error}')
        stream.close()
        connection.close()
        print(f':::::::::::> ADB {self.device} ---> Logcat Reader Stopped')

    def data_clean(self, status):
        if status == 'End':
            self.__reader_status_pause = True
            self.__lock.acquire()
            self.data.append(f'<::::::: Logcat Log Read End :::::::> {self.device}\n')
            self.__lock.release()
        elif status == 'Start':
            self.__lock.acquire()
            self.data.clear()
            self.data = [f'<::::::: Logcat Log Read Start :::::::> {self.device}\n']
            self.__lock.release()
            self.__reader_status_pause = False
