# -*- coding: utf-8 -*-
import pigpio
import time
from enum import Enum

# SHT30の値を扱う処理の詳細はデータシートを参照
ADDRESS_0              = 0x44
ADDRESS_1              = 0x45

READ_COMMAND           = 0x00

MSB_SS_CS_OFF          = 0x24
LSB_SS_CS_OFF_HIGH     = 0x00
LSB_SS_CS_OFF_MIDDLE   = 0x0B
LSB_SS_CS_OFF_LOW      = 0x16
MSB_SS_CS_ON           = 0x2C
LSB_SS_CS_ON_HIGH      = 0x06
LSB_SS_CS_ON_MIDDLE    = 0x0D
LSB_SS_CS_ON_LOW       = 0x10
MSB_PR_MPS_0_5         = 0x20
MSB_PR_MPS_0_5_LOW     = 0x2F
MSB_PR_MPS_0_5_MIDDLE  = 0x24
MSB_PR_MPS_0_5_HIGH    = 0x32
MSB_PR_MPS_1_0         = 0x21
MSB_PR_MPS_1_0_LOW     = 0x2D
MSB_PR_MPS_1_0_MIDDLE  = 0x26
MSB_PR_MPS_1_0_HIGH    = 0x30
MSB_PR_MPS_2_0         = 0x22
MSB_PR_MPS_2_0_LOW     = 0x2B
MSB_PR_MPS_2_0_MIDDLE  = 0x20
MSB_PR_MPS_2_0_HIGH    = 0x36
MSB_PR_MPS_4_0         = 0x23
MSB_PR_MPS_4_0_LOW     = 0x29
MSB_PR_MPS_4_0_MIDDLE  = 0x22
MSB_PR_MPS_4_0_HIGH    = 0x34
MSB_PR_MPS_10_0        = 0x27
MSB_PR_MPS_10_0_LOW    = 0x2A
MSB_PR_MPS_10_0_MIDDLE = 0x21
MSB_PR_MPS_10_0_HIGH   = 0x37

MSB_PR_READ            = 0xE0
LSB_PR_READ            = 0x00
MSB_BREAK              = 0x30
LSB_BREAK              = 0x93

DATA_LENGTH            = 6

class Address(Enum):
    LOW                                  = ADDRESS_0
    HIGH                                 = ADDRESS_1

class Mode(Enum):
    SINGLE_SHOT_CLOCK_STRETCH_OFF_LOW    = 0
    SINGLE_SHOT_CLOCK_STRETCH_OFF_MIDDLE = 1
    SINGLE_SHOT_CLOCK_STRETCH_OFF_HIGH   = 2
    SINGLE_SHOT_CLOCK_STRETCH_ON_LOW     = 3
    SINGLE_SHOT_CLOCK_STRETCH_ON_MIDDLE  = 4
    SINGLE_SHOT_CLOCK_STRETCH_ON_HIGH    = 5
    PERIODIC_MPS_0_5_LOW                 = 6
    PERIODIC_MPS_0_5_MIDDLE              = 7
    PERIODIC_MPS_0_5_HIGH                = 8
    PERIODIC_MPS_1_0_LOW                 = 9
    PERIODIC_MPS_1_0_MIDDLE              = 10
    PERIODIC_MPS_1_0_HIGH                = 11
    PERIODIC_MPS_2_0_LOW                 = 12
    PERIODIC_MPS_2_0_MIDDLE              = 13
    PERIODIC_MPS_2_0_HIGH                = 14
    PERIODIC_MPS_4_0_LOW                 = 15
    PERIODIC_MPS_4_0_MIDDLE              = 16
    PERIODIC_MPS_4_0_HIGH                = 17
    PERIODIC_MPS_10_0_LOW                = 18
    PERIODIC_MPS_10_0_MIDDLE             = 19
    PERIODIC_MPS_10_0_HIGH               = 20

