#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Used to manage RedRat RF devices
For RedRad RF,
 the RR_CLI.exe and RedRat.dll files should be copied
 under the 'C:\\Users\\USERS\\.Corut\\RedRat\\' directory.
"""

__author__ = 'ibrahim CÖRÜT'
__email__ = 'ibrhmcorut@gmail.com'

import os
import platform
from subprocess import call, TimeoutExpired
from ..Shell import run_cmd, run_cmd_2
from ..OS import join_directory, get_path_home, get_platform


class RedRat:
    def __init__(self):
        self.__path_exe = None
        self.__xml_name = None
        self.__xml_path = None
        self.path_files_xml_directory = None
        self.device = None
        self.devices = ['None']
        self.RC_TYPE_REDRAT_LIST = [
            'OEM', 'HITACHI', 'PANASONIC', 'PHILIPS', 'JVC', 'TOSHIBA', 'MEDION'
        ]

    def get_devices(self):
        self.get_path()
        assert os.path.exists(self.__path_exe), 'Check the file path and RR_CLI.exe name!..'
        self.devices = ['None']
        cmd = ("mono " if get_platform() == 'linux' else "") + f'{self.__path_exe} test -blink'
        if platform.system() == 'Linux':
            try:
                with call(cmd, shell=True, timeout=7) as line:
                    print(line)
                    if 'No name' in line:
                        self.devices.append(str(line[line.index('USB device') + 11:]).strip())
            except TimeoutExpired:
                pass
        else:
            for line in run_cmd_2(cmd, shell=True, timeout=7):
                print(line)
                if 'No name' in line:
                    self.devices.append(str(line[line.index('USB device') + 11:]).strip())
        print(f'RedRat Devices List:{self.devices}')
        return self.devices

    def get_path(self):
        self.__path_exe = join_directory([get_path_home(), '.Corut', 'RedRat', 'RR_CLI.exe'])
        if not os.path.isfile(self.__path_exe):
            print(f'Cannot find RedRat sender program in {self.__path_exe}')
        if not os.path.isfile(os.path.join(os.path.dirname(self.__path_exe), 'RedRat.dll')):
            print(
                f'Cannot find DLL needed for RedRat in '
                f'{os.path.join(os.path.dirname(self.__path_exe), "RedRat.dll")}'
            )
        print(f'RedRat Exe File:{self.__path_exe}')
        return self.__path_exe

    def set_red_rat_xml_file(self, name):
        self.get_path()
        self.__xml_name = name
        self.__xml_path = os.path.join(self.path_files_xml_directory, f'{str(name).upper()}.xml')
        print(f'{self.__xml_path} file is set.')
        return name

    def send(self, command, command_name):
        print(f"Send {self.device.split(' - ')[0]} :::> {self.__xml_name} ---> {command_name}")
        command_line = [
            self.__path_exe,
            self.device.split(' - ')[0],
            '-output',
            self.__xml_path,
            '-device',
            self.__xml_name,
            '-signal',
            command
        ]
        run_cmd(command_line, print_output_status=False)
