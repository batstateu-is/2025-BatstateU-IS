# LPF2 class allows communication between LEGO SPIKE Prime and third party devices.
__author__ = "Anton Vanhoucke & Ste7an"
__copyright__ = "Copyright 2023, 2024 AntonsMindstorms.com"
__license__ = "GPL"
__version__ = "1.5"
__status__ = "Production"

import machine
import struct
import utime
from micropython import const
from sys import implementation

# OpenMV board platform type
# sys.implementation[2]: OPENMV4P-STM32H743
OPENMV = const(0)
# LMS-ESP32 board platform type
# sys.implementation[2]: ESP32 module (lvgl,ulab,spiram) with ESP32
ESP32 = const(1)
# OpenMV RT board platform type
# sys.implementation[2]: OpenMV IMXRT1060-MIMXRT1062DVJ6A
OPENMVRT = const(2)

MAX_PKT = const(32)

BYTE_NACK = const(0x02)
BYTE_ACK = const(0x04)
CMD_Type = const(0x40)  # @, set sensor type command
CMD_Select = const(0x43)  #  C, sets modes on the fly
CMD_MODES = const(0x41)  # I, set mode type command
CMD_EXT_MODE = const(0x46)
CMD_Baud = const(0x52)  # R, set the transmission baud rate
CMD_Vers = const(0x5F)  # _,  set the version number
MSG_INFO = const(0x80)  # name command
MSG_DATA = const(0xC0)  # data command
MSG_EXT_MODE = const(0x46)
EXT_MODE_0 = const(0x00)
EXT_MODE_8 = const(0x08)  # only used for extended mode > 7
CMD_LLL_SHIFT = const(3)
MSG_INFO_PLUS8 = const(0x20)

LEN_4 = const(2 << CMD_LLL_SHIFT)
LEN_2 = const(1 << CMD_LLL_SHIFT)
LEN_8 = const(3 << CMD_LLL_SHIFT)

NAME = const(0x0)
RAW = const(0x1)
PCT = const(0x2)
SI = const(0x3)
SYM = const(0x4)
FUNCTION_MAP = const(0x5)
FMT = const(0x80)

DATA8 = const(0)
DATA16 = const(1)
DATA32 = const(2)
DATAF = const(3)

# Input/Output Mapping flags, can be combined with |
WITH_NULL = const(2**7)  # Supports NULL value
FUNC_2 = const(2**6)  # Supports Functional Mapping 2.0+
ABSOLUTE = const(16)  # ABS (Absolute [min..max])
RELATIVE = const(8)  # REL (Relative [-1..1])
DISCRETE = const(4)  # DIS (Discrete [0, 1, 2, 3])

STRUCT_FMT = ("B", "H", "I", "f")

HEARTBEAT_PERIOD = const(1000)  # time of inactivity after which we reset sensor


def __num_bits(x):
    # Return the number of bits required to represent x
    n = 0
    while x > 0:
        x >>= 1
        n += 1
    return n