class Command(Enum):
    SINGLE_SHOT_CLOCK_STRETCH_OFF_LOW    = 0
    SINGLE_SHOT_CLOCK_STRETCH_OFF_MIDDLE = 1
    SINGLE_SHOT_CLOCK_STRETCH_OFF_HIGH   = 2
    SINGLE_SHOT_CLOCK_STRETCH_ON_LOW     = 3
    SINGLE_SHOT_CLOCK_STRETCH_ON_MIDDLE  = 4
    SINGLE_SHOT_CLOCK_STRETCH_ON_HIGH    = 5
    PERIODIC_MPS_0_5_LOW                 = 6
    PERIODIC_MPS_0_5_MIDDLE              = 7
    PERIODIC_MPS_0_5_HIGH                = 8
    PERIODIC_MPS_1_0_LOW                 = 9
    PERIODIC_MPS_1_0_MIDDLE              = 10
    PERIODIC_MPS_1_0_HIGH                = 11
    PERIODIC_MPS_2_0_LOW                 = 12
    PERIODIC_MPS_2_0_MIDDLE              = 13
    PERIODIC_MPS_2_0_HIGH                = 14
    PERIODIC_MPS_4_0_LOW                 = 15
    PERIODIC_MPS_4_0_MIDDLE              = 16
    PERIODIC_MPS_4_0_HIGH                = 17
    PERIODIC_MPS_10_0_LOW                = 18
    PERIODIC_MPS_10_0_MIDDLE             = 19
    PERIODIC_MPS_10_0_HIGH               = 20
    PERIODIC_READ                        = 21
    BREAK                                = 12

class Data(Enum):
    TEMP_MSB = 0
    TEMP_LSB = 1
    TEMP_CRC = 2
    HUMI_MSB = 3
    HUMI_LSB = 4
    HUMI_CRC = 5
    
MODE = [
    { 'mode' : Mode.SINGLE_SHOT_CLOCK_STRETCH_OFF_LOW.value,
      'read' : Command.SINGLE_SHOT_CLOCK_STRETCH_OFF_LOW.value },
    { 'mode' : Mode.SINGLE_SHOT_CLOCK_STRETCH_OFF_MIDDLE.value,
      'read' : Command.SINGLE_SHOT_CLOCK_STRETCH_OFF_MIDDLE.value },
    { 'mode' : Mode.SINGLE_SHOT_CLOCK_STRETCH_OFF_HIGH.value,
      'read' : Command.SINGLE_SHOT_CLOCK_STRETCH_OFF_HIGH.value },
    { 'mode' : Mode.SINGLE_SHOT_CLOCK_STRETCH_ON_LOW.value,
      'read' : Command.SINGLE_SHOT_CLOCK_STRETCH_ON_LOW.value },
    { 'mode' : Mode.SINGLE_SHOT_CLOCK_STRETCH_ON_MIDDLE.value,
      'read' : Command.SINGLE_SHOT_CLOCK_STRETCH_ON_MIDDLE.value },
    { 'mode' : Mode.SINGLE_SHOT_CLOCK_STRETCH_ON_HIGH.value,
      'read' : Command.SINGLE_SHOT_CLOCK_STRETCH_ON_HIGH.value },
    { 'mode' : Mode.PERIODIC_MPS_0_5_LOW.value,
      'read' : Command.PERIODIC_READ.value },
    { 'mode' : Mode.PERIODIC_MPS_0_5_MIDDLE.value,
      'read' : Command.PERIODIC_READ.value },
    { 'mode' : Mode.PERIODIC_MPS_0_5_HIGH.value,
      'read' : Command.PERIODIC_READ.value },
    { 'mode' : Mode.PERIODIC_MPS_1_0_LOW.value,
      'read' : Command.PERIODIC_READ.value },
    { 'mode' : Mode.PERIODIC_MPS_1_0_MIDDLE.value,
      'read' : Command.PERIODIC_READ.value },
    { 'mode' : Mode.PERIODIC_MPS_1_0_HIGH.value,
      'read' : Command.PERIODIC_READ.value },
    { 'mode' : Mode.PERIODIC_MPS_2_0_LOW.value,
      'read' : Command.PERIODIC_READ.value },
    { 'mode' : Mode.PERIODIC_MPS_2_0_MIDDLE.value,
      'read' : Command.PERIODIC_READ.value },
    { 'mode' : Mode.PERIODIC_MPS_2_0_HIGH.value,
      'read' : Command.PERIODIC_READ.value },
    { 'mode' : Mode.PERIODIC_MPS_4_0_LOW.value,
      'read' : Command.PERIODIC_READ.value },
    { 'mode' : Mode.PERIODIC_MPS_4_0_MIDDLE.value,
      'read' : Command.PERIODIC_READ.value },
    { 'mode' : Mode.PERIODIC_MPS_4_0_HIGH.value,
      'read' : Command.PERIODIC_READ.value },
    { 'mode' : Mode.PERIODIC_MPS_10_0_LOW.value,
      'read' : Command.PERIODIC_READ.value },
    { 'mode' : Mode.PERIODIC_MPS_10_0_MIDDLE.value,
      'read' : Command.PERIODIC_READ.value },
    { 'mode' : Mode.PERIODIC_MPS_10_0_HIGH.value,
      'read' : Command.PERIODIC_READ.value }
]

