#!/usr/bin/env python3
# -*    - coding: utf-8 -*-

"""
Designed to control Serial Devices.
"""

__author__ = 'ibrahim CÖRÜT'
__email__ = 'ibrhmcorut@gmail.com'

import binascii
import threading
import re
from time import sleep
from serial import Serial, STOPBITS_ONE, PARITY_NONE, EIGHTBITS, SerialException
from serial.tools import list_ports
from ..DateTime import add_date_time_to_line, add_date_time_to_list
from ..ParallelProcessing import ThreadWithReturnValue


# ------------------------------ Astro Devices ---------------------------------------
ENQ = "\x05"  # Request to start terminal mode
EOT = "\x04"  # Request to end terminal mode
ACK = "\x06"  # Positive acknowledge character
PTS = "\x41"  # PTS command
NAK = "\x15"  # Negative acknowledge character
STX = "\x02"  # Transmission text (command) start
ETB = "\x17"  # Transmission text (data) end
ETX = "\x03"  # Transmission text (command, data) end
TRDT = "\x10"  # When data is to be transmitted,this command is placed at the head of the block before it is transmitted
ESTS = "\x11"  # When an error status is to be transmitted,an error number is transmitted with this command preceding it
SPTS = "\x47"
SPTS4 = "\x20\x2A"
LPTS4 = "\x20\x2B"
EXPDN = "\x09"  # EXPDN command
EXPON = "\x0E"  # EXPON command
INDC4 = "\x24\x21"
EXBN4 = "\x24\x22"
EXTCMD = "\xFF"  # Extended command identification code (* Added with old VG models)
VG4CMD = "\xFD"  # New command identification code
EXPDN4 = "\x24\x20"
INIBUF4 = "\x24\x23"
WINCLR4 = "\x28\x63"
EXPONOFF4 = "\x24\x30"
# ------------------------------------------------------------------------------------


class GetSerialDevices:
    def __init__(self):
        self.rns = None
        self.uart = None
        self.arduino = None
        self.astro = None

    def __check_device(self, ports, command, baudrate):
        other_devices = []
        for port in ports:
            s = None
            if 'ttyusb' in str(port[0]).lower() or 'com' in str(port[0]).lower():
                try:
                    s = Serial(port[0], baudrate=baudrate, timeout=2, write_timeout=1)
                    # set timeout=2 for arduino problem
                    s.write(command)
                    response = s.read(33)
                    if type(response) == bytes:
                        response = response.strip()
                    print(f'{port[0]} ---> {baudrate} ---> ##{response}##')
                    if response in (b'OK', [b'OK'], b'\x00OK\xff', [b'\x00OK\xff']):
                        self.rns.append(f"{port[0]} - {port[1]}")
                    elif b'arduino' in response.lower():
                        # Arduino, Arduino is Ready, <Arduino is ready>,
                        # Arduino Uno, <Arduino Uno is ready>
                        self.arduino.append(f"{port[0]} - {port[1]}")
                    elif str(port.pid).isdigit() and baudrate == 38400:
                        if response and type(response) == bytes and response == ACK.encode():
                            self.astro.append(f"{port[0]} - {port[1]}")
                        else:
                            self.uart.append(f"{port[0]} - {port[1]}")
                    else:
                        other_devices.append(port)
                except (OSError, SerialException):
                    pass
                finally:
                    try:
                        s.close()
                    except Exception as _e:
                        print(_e)
        return other_devices

    def get_all_active_serial_devices(self):
        self.rns = []
        self.uart = []
        self.arduino = []
        self.astro = []
        devices = sorted(list_ports.comports())
        devices = self.__check_device(devices, f"CHECKRMC\n".encode(), 115200)  # RNS,UART,Arduino
        if len(devices) > 0:
            self.__check_device(devices, ENQ.encode(), 38400)  # for Astro
        print(f'Devices UART: {self.uart}')
        print(f'Devices RNS: {self.rns}')
        print(f'Devices Arduino: {self.arduino}')
        print(f'Devices Astro: {self.astro}')
        return self.rns, self.uart, self.arduino, self.astro