class LPF2(object):
    def __init__(
        self,
        modes,
        sensor_id=62,
        debug=False,
        max_packet_size=MAX_PKT,
        rx=None,
        tx=None,
        uart_n=None,
    ):
        self.modes = modes
        self.current_mode = 0
        self.sensor_id = sensor_id
        self.connected = False
        self.payloads = {}
        self.last_nack = 0
        self.debug = debug
        self.max_packet_size = max_packet_size
        self.UART_N = uart_n
        self.TX_PIN_N = tx
        self.RX_PIN_N = rx
        if "RT1060" in implementation[2]:
            self.BOARD = OPENMVRT
            if uart_n == None:
                self.UART_N = 1
            print("OpenMV RT defaults loaded")
        elif "OPENMV4" in implementation[2]:
            self.BOARD = OPENMV
            import pyb
            self.pyb = pyb
            if uart_n == None:
                self.UART_N = 3
            print("OpenMV H7 defaults loaded")
        else:
            self.BOARD = ESP32
            try:
                from lms_esp32 import RX_PIN,TX_PIN
            except ImportError:
                RX_PIN = 18
                TX_PIN = 19
            if tx == None:
                self.TX_PIN_N = TX_PIN
            if rx == None:
                self.RX_PIN_N = RX_PIN
            if uart_n == None:
                self.UART_N = 2
            print(
                "LMS-ESP32 defaults loaded, with rx={}, tx={}".format(self.RX_PIN_N, self.TX_PIN_N)
            )

    @staticmethod
    def mode(
        name,
        size=1,
        data_type=DATA8,
        writable=0,  # Leaving this for bw compatibility
        format="3.0",
        raw_range=[0, 100],
        percent_range=[0, 100],
        si_range=[0, 100],
        symbol="",
        functionmap=[ABSOLUTE, ABSOLUTE],  # [in (to hub), out (from hub)]
        view=True,
    ):
        fig, dec = format.split(".")
        total_data_size = size * 2**data_type  # Byte size of data set.
        # Find the power of 2 that is greater than the length of the data
        # -1 because of the header byte.
        bit_size = __num_bits(total_data_size - 1)
        mode_list = [
            name,  # 0
            [size, data_type, int(fig), int(dec)],  # 1
            raw_range,  # 2
            percent_range,  # 3
            si_range,  # 4
            symbol,  # 5
            functionmap,  # 6
            view and functionmap[0],  # 7
            total_data_size,  # 8
            bit_size,  # 9
        ]
        return mode_list

    def init_pins(self):
        if self.BOARD == ESP32:
            self.rx_pin = machine.Pin(self.RX_PIN_N, machine.Pin.IN)
            self.tx_pin = machine.Pin(
                self.TX_PIN_N, machine.Pin.OUT, machine.Pin.PULL_DOWN
            )
        elif self.BOARD == OPENMVRT:
            self.rx_pin = machine.Pin("P5", machine.Pin.IN)
            self.tx_pin = machine.Pin("P4", machine.Pin.OUT, machine.Pin.PULL_DOWN)
        elif self.BOARD == OPENMV:
            self.rx_pin = self.pyb.Pin("P5", self.pyb.Pin.IN)
            self.tx_pin = self.pyb.Pin("P4", self.pyb.Pin.OUT_PP)

    def wrt_tx_pin(self, val, wait):
        # Reinit pin to deal with cable unplugging and re-plugging
        self.tx_pin.value(val)
        utime.sleep_ms(wait)

    def slow_uart(self):
        if self.BOARD == ESP32:
            self.uart = machine.UART(
                self.UART_N,
                baudrate=2400,
                rx=self.RX_PIN_N,
                tx=self.TX_PIN_N,
            )

        elif self.BOARD == OPENMVRT:
            self.uart = machine.UART(self.UART_N, 2400)

        elif self.BOARD == OPENMV:
            self.uart = self.pyb.UART(self.UART_N, 2400)

    def fast_uart(self):
        if self.BOARD == ESP32:
            self.uart = machine.UART(
                self.UART_N,
                baudrate=115200,
                rx=self.RX_PIN_N,
                tx=self.TX_PIN_N,
            )

        elif self.BOARD == OPENMVRT:
            self.uart = machine.UART(self.UART_N, 115200)
            utime.sleep_ms(5)

        elif self.BOARD == OPENMV:
            self.uart = self.pyb.UART(self.UART_N, 115200)

    # -------- Payload definition

    def load_payload(self, data, mode=None):
        if mode is None:
            mode = self.current_mode
        data_type = self.modes[mode][1][1]
        if isinstance(data, bytes):
            bin_data = data
        elif isinstance(data, bytearray):
            bin_data = data
        elif isinstance(data, list):
            # We have a list of integers. Pack them as bytes.
            bin_data = struct.pack("%d" % len(data) + STRUCT_FMT[data_type], *data)
        elif isinstance(data, float) or isinstance(data, int):
            bin_data = struct.pack(STRUCT_FMT[data_type], data)
        elif isinstance(data, str):
            # String. Convert to bytes of max size.
            bin_data = bytes(data, "UTF-8")[: self.max_packet_size]
        else:
            raise ValueError("Wrong data type: %s" % type(data))

        bytesize = self.modes[mode][8]
        bit = self.modes[mode][9]

        assert len(bin_data) > 0, "Payload is empty"
        assert len(bin_data) <= bytesize, "Wrong payload size"

        payload = bytearray(2**bit + 5)
        payload[0] = MSG_EXT_MODE
        payload[1] = EXT_MODE_0 if mode < 8 else EXT_MODE_8
        payload[2] = 0xFF ^ payload[0] ^ payload[1]
        cksm = 0xFF
        payload[3] = MSG_DATA | (bit << CMD_LLL_SHIFT) | (mode & 7)
        cksm ^= payload[3]
        for i in range(len(bin_data)):
            payload[i + 4] = bin_data[i]
            cksm ^= bin_data[i]
        payload[-1] = cksm  # No need to checksum zero bytes.

        self.payloads[mode] = payload

    def send_payload(self, data=None, mode=None):
        """
        Convert bytes of data to a proper LPF2 payload,
        save it to the payload of the current mode,
        and write it to the hub. If there is no data, just
        send current payload.
        """
        if not self.connected:
            if self.debug:
                print("Write payload, but not connected.")
            return
        if mode == None:
            mode = self.current_mode
        if data != None:
            self.load_payload(data, mode)
        self.write(self.payloads[mode])

    # ----- comm stuff

    def flush(self):
        return self.uart.read(self.uart.any())

    @staticmethod
    def str_b(b):
        return " ".join([hex(c) for c in b])

    def readchar(self):
        if self.uart.any():
            c = self.uart.read(1)
        else: # Try again once
            utime.sleep_ms(1)
            if self.uart.any():
                c = self.uart.read(1)
            else:
                return -1
        if c == None:
            return -1
        else:
            if self.debug:
                print(f"\033[91m {self.str_b(c)}\033[0m", end=" ")
            return ord(c)

    def heartbeat(self):
        if not self.connected:
            print("Checking heartbeat, but not connected. Initializing.")
            self.connect()
            return

        if (utime.ticks_ms() - self.last_nack) > HEARTBEAT_PERIOD:
            print("Checking heartbeat, but line is dead. Re-initializing.")
            self.connected = False
            self.connect()
            return

        b = self.readchar()  # Read in any heartbeat or command bytes
        if b > 0:  # There is data, let's see what it is.
            if b == BYTE_NACK:
                # Regular heartbeat pulse from the hub.
                self.last_nack = utime.ticks_ms()  # reset heartbeat timer
                # Resend latest data, just in case
                self.send_payload()

            elif b == CMD_Select:
                self.last_nack = utime.ticks_ms()  # reset heartbeat timer
                # The hub is asking us to change mode.
                mode = self.readchar()
                cksm = self.readchar()
                # Calculate the checksum for two bytes.
                if cksm == 0xFF ^ CMD_Select ^ mode:
                    self.current_mode = mode
                    self.send_payload()
                    if self.debug:
                        print(f"Mode switched to {mode}")

            elif b == CMD_EXT_MODE:
                self.last_nack = utime.ticks_ms()  # reset heartbeat timer
                ext_mode = self.readchar()  # 0x00 or 0x08
                cksm = self.readchar()  # 0xb9 or 0xb1

                if cksm == 0xFF ^ CMD_EXT_MODE ^ ext_mode:
                    b = self.readchar()  # CMD_Data | LENGTH | MODE

                    # Bitmask and then shift to get the LENGTH (=size exponent) of the data
                    size = 2 ** ((b & 0b111000) >> 3)

                    # Bitmask to get the mode number
                    # TODO test if setting current mode is part of the protocol
                    wrt_mode = (b & 0b111) + ext_mode

                    # Keep track of the checksum while reading data
                    ck = 0xFF ^ b

                    buf = bytearray(size)
                    for i in range(size):
                        buf[i] = self.readchar()
                        # Keep track of the checksum
                        ck ^= buf[i]

                    if ck == self.readchar():
                        return buf, wrt_mode
                    else:
                        print(
                            "Checksum error. Try reducing max_packet_size to 16 if using Pybricks."
                        )
            else:
                if self.debug:
                    buf = self.flush()
                    print(f"Unhandled data from hub {hex(b)} {self.str_b(buf)}")

    def write(self, array):
        if self.debug:
            print("\n>> ", self.str_b(array))
        return self.uart.write(array)

    @staticmethod
    def calc_cksm(array):
        chksm = 0xFF
        for b in array:
            chksm ^= b
        return chksm

    def addChksm(self, array):
        return array + self.calc_cksm(array).to_bytes(1, "little")

    # ---- settup definitions

    def setType(self, sensorType):
        return self.addChksm(bytearray([CMD_Type, sensorType]))

    def defineBaud(self, baud):
        rate = baud.to_bytes(4, "little")
        return self.addChksm(bytearray([CMD_Baud]) + rate)

    @staticmethod
    def str_vers_to_4_bytes(str_vers: str) -> bytes:
        stvb = bytes([int(n)&0xFF for n in str_vers.split(".")])
        if len(stvb) >= 4:
            return stvb[:4]
        return b"\x00" * (4 - len(stvb)) + stvb

    def defineVers(self, hardware: str, software: str):
        return self.addChksm(
            bytearray([CMD_Vers])
            + self.str_vers_to_4_bytes(hardware)
            + self.str_vers_to_4_bytes(software)
        )

    def str_info(self, data, num, info_type):
        if isinstance(data, str):  # Convert and truncate
            dt = bytearray(data, "UTF-8")[: self.max_packet_size]
        else:  # Bytes, or bytearray. Just truncate.
            dt = bytearray(data)[: self.max_packet_size]
        exp = __num_bits(len(dt) - 1)
        pl = bytearray(2**exp)
        pl[: len(dt)] = dt
        return self.addChksm(
            bytearray([MSG_INFO | exp << CMD_LLL_SHIFT | num, info_type]) + pl
        )

    def buildFunctMap(self, fmap, num, info_type):
        return self.addChksm(
            bytearray([MSG_INFO | LEN_2 | num, info_type, fmap[0], fmap[1]])
        )

    def buildFormat(self, fmt, num, info_type):
        sampleSize = fmt[0] & 0xFF
        dataType = fmt[1] & 0xFF
        figures = fmt[2] & 0xFF
        decimals = fmt[3] & 0xFF
        return self.addChksm(
            bytearray(
                [
                    MSG_INFO | LEN_4 | num,
                    info_type,
                    sampleSize,
                    dataType,
                    figures,
                    decimals,
                ]
            )
        )

    def buildRange(self, settings, num, rangeType):
        exp = 3 << CMD_LLL_SHIFT
        minVal = struct.pack("<f", settings[0])
        maxVal = struct.pack("<f", settings[1])
        return self.addChksm(
            bytearray([MSG_INFO | exp | num, rangeType]) + minVal + maxVal
        )

    def defineModes(self):
        n_modes = len(self.modes) - 1
        n_views = [m[7] for m in self.modes].count(True) - 1
        return self.addChksm(
            bytearray(
                [
                    CMD_MODES | LEN_4,
                    min(n_modes, 7),
                    min(n_views, 7),
                    n_modes,
                    n_views,
                ]
            )
        )

    def setupMode(self, mode, num):
        self.load_payload(b"\x00" * mode[8], num)  # Store empty payload for this mode
        plus_8 = 0x00
        if num > 7:
            num -= 8
            plus_8 = MSG_INFO_PLUS8
        self.write(self.str_info(mode[0], num, NAME | plus_8))  # write name
        self.write(self.buildRange(mode[2], num, RAW | plus_8))  # write RAW range
        self.write(self.buildRange(mode[3], num, PCT | plus_8))  # write Percent range
        self.write(self.buildRange(mode[4], num, SI | plus_8))  # write SI range
        self.write(self.str_info(mode[5], num, SYM | plus_8))  # write symbol
        self.write(
            self.buildFunctMap(mode[6], num, FUNCTION_MAP | plus_8)
        )  # write Function Map
        self.write(self.buildFormat(mode[1], num, FMT | plus_8))  # write format

    # -----   Start everything up

    def connect(self):
        fast_uart_hub = False
        self.init_pins()
        self.wrt_tx_pin(1, 5)  # Say hello!
        self.wrt_tx_pin(0, 0)
        for i in range(25):  # Wait for AOK
            n = 0
            while self.rx_pin.value() == 1:
                utime.sleep_ms(1)
                if n > 20:
                    break
                n += 1
            if self.debug:
                print(i, "falling after ms high:", n)
            if i > 10 and (n > 21 or n < 16):
                fast_uart_hub = True
                if self.debug:
                    print("Fast uart handshake after drops: ",n)
                break
            while self.rx_pin.value() == 0:
                utime.sleep_ms(1)
                # Wait until rise again

        if fast_uart_hub:
            self.fast_uart()
            utime.sleep_ms(5)
            self.write(b"\x04")
        else:
            self.slow_uart()
            self.write(b"\x00")
        self.write(self.setType(self.sensor_id))
        self.write(self.defineModes())  # tell how many modes
        self.write(self.defineBaud(115200))
        self.write(self.defineVers("0.1", __version__))
        num = len(self.modes) - 1
        for mode in reversed(self.modes):
            utime.sleep_ms(20)
            self.setupMode(mode, num)
            num -= 1

        self.write(b"\x04")  # ACK
        end = utime.ticks_ms() + 2500
        while utime.ticks_ms() < end:  # Wait for ack
            data = self.readchar()
            if data == BYTE_ACK:
                self.connected = True
                break

        if self.connected:
            self.last_nack = utime.ticks_ms()
            print("\nSuccessfully connected to hub with sensor id {}".format(self.sensor_id))
            if not fast_uart_hub:
                self.fast_uart()
        else:
            print("\nFailed to connect to hub")