COMMANDS = [
    { 'msb' : MSB_SS_CS_OFF, 'lsb' : LSB_SS_CS_OFF_LOW },
    { 'msb' : MSB_SS_CS_OFF, 'lsb' : LSB_SS_CS_OFF_MIDDLE },
    { 'msb' : MSB_SS_CS_OFF, 'lsb' : LSB_SS_CS_OFF_HIGH },
    { 'msb' : MSB_SS_CS_ON, 'lsb' : LSB_SS_CS_ON_LOW },
    { 'msb' : MSB_SS_CS_ON, 'lsb' : LSB_SS_CS_ON_MIDDLE },
    { 'msb' : MSB_SS_CS_ON, 'lsb' : LSB_SS_CS_ON_HIGH },
    { 'msb' : MSB_PR_MPS_0_5, 'lsb' : MSB_PR_MPS_0_5_LOW },
    { 'msb' : MSB_PR_MPS_0_5, 'lsb' : MSB_PR_MPS_0_5_MIDDLE },
    { 'msb' : MSB_PR_MPS_0_5, 'lsb' : MSB_PR_MPS_0_5_HIGH },
    { 'msb' : MSB_PR_MPS_1_0, 'lsb' : MSB_PR_MPS_1_0_LOW },
    { 'msb' : MSB_PR_MPS_1_0, 'lsb' : MSB_PR_MPS_1_0_MIDDLE },
    { 'msb' : MSB_PR_MPS_1_0, 'lsb' : MSB_PR_MPS_1_0_HIGH },
    { 'msb' : MSB_PR_MPS_2_0, 'lsb' : MSB_PR_MPS_2_0_LOW },
    { 'msb' : MSB_PR_MPS_2_0, 'lsb' : MSB_PR_MPS_2_0_MIDDLE },
    { 'msb' : MSB_PR_MPS_2_0, 'lsb' : MSB_PR_MPS_2_0_HIGH },
    { 'msb' : MSB_PR_MPS_4_0, 'lsb' : MSB_PR_MPS_4_0_LOW },
    { 'msb' : MSB_PR_MPS_4_0, 'lsb' : MSB_PR_MPS_4_0_MIDDLE },
    { 'msb' : MSB_PR_MPS_4_0, 'lsb' : MSB_PR_MPS_4_0_HIGH },
    { 'msb' : MSB_PR_MPS_10_0, 'lsb' : MSB_PR_MPS_10_0_LOW },
    { 'msb' : MSB_PR_MPS_10_0, 'lsb' : MSB_PR_MPS_10_0_MIDDLE },
    { 'msb' : MSB_PR_MPS_10_0, 'lsb' : MSB_PR_MPS_10_0_HIGH },
    { 'msb' : MSB_PR_READ, 'lsb' : LSB_PR_READ },
    { 'msb' : MSB_BREAK, 'lsb' : LSB_BREAK }
]