class SerialDevice:
    def __init__(
            self,
            port=None,
            device_type='UART',
            baudrate=115200,
            timeout=0.9,
            write_timeout=0.9,
            enter_key_for_send='\r\n'
    ):
        self.__baud_rate = baudrate
        self.__enter_key_for_send = enter_key_for_send
        self.__serial = None
        self.__timeout = timeout
        self.__write_timeout = write_timeout
        self.__short_name = None
        self.connection_status = False
        self.device_type = device_type
        self.port = port

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        if self.__serial is None:
            if self.port:
                self.__short_name = f'{self.port.split(" - ")[0]}:Serial {self.device_type} Device'
            try:
                self.__serial = Serial(
                    port=self.port.split(" - ")[0],
                    baudrate=self.__baud_rate,
                    bytesize=EIGHTBITS,
                    parity=PARITY_NONE,
                    stopbits=STOPBITS_ONE,
                    timeout=self.__timeout,
                    write_timeout=self.__write_timeout
                )
                if not self.__serial.isOpen():
                    self.__serial.open()
                self.connection_status = True
                print(f'{self.__short_name} Connection Successful...')
            except FileNotFoundError:
                self.disconnect()
            except Exception as error:
                print(f'### Error!!! ### {self.__short_name} Connect:{error}')

    def disconnect(self):
        try:
            if self.__serial is not None:
                if self.__serial.isOpen():
                    self.__serial.close()
                    print(f'{self.__short_name} Disconnect Successful...')
        except Exception as error:
            print(f'### Error!!! ### {self.__short_name} Disconnect:{error}')
        self.connection_status = False
        self.__serial = None
        self.__short_name = None

    def send(self, command, command_name):
        try:
            if isinstance(command, bytes):
                self.__serial.write(command)
            else:
                self.__serial.write(f'{command}{self.__enter_key_for_send}'.encode())
            if command == command_name:
                print(f'{self.__short_name} ---> Send :::> {command_name}')
            else:
                print(f'{self.__short_name} ---> Send :::> {command_name} --->{command}')
            self.__serial.flush()
        except Exception as error:
            print(f'### Error!!! ### {self.__short_name} Send:{error}')

    def get_serial_in_waiting(self):
        try:
            return self.__serial.inWaiting()
        except Exception as e:
            print(e)
            return 1

    def read(self, size):
        try:
            return self.__serial.read(size)
        except Exception as e:
            print(e)
            return b''


