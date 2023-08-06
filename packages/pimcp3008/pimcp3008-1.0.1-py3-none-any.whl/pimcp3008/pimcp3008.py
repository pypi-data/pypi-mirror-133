# -*- coding: utf-8 -*-
import pigpio
import time
from enum import Enum

# MCP3008を扱う処理の詳細はデータシートを参照
ADDRESS_0                          = 0x80
ADDRESS_1                          = 0x90
ADDRESS_2                          = 0xA0
ADDRESS_3                          = 0xB0
ADDRESS_4                          = 0xC0
ADDRESS_5                          = 0xD0
ADDRESS_6                          = 0xE0
ADDRESS_7                          = 0xF0

COMMAND_START                      = 0x01
DATA_DUMMY                         = 0x00
DATA_MAX                           = (2.0 ** 10) - 1

class Device(Enum):
    MCP3008                        = 0
    MCP3004                        = 1

class Channel(Enum):
    CE0                            = 0
    CE1                            = 1
    CE2                            = 2

class FlagMode(Enum):
    MODE0                          = 0
    MODE1                          = 1
    MODE2                          = 2
    MODE3                          = 3

class FlagCeActive(Enum):
    LOW                            = 0
    HIGH                           = 1

class FlagCeGPIO(Enum):
    SPI                            = 0
    OTHER                          = 1

class FlagBusSPI(Enum):
    MAIN                           = 0
    AUXILIARY                      = 1

class Flag3Wire(Enum):
    NOT_3WIRE                      = 0
    USE_3WIRE                      = 1

class FlagBitOrder(Enum):
    BIG                            = 0
    LITTLE                         = 1

FLAG_SPI_MODE_BIT                  = 0
FLAG_CE_ACTIVE_P0_BIT              = 2
FLAG_CE_ACTIVE_P1_BIT              = 3
FLAG_CE_ACTIVE_P2_BIT              = 4
FLAG_CE_GPIO_U0_BIT                = 5
FLAG_CE_GPIO_U1_BIT                = 6
FLAG_CE_GPIO_U2_BIT                = 7
FLAG_BUS_SPI_BIT                   = 8
FLAG_MAIN_3WIRE_BIT                = 9
FLAG_MAIN_BEFORE_WRITE_BIT         = 10
FLAG_AUXILIARY_WRITE_BIT_ORDER_BIT = 14
FLAG_AUXILIARY_READ_BIT_ORDER_BIT  = 15
FLAG_AUXILIARY_WORD_SIZE_BIT       = 16

CLOCK_1M = 1000000
DEFAULT_FLAG = 0

ADDRESS = [
    ADDRESS_0,
    ADDRESS_1,
    ADDRESS_2,
    ADDRESS_3,
    ADDRESS_4,
    ADDRESS_5,
    ADDRESS_6,
    ADDRESS_7
]

MAX_CHANNELS = [
    8,
    4
]

class PiMcp3008():
    def __init__(self, config={}):
        self.config = {}
        config_i = {
            'device' : Device.MCP3008.value,
            'channel' : Channel.CE0.value,
            'clock' : CLOCK_1M,
            'spi_mode' : FlagMode.MODE0.value,
            'spi_bus' : FlagBusSPI.MAIN.value,
            'ce0_active' : FlagCeActive.LOW.value,
            'ce1_active' : FlagCeActive.LOW.value,
            'ce2_active' : FlagCeActive.LOW.value,
            'ce0_gpio' : FlagCeGPIO.SPI.value,
            'ce1_gpio' : FlagCeGPIO.SPI.value,
            'ce2_gpio' : FlagCeGPIO.SPI.value,
            'main_3wire' : Flag3Wire.NOT_3WIRE.value,
            'main_before_write_byte' : 0,
            'auxiliary_write_bit_order' : FlagBitOrder.BIG.value,
            'auxiliary_read_bit_order' : FlagBitOrder.BIG.value,
            'auxiliary_word_size' : 0 # 8bit
        }
        self.__modify_config(config_i)
        self.__modify_config(config)

    def __modify_config(self, config={}):
        """
        設定を変更する．
        """
        for key in config.keys():
            if config[key] is not None:
                self.config[key] = config[key]
        
        if (self.config['spi_bus'] == FlagBusSPI.MAIN.value):
            self.config['ce2_active'] = FlagCeActive.LOW.value
            self.config['ce2_gpio'] = FlagCeGPIO.SPI.value
            self.config['auxiliary_write_bit_order'] = FlagBitOrder.BIG.value
            self.config['auxiliary_read_bit_order'] = FlagBitOrder.BIG.value
            self.config['auxiliary_word_size'] = 0
        else:
            self.config['main_3wire'] = Flag3Wire.NOT_3WIRE.value
            self.config['main_before_write_byte'] = 0
        
        self.config['flag'] = ((self.config['spi_mode'] & 0x03) << FLAG_SPI_MODE_BIT) | \
                              ((self.config['ce0_active'] & 0x01) << FLAG_CE_ACTIVE_P0_BIT) | \
                              ((self.config['ce1_active'] & 0x01) << FLAG_CE_ACTIVE_P1_BIT) | \
                              ((self.config['ce2_active'] & 0x01) << FLAG_CE_ACTIVE_P2_BIT) | \
                              ((self.config['ce0_gpio'] & 0x01) << FLAG_CE_GPIO_U0_BIT) | \
                              ((self.config['ce1_gpio'] & 0x01) << FLAG_CE_GPIO_U1_BIT) | \
                              ((self.config['ce2_gpio'] & 0x01) << FLAG_CE_GPIO_U2_BIT) | \
                              ((self.config['spi_bus'] & 0x01) << FLAG_BUS_SPI_BIT) | \
                              ((self.config['main_3wire'] & 0x01) << FLAG_MAIN_3WIRE_BIT) | \
                              ((self.config['main_before_write_byte'] & 0x0F) << FLAG_MAIN_BEFORE_WRITE_BIT) | \
                              ((self.config['auxiliary_write_bit_order'] & 0x01) << FLAG_AUXILIARY_WRITE_BIT_ORDER_BIT) | \
                              ((self.config['auxiliary_read_bit_order'] & 0x01) << FLAG_AUXILIARY_READ_BIT_ORDER_BIT) | \
                              ((self.config['auxiliary_word_size'] & 0x3F) << FLAG_AUXILIARY_WORD_SIZE_BIT)

    def read(self, *channels):
        """
        MCP3008から指定したチャネルに入力される電圧を読み出す．
        MCP3008の使い方はデータシートを参照．
        
        Parameters
        ----------
        channels : unsigned int
            MCP3008のチャネル．
            指定がない場合はすべてのチャネル．
        
        Returns
        -------
        value : dictionary
            {0-7: A/D変換値, ...}．
        """
        # チャネルの解析
        channels_r = []
        if (not channels):
            channels_r = list(range(MAX_CHANNELS[self.config['device']]))
        else:
            for i in channels:
                if (isinstance(i, int) and i >= 0 and i < MAX_CHANNELS[self.config['device']]):
                    channels_r.append(i)
            channels_r = list(set(channels_r))
            if (not channels_r):
                return {}

        # SPIから値を読み出す
        pi = pigpio.pi()
        spi = pi.spi_open(self.config['channel'], self.config['clock'], self.config['flag'])
        value = {}
        for ch in channels_r:
            len, data = pi.spi_xfer(spi, [COMMAND_START, ADDRESS[ch], DATA_DUMMY])
            data = ((data[1] & 0x03) << 8) | data[2]
            value[ch] = data
        pi.spi_close(spi)
        pi.stop()
        return value