class PiSht30():
    def __init__(self, config={}):
        self.config = {}
        config_i = {
            'address' : Address.LOW.value,
            'mode': Mode.SINGLE_SHOT_CLOCK_STRETCH_OFF_LOW.value
        }
        self.__modify_config(config_i)
        self.__modify_config(config)
        if (self.config['mode'] >= Mode.PERIODIC_MPS_0_5_LOW.value):
            self.__pre_process()
            command = COMMANDS[MODE[self.config['mode']]['mode']]
            self.pi.i2c_write_i2c_block_data(self.sht30, \
                                             command['msb'], \
                                             [command['lsb']])
            self.__post_process()
            
    def __pre_process(self):
        """
        pigpioを初期化してSHT30との接続を初期化する．
        """
        self.pi = pigpio.pi()
        self.sht30 = self.pi.i2c_open(1, self.config['address'])
        if (self.config['mode'] <= Mode.SINGLE_SHOT_CLOCK_STRETCH_ON_HIGH.value):
            self.__break()

    def __post_process(self):
        """
        pigpioを終了してSHT30との接続を切断する．
        """
        self.pi.i2c_close(self.sht30)
        self.pi.stop()

    def __modify_config(self, config={}):
        """
        設定を変更する．
        """
        for key in config.keys():
            if config[key] is not None:
                self.config[key] = config[key]

    def __convert_temperature(self, data):
        """
        SHT30から読み出した温度センサの値からセルシウス度に変換する．
        計算式はSHT30のデータシートを参照．
        
        Parameters
        ----------
        data : list
            センサの値．
        
        Returns
        -------
        temperature : float
            温度[℃]．
        """
        temperature =  ((((data[Data.TEMP_MSB.value] * 256.0) + data[Data.TEMP_LSB.value]) * 175.0)  / 65535.0) - 45.0
        return temperature
    
    def __convert_humidity(self, data):
        """
        SHT30から読み出した湿度センサの値から相対湿度に変換する．
        計算式はSHT30のデータシートを参照．
        
        Parameters
        ----------
        data : list
            センサの値．
        
        Returns
        -------
        humidity : float
            相対湿度[%]．
        """
        humidity = 100.0 * (data[Data.HUMI_MSB.value] * 256.0 + data[Data.HUMI_LSB.value]) / 65535.0 
        return humidity

    def __calc_crc(self, data):
        """
        SHT30から読み出した値に対するCRCを計算する．
        計算式はSHT30のデータシートを参照．
        
        Parameters
        ----------
        data : list
            センサの値．
        
        Returns
        -------
        crc : integer
            CRC．
        """
        crc = 0xFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc <<= 1
                    crc ^= 0x131
                else:
                    crc <<= 1
        return crc

    def __break(self):
        '''
        読込みを停止する．
        '''
        command = COMMANDS[Command.BREAK.value]
        self.pi.i2c_write_i2c_block_data(self.sht30, command['msb'], [command['lsb']])

    def read(self):
        """
        SHT30から気温と相対湿度のデータを読み出す．
        計算式はSHT30のデータシートを参照．
        
        Returns
        -------
        value : dictionary
            {'temperature': 温度, 'humidity': 相対湿度}．
        """
        self.__pre_process()
        # SHT30からセンサの値を格納した各レジスタの値を読み出す
        command = COMMANDS[MODE[self.config['mode']]['read']]
        self.pi.i2c_write_i2c_block_data(self.sht30, \
                                         command['msb'], \
                                         [command['lsb']])
        len, data = self.pi.i2c_read_i2c_block_data(self.sht30, READ_COMMAND, DATA_LENGTH)
        self.__post_process()
        
        if len == DATA_LENGTH:
            # CRCを計算する
            temperature_crc = self.__calc_crc([data[Data.TEMP_MSB.value], 
                                               data[Data.TEMP_LSB.value]])
            humidity_crc = self.__calc_crc([data[Data.HUMI_MSB.value], 
                                            data[Data.HUMI_LSB.value]])

            if temperature_crc == data[Data.TEMP_CRC.value]: 
                # 人間が解る値に変換する
                temperature = self.__convert_temperature(data)
            else:
                temperature = False
            if humidity_crc == data[Data.HUMI_CRC.value]:
                # 人間が解る値に変換する
                humidity    = self.__convert_humidity(data)
            else:
                humidity    = False
        else:
            temperature = False
            humidity    = False
        # 戻り値を整形する
        value = {'temperature': temperature, \
                 'humidity': humidity}
        return value
