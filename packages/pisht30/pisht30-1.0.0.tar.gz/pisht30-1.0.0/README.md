# Installing

Stable library from PyPi:

* Just run `pip install pisht30`

# PiSht30's Methods

## Constructor(config={})

'config' is dictionary type.

### 'address'

Configure I2C address of SHT30.

* Address.LOW.value
    * I2C address is 0x44
    * Default
* Address.HIGH.value
    * I2C address is 0x45

### 'mode'

Configure measurement mode of SHT30.

* Mode.SINGLE_SHOT_CLOCK_STRETCH_OFF_LOW.value
    * Single Shot Data Acquisition Mode
    * Clock stretching : Disabled
    * Repeatability : Low
    * Default
* Mode.SINGLE_SHOT_CLOCK_STRETCH_OFF_MIDDLE.value
    * Single Shot Data Acquisition Mode
    * Clock stretching : Disabled
    * Repeatability : Middle
* Mode.SINGLE_SHOT_CLOCK_STRETCH_OFF_HIGH.value
    * Single Shot Data Acquisition Mode
    * Clock stretching : Disabled
    * Repeatability : High
* Mode.SINGLE_SHOT_CLOCK_STRETCH_ON_LOW.value
    * Single Shot Data Acquisition Mode
    * Clock stretching : Enabled
    * Repeatability : Low
* Mode.SINGLE_SHOT_CLOCK_STRETCH_ON_MIDDLE.value
    * Single Shot Data Acquisition Mode
    * Clock stretching : Enabled
    * Repeatability : Middle
* Mode.SINGLE_SHOT_CLOCK_STRETCH_ON_HIGH.value
    * Single Shot Data Acquisition Mode
    * Clock stretching : Enabled
    * Repeatability : High
* Mode.PERIODIC_MPS_0_5_LOW.value
    * Periodic Data Acquisition Mode
    * Measurements per second: 0.5
    * Repeatability : Low
* Mode.PERIODIC_MPS_0_5_MIDDLE.value
    * Periodic Data Acquisition Mode
    * Measurements per second: 0.5
    * Repeatability : Middle
* Mode.PERIODIC_MPS_0_5_HIGH.value
    * Periodic Data Acquisition Mode
    * Measurements per second: 0.5
    * Repeatability : High
* Mode.PERIODIC_MPS_1_0_LOW.value
    * Periodic Data Acquisition Mode
    * Measurements per second: 1
    * Repeatability : Low
* Mode.PERIODIC_MPS_1_0_MIDDLE.value
    * Periodic Data Acquisition Mode
    * Measurements per second: 1
    * Repeatability : Middle
* Mode.PERIODIC_MPS_1_0_HIGH.value
    * Periodic Data Acquisition Mode
    * Measurements per second: 1
    * Repeatability : High
* Mode.PERIODIC_MPS_2_0_LOW.value
    * Periodic Data Acquisition Mode
    * Measurements per second: 2
    * Repeatability : Low
* Mode.PERIODIC_MPS_2_0_MIDDLE.value
    * Periodic Data Acquisition Mode
    * Measurements per second: 2
    * Repeatability : Middle
* Mode.PERIODIC_MPS_2_0_HIGH.value
    * Periodic Data Acquisition Mode
    * Measurements per second: 2
    * Repeatability : High
* Mode.PERIODIC_MPS_4_0_LOW.value
    * Periodic Data Acquisition Mode
    * Measurements per second: 4
    * Repeatability : Low
* Mode.PERIODIC_MPS_4_0_MIDDLE.value
    * Periodic Data Acquisition Mode
    * Measurements per second: 4
    * Repeatability : Middle
* Mode.PERIODIC_MPS_4_0_HIGH.value
    * Periodic Data Acquisition Mode
    * Measurements per second: 4
    * Repeatability : High
* Mode.PERIODIC_MPS_10_0_LOW.value
    * Periodic Data Acquisition Mode
    * Measurements per second: 10
    * Repeatability : Low
* Mode.PERIODIC_MPS_10_0_MIDDLE.value
    * Periodic Data Acquisition Mode
    * Measurements per second: 10
    * Repeatability : Middle
* Mode.PERIODIC_MPS_10_0_HIGH.value
    * Periodic Data Acquisition Mode
    * Measurements per second: 10
    * Repeatability : High

## read()

Read temperature and humidity.
Return value is dictionary type.

### 'temperature'

* OK
    * Type: float
    * Celsius temperature value [℃]
* NG
    * Type: False

### 'humidity'

* OK
    * Type: float
    * Relative humidity value [%]
* NG
    * Type: False

# Sample

Run `sudo pigpiod` before running the sample.

## Simple

.. code-block:: shell

    # -*- coding: utf-8 -*-
    import pisht30 as SHT30
    import time
    
    obj = SHT30.PiSht30()
    try:
        while True:
            value = obj.read()
            if (isinstance(value['temperature'], float)):
                print(round(value['temperature'], 2))
            if (isinstance(value['humidity'], float)):
                print(round(value['humidity'], 2))
            time.sleep(10)
    except KeyboardInterrupt:
        pass


## Modify config

'address' is HIGH and 'mode' is PERIODIC_MPS_1_0_HIGH.

.. code-block:: shell

    # -*- coding: utf-8 -*-
    import pisht30 as SHT30
    import time
    
    config = {
        'address' : SHT30.Address.HIGH.value.
        'mode' : SHT30.Mode.PERIODIC_MPS_1_0_HIGH.value
    }
    obj = SHT30.PiSht30(config)
    try:
        while True:
            value = obj.read()
            if (isinstance(value['temperature'], float)):
                print(round(value['temperature'], 2))
            if (isinstance(value['humidity'], float)):
                print(round(value['humidity'], 2))
            time.sleep(10)
    except KeyboardInterrupt:
        pass