# noinspection PyBroadException
class UartRW:
    def __init__(self):
        self.__thread = None
        self.__serial = None
        self.__reader_pause_status = None
        self.__reader_status = None
        self.__lock = None
        self.__buf = None
        self.data = []
        self.port = None
        self.device_name = None

    def get_connection_status(self):
        if self.__serial is None:
            return False
        return self.__serial.connection_status

    def stop(self):
        try:
            self.__reader_pause_status = True
            self.__reader_status = False
            if self.__serial:
                self.__serial.disconnect()
            if self.__thread:
                self.__thread.stop()
            self.data_clean('End')
            self.__thread = None
            self.__buf = None
            print(f'Serial Thread Reader Stopped:{self.port}')
        except Exception as error:
            print(f'Error Serial Thread:{error}')

    def __reconnect(self):
        with self.__lock:
            self.stop()
            print(f'Serial Re-Connect:{self.port}')
            self.__uart_reader_function()

    def __uart_reader_function(self):
        print(f'Serial Thread Reader Start:{self.port}')
        self.__buf = b''
        while self.__reader_status:
            try:
                if not self.__reader_pause_status:
                    try:
                        buf = self.__serial.read(1)
                        if buf != b'':
                            self.__buf += buf
                            self.__buf += self.__serial.read(self.__serial.get_serial_in_waiting())
                            find = self.__buf.rfind(b'\r\n')
                            if find > 0:
                                buf = self.__buf[:find] + b'\r\n'
                                self.__buf = self.__buf[find:].lstrip()
                                # -------- due to bad ascii characters in the last lines -----
                                find = self.__buf.find(b'\xff')
                                if find > 0:
                                    buf += self.__buf
                                    self.__buf = b''
                                buf = buf.decode(encoding='UTF-8', errors='ignore')
                                self.__lock.acquire()
                                self.data.extend(add_date_time_to_list(buf))
                                self.__lock.release()
                    except Exception as error:
                        print(
                            f'### Error!!! ### '
                            f'PORT:{self.port} Serial {self.device_name} Device Read:{error}'
                        )
            except Exception as error:
                print(f'Error Serial Thread Reader:{error}')

    def start(self):
        try:
            self.__serial = SerialDevice(
                port=self.port,
                device_type='UART',
                baudrate=115200,
                timeout=0.9,
                write_timeout=0.9,
                enter_key_for_send='\r\n'
            )
            self.__reader_pause_status = False
            self.__reader_status = True
            self.__lock = threading.Lock()
            self.device_name = str(self.port).split(' - ')[0]
            self.__serial.connect()
            self.data_clean('Start')
            if self.__serial.connection_status:
                self.__thread = ThreadWithReturnValue(
                    target=self.__uart_reader_function,
                    name=f'SERIAL UART {self.device_name}',
                    daemon=True
                )
                self.__thread.start()
        except (KeyboardInterrupt, SystemExit) as error:
            print(f'Error Serial Thread:{error}')
            self.stop()

    def send(self, command, command_name):
        try:
            with self.__lock:
                self.__serial.send(command, command_name)
        except PermissionError as error:
            print(f'Error Serial Send:{error}')
            self.__reconnect()
            self.send(command, command_name)

    def data_clean(self, status):
        if status == 'End':
            self.__reader_pause_status = True
            if self.__lock:
                self.__lock.acquire()
            self.data.append(
                add_date_time_to_line(f'<::::::: Serial Log Read End :::::::> {self.port}')
            )
            if self.__lock:
                self.__lock.release()
        elif status == 'Start':
            if self.__lock:
                self.__lock.acquire()
            self.data.clear()
            self.data.append(
                add_date_time_to_line(f'<::::::: Serial Log Read Start :::::::> {self.port}')
            )
            if self.__lock:
                self.__lock.release()
            self.__reader_pause_status = False

    def data_extend(self, data):
        data_new = []
        for d in data:
            data_new.append(add_date_time_to_line(d))
        self.__lock.acquire()
        self.data.extend(data_new.copy())
        self.__lock.release()


class SerialAstro:
    """
    For example;
    sender(
            {
                'program': 1040,
                'multi_pattern': ('Name', 'MonoScope'),
            }
        )
    """
    def __init__(self):
        self.ASTRO_MODELS = [
            'VG-848', 'VG-835', 'VG-849/A/B', 'VG-858', 'VG-830', 'VG-857', 'VG-859/A/B',
            'VG-837', 'VG-835A', 'VG-849C', 'VG-859C', 'VG-870B'
        ]
        self.__PATTERNS = None
        self.__PATTERNS_NAMES = None
        self.__VARIABLES = None
        self.__serial = None
        self.multi___PATTERNS = None
        self.port = None
        self.device_model = self.ASTRO_MODELS[11]

    def start(self):
        if self.device_model == 'VG-870B':
            self.__PATTERNS = {
                3: 'INV', 6: 'CharacterPlane', 7: 'OPT', 8: 'Checker', 9: 'Aspect', 10: 'Raster',
                11: 'MonoScope', 12: 'Sweep', 13: 'Ramp', 14: 'GrayScale', 15: 'ColorBar',
                17: 'Name', 18: 'Cursor', 19: 'Window', 24: 'Burst', 25: 'Circle', 26: 'X',
                27: '+', 28: 'RECTANGLE', 29: 'DOTS', 30: 'CROSS', 31: 'CHARA'
            }
            self.__PATTERNS_NAMES = {}
            for key in self.__PATTERNS:
                self.__PATTERNS[key] = self.__PATTERNS[key].upper().replace(' ', '')
                self.__PATTERNS_NAMES[self.__PATTERNS[key].upper().replace(' ', '')] = key
            self.__VARIABLES = {
                'program': ['Choose program', range(1001, 2001), 0],
                'pattern': ['Choose pattern', list(self.__PATTERNS.keys()), 0],
                'multi_pattern': ['Choose multiple patterns', list(self.__PATTERNS.keys()), 0],
            }
        else:
            self.__PATTERNS = {
                0: 'CHARA', 1: 'CROSS', 2: 'DOTS', 3: 'CIRCLE', 4: '+', 5: 'RECTANGLE', 6: 'X',
                7: 'COLOR', 8: 'GRAY', 9: 'BURST', 10: 'WINDOW', 11: 'OPT1', 12: 'OPT2',
                13: 'NAME', 14: 'CURSOR'
            }
            self.__PATTERNS_NAMES = {}
            for key in self.__PATTERNS:
                self.__PATTERNS_NAMES[self.__PATTERNS[key].upper().replace(' ', '')] = key
            self.multi___PATTERNS = {
                0: 'CHARA', 1: 'CROSS', 2: 'DOTS', 3: 'CIRCLE', 4: '+', 28: 'RECTANGLE', 6: 'X',
                7: 'COLOR', 8: 'GRAY', 9: 'BURST', 10: 'WINDOW', 11: 'NAME'
            }
            self.__VARIABLES = {
                'program': ['Choose program', range(0, 1000), 0],
                'pattern': ['Choose pattern', list(self.__PATTERNS.keys()), 0],
                'multi_pattern': ['Choose multiple patterns', list(self.__PATTERNS.keys()), 0],
            }
        self.__serial = SerialDevice(
                port=self.port,
                device_type='Astro',
                baudrate=38400,
                timeout=0.9,
                write_timeout=0.9,
                enter_key_for_send='\r\n'
            )
        self.__serial.connect()

    def stop(self):
        if self.__serial is not None:
            self.__serial.disconnect()
        self.__init__()

    @staticmethod
    def __char2hex(char=None):
        char = char.lower()
        if char == '0':
            char = '\x00'
        elif char == '1':
            char = '\x01'
        elif char == '2':
            char = '\x02'
        elif char == '3':
            char = '\x03'
        elif char == '4':
            char = '\x04'
        elif char == '5':
            char = '\x05'
        elif char == '6':
            char = '\x06'
        elif char == '7':
            char = '\x07'
        elif char == '8':
            char = '\x08'
        elif char == '9':
            char = '\x09'
        elif char == 'a':
            char = '\x0a'
        elif char == 'b':
            char = '\x0b'
        elif char == 'c':
            char = '\x0c'
        elif char == 'd':
            char = '\x0d'
        elif char == 'e':
            char = '\x0e'
        elif char == 'f':
            char = '\x0f'
        else:
            char = '\xff'  # error code
        return char

    @staticmethod
    def __get_error_message(error):
        message_target = 'range when direct display or a program was executed.'
        if error == "00":
            msg = "An attempt has been made to save data when the memory card was not installed."
        elif error == "01":
            msg = "Program which was input is disabled " \
                  "when direct display or a program was executed."
        elif error == "02":
            msg = "Horizontal sync data is outside the 5.00 MHz <= Dot Clock <= 300.00 MHz "
            msg += message_target
        elif error == "03":
            msg = "Horizontal sync data is outside the H Period >= Hsync + HBackp + Hdisp (dot) "
            msg += message_target
        elif error == "04":
            msg = "Horizontal sync data is outside the H Period >= Hsync + HBackp + Hdisp (µs) "
            msg += message_target
        elif error == "05":
            msg = "Horizontal sync data is outside the H Period >= HDstart + HDwidth (dot) "
            msg += message_target
        elif error == "06":
            msg = "Horizontal sync data is outside the H Period >= HDstart + HDwidth (µs) "
            msg += message_target
        elif error == "16":
            msg = "Correct data was not set in the output condition data."
        elif error == "17":
            msg = "Correct data was not set in the character pattern data."
        elif error == "18":
            msg = "Correct data was not set in the crosshatch pattern data."
        elif error == "19":
            msg = "Correct data was not set in the dot pattern data."
        elif error == "20":
            msg = "Correct data was not set in the circle pattern data."
        elif error == "21":
            msg = "Correct data was not set in the burst pattern data."
        elif error == "22":
            msg = "Correct data was not set in the window pattern data."
        elif error == "23":
            msg = "Correct data was not set in the color bar pattern data."
        elif error == "24":
            msg = "There is an error in a parameter."
        elif error == "25":
            msg = "There is an error in the data."
        elif error == "26":
            msg = "Sync signals have not been set."
        else:
            msg = f"Unknown type of error...error code: {error}"
        return msg

    @staticmethod
    def __str2hex(s):
        return bytes.fromhex("".join("{:02x}".format(ord(c)) for c in s))

    def __send_command(self, command):
        try:
            s = self.__str2hex(command + "\n")
            self.__serial.send(s, s)
            sleep(0.3)
            response = self.__serial.read()
            print(f"response: {binascii.hexlify(response)}")
            if response:
                response = response.decode("utf-8")
                if response[0] != ACK:
                    if response[1] == ESTS:
                        error_code = binascii.hexlify(chr(ord(response[2])).encode()).decode()
                        print("{}\n".format(self.__get_error_message(error_code)))
                else:
                    print("Astro send command: OK")
                    return response
            else:
                print("Astro send command: NOK")
                return ""
        except Exception as error:
            print(error)

    def __command_parser(self, param, key, pattern):
        try:
            if isinstance(param[key], list):
                for i in param[key]:
                    self.__command_parser({key: i}, key, pattern)
            if key in list(self.__VARIABLES.keys()):
                if key == "pattern" and isinstance(param[key], str):
                    param[key] = list(self.__PATTERNS.values()).index(param[key])
                if key == "multi_pattern" and isinstance(param[key], str):
                    param[key] = (list(self.__PATTERNS.values()).index(param[key]),)
                if key == "multi_pattern" and isinstance(param[key], (list, tuple)):
                    try:
                        param[key] = tuple(
                            [self.__PATTERNS_NAMES[x.upper().replace(" ", "")] for x in param[key]]
                        )
                    except Exception as e:
                        print(f"Parameter or Value error...:{e}")
                        return
                if (
                        key == "multi_pattern" and isinstance(param[key], tuple)
                ) or param[key] in self.__VARIABLES[key][1]:
                    if not isinstance(param[key], tuple):
                        value = str(param[key])
                    else:
                        value = tuple([str(x) for x in param[key]])
                    if self.device_model == "VG-870B":
                        if key == "multi_pattern":
                            value = list(value)
                            if str(self.__PATTERNS_NAMES["CHARACTERPLANE"]) in value:
                                value.remove(str(self.__PATTERNS_NAMES["CHARACTERPLANE"]))
                            if re.findall(
                                    r"BURST|CIRCLE|X|\+|RECTANGLE|DOTS|CROSS|CHARA",
                                    ",".join([self.__PATTERNS[int(x)] for x in value])
                            ) and self.__PATTERNS_NAMES["CHARACTERPLANE"] not in value:
                                value.insert(0, str(self.__PATTERNS_NAMES["CHARACTERPLANE"]))
                            self.__send_command(
                                STX + VG4CMD + SPTS4 + "0" + "\x2C" +
                                "0" + "\x2C" + "1" + "\x2C" + "2" + "\x2C" +
                                "\x2C".join([str(x) for x in value]) + ETX
                            )
                            self.__send_command(STX + VG4CMD + EXBN4 + ETX)
                            print(key+" -> "+", ".join([self.__PATTERNS[int(x)] for x in value]))
                    else:
                        if key == "pattern":
                            if int(value) == 14:
                                pattern_value = "\x69"
                            else:
                                pattern_value = chr(int(value) + ord("\x50"))
                            cmd = STX + PTS + '\x30' + ETX
                            print(f"cmd: {self.__str2hex(cmd)}")
                            data = self.__send_command(cmd)
                            print(f"data: {binascii.hexlify(self.__str2hex(data))}")
                            data1 = STX + TRDT
                            for i in range(2, len(data)):
                                if data[i] == "\x5e" or data[i] == "\x5f" or data[i] == "\x60":
                                    data1 += data[i]
                                elif data[i] == pattern_value:
                                    pattern_value = ETX
                            data1 += pattern_value
                            if pattern_value != ETX:
                                data1 += ETX
                            self.__send_command(data1)
                            print(f"data1: {binascii.hexlify(self.__str2hex(data1))}")
                            print(key + " -> " + self.__PATTERNS[int(value)])
                        if key == "multi_pattern":
                            pattern_values = []
                            for patt in value:
                                pattern_values.append(chr(int(patt) + ord("\x50")))
                                if int(patt) == 11:
                                    pattern_values[-1] = chr(ord(pattern_values[-1]) + ord("\x02"))
                            cmd = STX + PTS + '\x30' + ETX
                            data = self.__send_command(cmd)
                            data1 = STX + TRDT
                            for i in range(2, len(data)):
                                if data[i] == "\x5e" or data[i] == "\x5f" or data[i] == "\x60":
                                    data1 += data[i]
                            data1 += "".join(pattern_values) + ETX
                            cmd = STX + EXPON + ETX
                            self.__send_command(cmd)
                            self.__send_command(data1)
                            print(key+" -> "+", ".join([self.__PATTERNS[int(x)] for x in value]))
                    if key == "program":
                        if self.device_model == "VG-870B":
                            cmd = STX + VG4CMD + '\x24\x20' + value + ETX
                            print(binascii.hexlify(cmd.encode("utf-8")))
                        else:
                            cmd = STX + EXPDN + value + ETX
                        self.__send_command(cmd)
                        print(key + " -> " + value)
                else:
                    print("Parameter or Value error...")
        except Exception as error:
            print(error)

    def sender(self, param):
        try:
            if param.get("program"):
                self.__command_parser(param, "program", r"\d{1,3}")
            if self.device_model == "VG-870B":
                if param.get("pattern") or param.get("multi_pattern"):
                    self.__command_parser(
                        param,
                        "multi_pattern",
                        "|".join([str(x) for x in list(self.__PATTERNS.keys())]) + "|" +
                        "|".join(list(self.__PATTERNS.values()))
                    )
            else:
                if param.get("pattern"):
                    self.__command_parser(
                        param,
                        "pattern",
                        "|".join([str(x) for x in list(self.__PATTERNS.keys())]) +
                        "|" + "|".join(list(self.__PATTERNS.values()))
                    )
                if param.get("multi_pattern"):
                    self.__command_parser(
                        param,
                        "multi_pattern",
                        "|".join([str(x) for x in list(self.multi___PATTERNS.keys())]) + "|" +
                        "|".join(list(self.multi___PATTERNS.values()))
                    )
        except Exception as error:
            print(error)


class SerialDevices:
    def __init__(self):
        self.astro = SerialAstro()
        self.device_list = GetSerialDevices()
        self.uart = UartRW()
