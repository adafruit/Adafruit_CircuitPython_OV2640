# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_ov2640`
================================================================================

CircuitPython driver for OV2640 Camera.


* Author(s): Jeff Epler

Implementation Notes
--------------------

**Hardware:**

* `ESP32-S2 Kaluga Dev Kit featuring ESP32-S2 WROVER <https://www.adafruit.com/product/4729>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

* Adafruit's Bus Device library: https:# github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

# pylint: disable=too-many-lines
# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_OV7670.git"

import time

import digitalio
import imagecapture
import pwmio
from adafruit_bus_device.i2c_device import I2CDevice

from micropython import const

CTRLI = const(0x50)
_R_BYPASS = const(0x05)
_QS = const(0x44)
_CTRLI = const(0x50)
_HSIZE = const(0x51)
_VSIZE = const(0x52)
_XOFFL = const(0x53)
_YOFFL = const(0x54)
_VHYX = const(0x55)
_DPRP = const(0x56)
_TEST = const(0x57)
_ZMOW = const(0x5A)
_ZMOH = const(0x5B)
_ZMHH = const(0x5C)
_BPADDR = const(0x7C)
_BPDATA = const(0x7D)
_CTRL2 = const(0x86)
_CTRL3 = const(0x87)
_SIZEL = const(0x8C)
_HSIZE8 = const(0xC0)
_VSIZE8 = const(0xC1)
_CTRL0 = const(0xC2)
_CTRL1 = const(0xC3)
_R_DVP_SP = const(0xD3)
_IMAGE_MODE = const(0xDA)
_RESET = const(0xE0)
_MS_SP = const(0xF0)
_SS_ID = const(0xF7)
_SS_CTRL = const(0xF7)
_MC_BIST = const(0xF9)
_MC_AL = const(0xFA)
_MC_AH = const(0xFB)
_MC_D = const(0xFC)
_P_CMD = const(0xFD)
_P_STATUS = const(0xFE)
_BANK_SEL = const(0xFF)

_CTRLI_LP_DP = const(0x80)
_CTRLI_ROUND = const(0x40)

_CTRL0_AEC_EN = const(0x80)
_CTRL0_AEC_SEL = const(0x40)
_CTRL0_STAT_SEL = const(0x20)
_CTRL0_VFIRST = const(0x10)
_CTRL0_YUV422 = const(0x08)
_CTRL0_YUV_EN = const(0x04)
_CTRL0_RGB_EN = const(0x02)
_CTRL0_RAW_EN = const(0x01)

_CTRL2_DCW_EN = const(0x20)
_CTRL2_SDE_EN = const(0x10)
_CTRL2_UV_ADJ_EN = const(0x08)
_CTRL2_UV_AVG_EN = const(0x04)
_CTRL2_CMX_EN = const(0x01)

_CTRL3_BPC_EN = const(0x80)
_CTRL3_WPC_EN = const(0x40)

_R_DVP_SP_AUTO_MODE = const(0x80)

_R_BYPASS_DSP_EN = const(0x00)
_R_BYPASS_DSP_BYPAS = const(0x01)

OV2640_COLOR_RGB = 0
OV2640_COLOR_YUV = 1
OV2640_COLOR_JPEG = 2

_IMAGE_MODE_Y8_DVP_EN = const(0x40)
_IMAGE_MODE_JPEG_EN = const(0x10)
_IMAGE_MODE_YUV422 = const(0x00)
_IMAGE_MODE_RAW10 = const(0x04)
_IMAGE_MODE_RGB565 = const(0x08)
_IMAGE_MODE_HREF_VSYNC = const(0x02)
_IMAGE_MODE_LBYTE_FIRST = const(0x01)

_RESET_MICROC = const(0x40)
_RESET_SCCB = const(0x20)
_RESET_JPEG = const(0x10)
_RESET_DVP = const(0x04)
_RESET_IPU = const(0x02)
_RESET_CIF = const(0x01)

_MC_BIST_RESET = const(0x80)
_MC_BIST_BOOT_ROM_SEL = const(0x40)
_MC_BIST_12KB_SEL = const(0x20)
_MC_BIST_12KB_MASK = const(0x30)
_MC_BIST_512KB_SEL = const(0x08)
_MC_BIST_512KB_MASK = const(0x0C)
_MC_BIST_BUSY_BIT_R = const(0x02)
_MC_BIST_MC_RES_ONE_SH_W = const(0x02)
_MC_BIST_LAUNCH = const(0x01)


_BANK_DSP = const(0)
_BANK_SENSOR = const(1)

# Sensor register bank FF=0x01
_GAIN = const(0x00)
_COM1 = const(0x03)
_REG04 = const(0x04)
_REG08 = const(0x08)
_COM2 = const(0x09)
_REG_PID = const(0x0A)
_REG_VER = const(0x0B)
_COM3 = const(0x0C)
_COM4 = const(0x0D)
_AEC = const(0x10)
_CLKRC = const(0x11)
_COM7 = const(0x12)
_COM8 = const(0x13)
_COM9 = const(0x14)  # AGC gain ceiling
_COM10 = const(0x15)
_HSTART = const(0x17)
_HSTOP = const(0x18)
_VSTART = const(0x19)
_VSTOP = const(0x1A)
_MIDH = const(0x1C)
_MIDL = const(0x1D)
_AEW = const(0x24)
_AEB = const(0x25)
_VV = const(0x26)
_REG2A = const(0x2A)
_FRARL = const(0x2B)
_ADDVSL = const(0x2D)
_ADDVSH = const(0x2E)
_YAVG = const(0x2F)
_HSDY = const(0x30)
_HEDY = const(0x31)
_REG32 = const(0x32)
_ARCOM2 = const(0x34)
_REG45 = const(0x45)
_FLL = const(0x46)
_FLH = const(0x47)
_COM19 = const(0x48)
_ZOOMS = const(0x49)
_COM22 = const(0x4B)
_COM25 = const(0x4E)
_BD50 = const(0x4F)
_BD60 = const(0x50)
_REG5D = const(0x5D)
_REG5E = const(0x5E)
_REG5F = const(0x5F)
_REG60 = const(0x60)
_HISTO_LOW = const(0x61)
_HISTO_HIGH = const(0x62)

_REG04_DEFAULT = const(0x28)
_REG04_HFLIP_IMG = const(0x80)
_REG04_VFLIP_IMG = const(0x40)
_REG04_VREF_EN = const(0x10)
_REG04_HREF_EN = const(0x08)
_REG04_SET = lambda x: (_REG04_DEFAULT | x)

_COM2_STDBY = const(0x10)
_COM2_OUT_DRIVE_1x = const(0x00)
_COM2_OUT_DRIVE_2x = const(0x01)
_COM2_OUT_DRIVE_3x = const(0x02)
_COM2_OUT_DRIVE_4x = const(0x03)

_COM3_DEFAULT = const(0x38)
_COM3_BAND_50Hz = const(0x04)
_COM3_BAND_60Hz = const(0x00)
_COM3_BAND_AUTO = const(0x02)
_COM3_BAND_SET = lambda x: (_COM3_DEFAULT | x)

_COM7_SRST = const(0x80)
_COM7_RES_UXGA = const(0x00)  # UXGA
_COM7_RES_SVGA = const(0x40)  # SVGA
_COM7_RES_CIF = const(0x20)  # CIF
_COM7_ZOOM_EN = const(0x04)  # Enable Zoom
_COM7_COLOR_BAR = const(0x02)  # Enable Color Bar Test

_COM8_DEFAULT = const(0xC0)
_COM8_BNDF_EN = const(0x20)  # Enable Banding filter
_COM8_AGC_EN = const(0x04)  # AGC Auto/Manual control selection
_COM8_AEC_EN = const(0x01)  # Auto/Manual Exposure control
_COM8_SET = lambda x: (_COM8_DEFAULT | x)

_COM9_DEFAULT = const(0x08)
_COM9_AGC_GAIN_2x = const(0x00)  # AGC:    2x
_COM9_AGC_GAIN_4x = const(0x01)  # AGC:    4x
_COM9_AGC_GAIN_8x = const(0x02)  # AGC:    8x
_COM9_AGC_GAIN_16x = const(0x03)  # AGC:   16x
_COM9_AGC_GAIN_32x = const(0x04)  # AGC:   32x
_COM9_AGC_GAIN_64x = const(0x05)  # AGC:   64x
_COM9_AGC_GAIN_128x = const(0x06)  # AGC:  128x
_COM9_AGC_SET = lambda x: (_COM9_DEFAULT | (x << 5))

_COM10_HREF_EN = const(0x80)  # HSYNC changes to HREF
_COM10_HSYNC_EN = const(0x40)  # HREF changes to HSYNC
_COM10_PCLK_FREE = const(0x20)  # PCLK output option: free running PCLK
_COM10_PCLK_EDGE = const(0x10)  # Data is updated at the rising edge of PCLK
_COM10_HREF_NEG = const(0x08)  # HREF negative
_COM10_VSYNC_NEG = const(0x02)  # VSYNC negative
_COM10_HSYNC_NEG = const(0x01)  # HSYNC negative

_CTRL1_AWB = const(0x08)  # Enable AWB

_VV_AGC_TH_SET = lambda h, l: ((h << 4) | (l & 0x0F))

_REG32_UXGA = const(0x36)
_REG32_SVGA = const(0x09)
_REG32_CIF = const(0x89)

_CLKRC_2X = const(0x80)
_CLKRC_2X_UXGA = const(0x01 | _CLKRC_2X)
_CLKRC_2X_SVGA = _CLKRC_2X
_CLKRC_2X_CIF = _CLKRC_2X

_OV2640_MODE_CIF = const(0)
_OV2640_MODE_SVGA = const(1)
_OV2640_MODE_UXGA = const(2)

OV2640_SIZE_96X96 = 0  # 96x96
OV2640_SIZE_QQVGA = 1  # 160x120
OV2640_SIZE_QCIF = 2  # 176x144
OV2640_SIZE_HQVGA = 3  # 240x176
OV2640_SIZE_240X240 = 4  # 240x240
OV2640_SIZE_QVGA = 5  # 320x240
OV2640_SIZE_CIF = 6  # 400x296
OV2640_SIZE_HVGA = 7  # 480x320
OV2640_SIZE_VGA = 8  # 640x480
OV2640_SIZE_SVGA = 9  # 800x600
OV2640_SIZE_XGA = 10  # 1024x768
OV2640_SIZE_HD = 11  # 1280x720
OV2640_SIZE_SXGA = 12  # 1280x1024
OV2640_SIZE_UXGA = 13  # 1600x1200

_ASPECT_RATIO_4X3 = const(0)
_ASPECT_RATIO_3X2 = const(1)
_ASPECT_RATIO_16X10 = const(2)
_ASPECT_RATIO_5X3 = const(3)
_ASPECT_RATIO_16X9 = const(4)
_ASPECT_RATIO_21X9 = const(5)
_ASPECT_RATIO_5X4 = const(6)
_ASPECT_RATIO_1X1 = const(7)
_ASPECT_RATIO_9X16 = const(8)

_resolution_info = [
    [96, 96, _ASPECT_RATIO_1X1],  # 96x96
    [160, 120, _ASPECT_RATIO_4X3],  # QQVGA
    [176, 144, _ASPECT_RATIO_5X4],  # QCIF
    [240, 176, _ASPECT_RATIO_4X3],  # HQVGA
    [240, 240, _ASPECT_RATIO_1X1],  # 240x240
    [320, 240, _ASPECT_RATIO_4X3],  # QVGA
    [400, 296, _ASPECT_RATIO_4X3],  # CIF
    [480, 320, _ASPECT_RATIO_3X2],  # HVGA
    [640, 480, _ASPECT_RATIO_4X3],  # VGA
    [800, 600, _ASPECT_RATIO_4X3],  # SVGA
    [1024, 768, _ASPECT_RATIO_4X3],  # XGA
    [1280, 720, _ASPECT_RATIO_16X9],  # HD
    [1280, 1024, _ASPECT_RATIO_5X4],  # SXGA
    [1600, 1200, _ASPECT_RATIO_4X3],  # UXGA
]

_ratio_table = [
    # ox,  oy,   mx,   my
    [0, 0, 1600, 1200],  # 4x3
    [8, 72, 1584, 1056],  # 3x2
    [0, 100, 1600, 1000],  # 16x10
    [0, 120, 1600, 960],  # 5x3
    [0, 150, 1600, 900],  # 16x9
    [2, 258, 1596, 684],  # 21x9
    [50, 0, 1500, 1200],  # 5x4
    [200, 0, 1200, 1200],  # 1x1
    [462, 0, 676, 1200],  # 9x16
]

# 30fps@24MHz
_ov2640_settings_cif = bytes(
    [
        _BANK_SEL,
        _BANK_DSP,
        0x2C,
        0xFF,
        0x2E,
        0xDF,
        _BANK_SEL,
        _BANK_SENSOR,
        0x3C,
        0x32,
        _CLKRC,
        0x01,
        _COM2,
        _COM2_OUT_DRIVE_3x,
        _REG04,
        _REG04_DEFAULT,
        _COM8,
        _COM8_DEFAULT | _COM8_BNDF_EN | _COM8_AGC_EN | _COM8_AEC_EN,
        _COM9,
        _COM9_AGC_SET(_COM9_AGC_GAIN_8x),
        0x2C,
        0x0C,
        0x33,
        0x78,
        0x3A,
        0x33,
        0x3B,
        0xFB,
        0x3E,
        0x00,
        0x43,
        0x11,
        0x16,
        0x10,
        0x39,
        0x92,
        0x35,
        0xDA,
        0x22,
        0x1A,
        0x37,
        0xC3,
        0x23,
        0x00,
        _ARCOM2,
        0xC0,
        0x06,
        0x88,
        0x07,
        0xC0,
        _COM4,
        0x87,
        0x0E,
        0x41,
        0x4C,
        0x00,
        0x4A,
        0x81,
        0x21,
        0x99,
        _AEW,
        0x40,
        _AEB,
        0x38,
        _VV,
        _VV_AGC_TH_SET(8, 2),
        0x5C,
        0x00,
        0x63,
        0x00,
        _HISTO_LOW,
        0x70,
        _HISTO_HIGH,
        0x80,
        0x7C,
        0x05,
        0x20,
        0x80,
        0x28,
        0x30,
        0x6C,
        0x00,
        0x6D,
        0x80,
        0x6E,
        0x00,
        0x70,
        0x02,
        0x71,
        0x94,
        0x73,
        0xC1,
        0x3D,
        0x34,
        0x5A,
        0x57,
        _BD50,
        0xBB,
        _BD60,
        0x9C,
        _COM7,
        _COM7_RES_CIF,
        _HSTART,
        0x11,
        _HSTOP,
        0x43,
        _VSTART,
        0x00,
        _VSTOP,
        0x25,
        _REG32,
        0x89,
        0x37,
        0xC0,
        _BD50,
        0xCA,
        _BD60,
        0xA8,
        0x6D,
        0x00,
        0x3D,
        0x38,
        _BANK_SEL,
        _BANK_DSP,
        0xE5,
        0x7F,
        _MC_BIST,
        _MC_BIST_RESET | _MC_BIST_BOOT_ROM_SEL,
        0x41,
        0x24,
        _RESET,
        _RESET_JPEG | _RESET_DVP,
        0x76,
        0xFF,
        0x33,
        0xA0,
        0x42,
        0x20,
        0x43,
        0x18,
        0x4C,
        0x00,
        _CTRL3,
        _CTRL3_WPC_EN | 0x10,
        0x88,
        0x3F,
        0xD7,
        0x03,
        0xD9,
        0x10,
        _R_DVP_SP,
        _R_DVP_SP_AUTO_MODE | 0x02,
        0xC8,
        0x08,
        0xC9,
        0x80,
        _BPADDR,
        0x00,
        _BPDATA,
        0x00,
        _BPADDR,
        0x03,
        _BPDATA,
        0x48,
        _BPDATA,
        0x48,
        _BPADDR,
        0x08,
        _BPDATA,
        0x20,
        _BPDATA,
        0x10,
        _BPDATA,
        0x0E,
        0x90,
        0x00,
        0x91,
        0x0E,
        0x91,
        0x1A,
        0x91,
        0x31,
        0x91,
        0x5A,
        0x91,
        0x69,
        0x91,
        0x75,
        0x91,
        0x7E,
        0x91,
        0x88,
        0x91,
        0x8F,
        0x91,
        0x96,
        0x91,
        0xA3,
        0x91,
        0xAF,
        0x91,
        0xC4,
        0x91,
        0xD7,
        0x91,
        0xE8,
        0x91,
        0x20,
        0x92,
        0x00,
        0x93,
        0x06,
        0x93,
        0xE3,
        0x93,
        0x05,
        0x93,
        0x05,
        0x93,
        0x00,
        0x93,
        0x04,
        0x93,
        0x00,
        0x93,
        0x00,
        0x93,
        0x00,
        0x93,
        0x00,
        0x93,
        0x00,
        0x93,
        0x00,
        0x93,
        0x00,
        0x96,
        0x00,
        0x97,
        0x08,
        0x97,
        0x19,
        0x97,
        0x02,
        0x97,
        0x0C,
        0x97,
        0x24,
        0x97,
        0x30,
        0x97,
        0x28,
        0x97,
        0x26,
        0x97,
        0x02,
        0x97,
        0x98,
        0x97,
        0x80,
        0x97,
        0x00,
        0x97,
        0x00,
        0xA4,
        0x00,
        0xA8,
        0x00,
        0xC5,
        0x11,
        0xC6,
        0x51,
        0xBF,
        0x80,
        0xC7,
        0x10,
        0xB6,
        0x66,
        0xB8,
        0xA5,
        0xB7,
        0x64,
        0xB9,
        0x7C,
        0xB3,
        0xAF,
        0xB4,
        0x97,
        0xB5,
        0xFF,
        0xB0,
        0xC5,
        0xB1,
        0x94,
        0xB2,
        0x0F,
        0xC4,
        0x5C,
        _CTRL1,
        0xFD,
        0x7F,
        0x00,
        0xE5,
        0x1F,
        0xE1,
        0x67,
        0xDD,
        0x7F,
        _IMAGE_MODE,
        0x00,
        _RESET,
        0x00,
        _R_BYPASS,
        _R_BYPASS_DSP_EN,
    ]
)

_ov2640_settings_to_cif = bytes(
    [
        _BANK_SEL,
        _BANK_SENSOR,
        _COM7,
        _COM7_RES_CIF,
        # Set the sensor output window
        _COM1,
        0x0A,
        _REG32,
        _REG32_CIF,
        _HSTART,
        0x11,
        _HSTOP,
        0x43,
        _VSTART,
        0x00,
        _VSTOP,
        0x25,
        # _CLKRC, 0x00,
        _BD50,
        0xCA,
        _BD60,
        0xA8,
        0x5A,
        0x23,
        0x6D,
        0x00,
        0x3D,
        0x38,
        0x39,
        0x92,
        0x35,
        0xDA,
        0x22,
        0x1A,
        0x37,
        0xC3,
        0x23,
        0x00,
        _ARCOM2,
        0xC0,
        0x06,
        0x88,
        0x07,
        0xC0,
        _COM4,
        0x87,
        0x0E,
        0x41,
        0x4C,
        0x00,
        _BANK_SEL,
        _BANK_DSP,
        _RESET,
        _RESET_DVP,
        # Set the sensor resolution (UXGA, SVGA, CIF)
        _HSIZE8,
        0x32,
        _VSIZE8,
        0x25,
        _SIZEL,
        0x00,
        # Set the image window size >= output size
        _HSIZE,
        0x64,
        _VSIZE,
        0x4A,
        _XOFFL,
        0x00,
        _YOFFL,
        0x00,
        _VHYX,
        0x00,
        _TEST,
        0x00,
        _CTRL2,
        _CTRL2_DCW_EN | 0x1D,
        _CTRLI,
        _CTRLI_LP_DP | 0x00,
        # _R_DVP_SP, 0x08,
    ]
)

_ov2640_settings_to_svga = bytes(
    [
        _BANK_SEL,
        _BANK_SENSOR,
        _COM7,
        _COM7_RES_SVGA,
        # Set the sensor output window
        _COM1,
        0x0A,
        _REG32,
        _REG32_SVGA,
        _HSTART,
        0x11,
        _HSTOP,
        0x43,
        _VSTART,
        0x00,
        _VSTOP,
        0x4B,
        # _CLKRC, 0x00,
        0x37,
        0xC0,
        _BD50,
        0xCA,
        _BD60,
        0xA8,
        0x5A,
        0x23,
        0x6D,
        0x00,
        0x3D,
        0x38,
        0x39,
        0x92,
        0x35,
        0xDA,
        0x22,
        0x1A,
        0x37,
        0xC3,
        0x23,
        0x00,
        _ARCOM2,
        0xC0,
        0x06,
        0x88,
        0x07,
        0xC0,
        _COM4,
        0x87,
        0x0E,
        0x41,
        0x42,
        0x03,
        0x4C,
        0x00,
        _BANK_SEL,
        _BANK_DSP,
        _RESET,
        _RESET_DVP,
        # Set the sensor resolution (UXGA, SVGA, CIF)
        _HSIZE8,
        0x64,
        _VSIZE8,
        0x4B,
        _SIZEL,
        0x00,
        # Set the image window size >= output size
        _HSIZE,
        0xC8,
        _VSIZE,
        0x96,
        _XOFFL,
        0x00,
        _YOFFL,
        0x00,
        _VHYX,
        0x00,
        _TEST,
        0x00,
        _CTRL2,
        _CTRL2_DCW_EN | 0x1D,
        _CTRLI,
        _CTRLI_LP_DP | 0x00,
        # _R_DVP_SP, 0x08,
    ]
)

_ov2640_settings_to_uxga = bytes(
    [
        _BANK_SEL,
        _BANK_SENSOR,
        _COM7,
        _COM7_RES_UXGA,
        # Set the sensor output window
        _COM1,
        0x0F,
        _REG32,
        _REG32_UXGA,
        _HSTART,
        0x11,
        _HSTOP,
        0x75,
        _VSTART,
        0x01,
        _VSTOP,
        0x97,
        # _CLKRC, 0x00,
        0x3D,
        0x34,
        _BD50,
        0xBB,
        _BD60,
        0x9C,
        0x5A,
        0x57,
        0x6D,
        0x80,
        0x39,
        0x82,
        0x23,
        0x00,
        0x07,
        0xC0,
        0x4C,
        0x00,
        0x35,
        0x88,
        0x22,
        0x0A,
        0x37,
        0x40,
        _ARCOM2,
        0xA0,
        0x06,
        0x02,
        _COM4,
        0xB7,
        0x0E,
        0x01,
        0x42,
        0x83,
        _BANK_SEL,
        _BANK_DSP,
        _RESET,
        _RESET_DVP,
        # Set the sensor resolution (UXGA, SVGA, CIF)
        _HSIZE8,
        0xC8,
        _VSIZE8,
        0x96,
        _SIZEL,
        0x00,
        # Set the image window size >= output size
        _HSIZE,
        0x90,
        _VSIZE,
        0x2C,
        _XOFFL,
        0x00,
        _YOFFL,
        0x00,
        _VHYX,
        0x88,
        _TEST,
        0x00,
        _CTRL2,
        _CTRL2_DCW_EN | 0x1D,
        _CTRLI,
        0x00,
        # _R_DVP_SP, 0x06,
    ]
)

_ov2640_color_settings = {
    OV2640_COLOR_JPEG: bytes(
        [
            _BANK_SEL,
            _BANK_DSP,
            _RESET,
            _RESET_JPEG | _RESET_DVP,
            _IMAGE_MODE,
            _IMAGE_MODE_JPEG_EN | _IMAGE_MODE_HREF_VSYNC,
            0xD7,
            0x03,
            0xE1,
            0x77,
            0xE5,
            0x1F,
            0xD9,
            0x10,
            0xDF,
            0x80,
            0x33,
            0x80,
            0x3C,
            0x10,
            0xEB,
            0x30,
            0xDD,
            0x7F,
            _RESET,
            0x00,
        ]
    ),
    OV2640_COLOR_YUV: bytes(
        [
            _BANK_SEL,
            _BANK_DSP,
            _RESET,
            _RESET_DVP,
            _IMAGE_MODE,
            _IMAGE_MODE_YUV422,
            0xD7,
            0x01,
            0xE1,
            0x67,
            _RESET,
            0x00,
        ]
    ),
    OV2640_COLOR_RGB: bytes(
        [
            _BANK_SEL,
            _BANK_DSP,
            _RESET,
            _RESET_DVP,
            _IMAGE_MODE,
            _IMAGE_MODE_RGB565,
            0xD7,
            0x03,
            0xE1,
            0x77,
            _RESET,
            0x00,
        ]
    ),
}


class _RegBits:
    def __init__(self, bank, reg, shift, mask):
        self.bank = bank
        self.reg = reg
        self.shift = shift
        self.mask = mask

    def __get__(self, obj, objtype=None):
        reg_value = obj._read_bank_register(self.bank, self.reg)
        return (reg_value >> self.shift) & self.mask

    def __set__(self, obj, value):
        if value & ~self.mask:
            raise ValueError(
                f"Value 0x{value:02x} does not fit in mask 0x{self.mask:02x}"
            )
        reg_value = obj._read_bank_register(self.bank, self.reg)
        reg_value &= ~(self.mask << self.shift)
        reg_value |= value << self.shift
        obj._write_register(self.reg, reg_value)


class _SCCBCameraBase:  # pylint: disable=too-few-public-methods
    def __init__(self, i2c_bus, i2c_address):
        self._i2c_device = I2CDevice(i2c_bus, i2c_address)
        self._bank = None

    def _get_reg_bits(self, bank, reg, shift, mask):
        return (self._read_bank_register(bank, reg) >> shift) & mask

    def _set_reg_bits(
        self, bank, reg, shift, mask, value
    ):  #  pylint: disable=too-many-arguments
        reg_value = self._read_bank_register(bank, reg)
        reg_value &= ~(mask << shift)
        reg_value |= value << shift
        self._write_register(reg, reg_value)

    def _write_list(self, reg_list):
        for i in range(0, len(reg_list), 2):
            self._write_register(reg_list[i], reg_list[i + 1])
            time.sleep(0.001)

    def _write_bank_register(self, bank, reg, value):
        if self._bank != bank:
            self._write_register(_BANK_SEL, bank)
        self._write_register(reg, value)

    def _read_bank_register(self, bank, reg):
        if self._bank != bank:
            self._write_register(_BANK_SEL, bank)
        result = self._read_register(reg)
        return result

    def _write_register(self, reg, value):
        if reg == _BANK_SEL:
            if self._bank == value:
                return
            self._bank = value
        # print(f"write_register {reg:02x} {value:02x}")
        b = bytearray(2)
        b[0] = reg
        b[1] = value
        with self._i2c_device as i2c:
            i2c.write(b)

    def _read_register(self, reg):
        b = bytearray(1)
        b[0] = reg
        with self._i2c_device as i2c:
            i2c.write(b)
            i2c.readinto(b)
        return b[0]


class OV2640(_SCCBCameraBase):  # pylint: disable=too-many-instance-attributes
    """Library for the OV2640 digital camera"""

    test_pattern = _RegBits(_BANK_SENSOR, _COM7, 1, 1)
    gain_ceiling = _RegBits(_BANK_SENSOR, _COM9, 5, 7)
    bpc = _RegBits(_BANK_DSP, _CTRL3, 7, 1)
    wpc = _RegBits(_BANK_DSP, _CTRL3, 6, 1)
    lenc = _RegBits(_BANK_DSP, _CTRL1, 1, 1)

    def __init__(
        self,
        i2c_bus,
        data_pins,
        clock,
        vsync,
        href,
        shutdown=None,
        reset=None,
        mclk=None,
        mclk_frequency=20_000_000,
        i2c_address=0x30,
        size=OV2640_SIZE_QQVGA,
    ):  # pylint: disable=too-many-arguments
        """
        Args:
            i2c_bus (busio.I2C): The I2C bus used to configure the OV2640
            data_pins (List[microcontroller.Pin]): A list of 8 data pins, in order.
            clock (microcontroller.Pin): The pixel clock from the OV2640.
            vsync (microcontroller.Pin): The vsync signal from the OV2640.
            href (microcontroller.Pin): The href signal from the OV2640, \
                sometimes inaccurately called hsync.
            shutdown (Optional[microcontroller.Pin]): If not None, the shutdown
                signal to the camera, also called the powerdown or enable pin.
            reset (Optional[microcontroller.Pin]): If not None, the reset signal
                to the camera.
            mclk (Optional[microcontroller.Pin]): The pin on which to create a
                master clock signal, or None if the master clock signal is
                already being generated.
            mclk_frequency (int): The frequency of the master clock to generate, \
                ignored if mclk is None, requred if it is specified
            i2c_address (int): The I2C address of the camera.
        """

        # Initialize the master clock
        if mclk:
            self._mclk_pwm = pwmio.PWMOut(mclk, frequency=mclk_frequency)
            self._mclk_pwm.duty_cycle = 32768
        else:
            self._mclk_pwm = None

        if shutdown:
            self._shutdown = digitalio.DigitalInOut(shutdown)
            self._shutdown.switch_to_output(True)
            time.sleep(0.1)
            self._shutdown.switch_to_output(False)
            time.sleep(0.3)
        else:
            self._shutdown = None

        if reset:
            self._reset = digitalio.DigitalInOut(reset)
            self._reset.switch_to_output(False)
            time.sleep(0.1)
            self._reset.switch_to_output(True)
            time.sleep(0.1)

        super().__init__(i2c_bus, i2c_address)

        self._write_bank_register(_BANK_SENSOR, _COM7, _COM7_SRST)
        time.sleep(0.001)

        self._write_list(_ov2640_settings_cif)

        self._colorspace = OV2640_COLOR_RGB
        self._w = None
        self._h = None
        self._size = None
        self._test_pattern = False
        self.size = size

        self._flip_x = False
        self._flip_y = False

        self.gain_ceiling = _COM9_AGC_GAIN_2x
        self.bpc = False
        self.wpc = True
        self.lenc = True

        # self._sensor_init()

        self._imagecapture = imagecapture.ParallelImageCapture(
            data_pins=data_pins, clock=clock, vsync=vsync, href=href
        )

    def capture(self, buf):
        """Capture an image into the buffer.

        Args:
            buf (Union[bytearray, memoryview]): A WritableBuffer to contain the \
                captured image.  Note that this can be a ulab array or a displayio Bitmap.
        """
        self._imagecapture.capture(buf)
        if self.colorspace == OV2640_COLOR_JPEG:
            eoi = buf.find(b"\xff\xd9")
            if eoi != -1:
                # terminate the JPEG data just after the EOI marker
                return memoryview(buf)[: eoi + 2]
        return None

    @property
    def capture_buffer_size(self):
        """Return the size of capture buffer to use with current resolution & colorspace settings"""
        if self.colorspace == OV2640_COLOR_JPEG:
            return self.width * self.height // 5
        return self.width * self.height * 2

    @property
    def mclk_frequency(self):
        """Get the actual frequency the generated mclk, or None"""
        return self._mclk_pwm.frequency if self._mclk_pwm else None

    @property
    def width(self):
        """Get the image width in pixels.  A buffer of 2*width*height bytes \
        stores a whole image."""
        return self._w

    @property
    def height(self):
        """Get the image height in pixels.  A buffer of 2*width*height bytes \
        stores a whole image."""
        return self._h

    @property
    def colorspace(self):
        """Get or set the colorspace, one of the ``OV2640_COLOR_`` constants."""
        return self._colorspace

    @colorspace.setter
    def colorspace(self, colorspace):
        self._colorspace = colorspace
        self._set_size_and_colorspace()

    def _set_colorspace(self):
        colorspace = self._colorspace
        settings = _ov2640_color_settings[colorspace]

        self._write_list(settings)
        # written twice?
        self._write_list(settings)
        time.sleep(0.01)

    def deinit(self):
        """Deinitialize the camera"""
        self._imagecapture.deinit()
        if self._mclk_pwm:
            self._mclk_pwm.deinit()
        if self._shutdown:
            self._shutdown.deinit()
        if self._reset:
            self._reset.deinit()

    @property
    def size(self):
        """Get or set the captured image size, one of the ``OV2640_SIZE_`` constants."""
        return self._size

    def _set_size_and_colorspace(self):
        size = self._size
        width, height, ratio = _resolution_info[size]
        offset_x, offset_y, max_x, max_y = _ratio_table[ratio]
        mode = _OV2640_MODE_UXGA
        if size <= OV2640_SIZE_CIF:
            mode = _OV2640_MODE_CIF
            max_x //= 4
            max_y //= 4
            offset_x //= 4
            offset_y //= 4
            max_y = min(max_y, 296)

        elif size <= OV2640_SIZE_SVGA:
            mode = _OV2640_MODE_SVGA
            max_x //= 2
            max_y //= 2
            offset_x //= 2
            offset_y //= 2

        self._set_window(mode, offset_x, offset_y, max_x, max_y, width, height)

    @size.setter
    def size(self, size):
        self._size = size
        self._set_size_and_colorspace()

    def _set_flip(self):
        bits = 0
        if self._flip_x:
            bits |= _REG04_HFLIP_IMG
        if self._flip_y:
            bits |= _REG04_VFLIP_IMG | _REG04_VREF_EN
        self._write_bank_register(_BANK_SENSOR, _REG04, _REG04_SET(bits))

    @property
    def flip_x(self):
        """Get or set the X-flip flag"""
        return self._flip_x

    @flip_x.setter
    def flip_x(self, value):
        self._flip_x = bool(value)
        self._set_flip()

    @property
    def flip_y(self):
        """Get or set the Y-flip flag"""
        return self._flip_y

    @flip_y.setter
    def flip_y(self, value):
        self._flip_y = bool(value)
        self._set_flip()

    @property
    def product_id(self):
        """Get the product id (PID) register.  The expected value is 0x26."""
        return self._read_bank_register(_BANK_SENSOR, _REG_PID)

    @property
    def product_version(self):
        """Get the version (VER) register.  The expected value is 0x4x."""
        return self._read_bank_register(_BANK_SENSOR, _REG_VER)

    def _set_window(
        self, mode, offset_x, offset_y, max_x, max_y, width, height
    ):  # pylint: disable=too-many-arguments, too-many-locals
        self._w = width
        self._h = height

        max_x //= 4
        max_y //= 4
        width //= 4
        height //= 4

        win_regs = [
            _BANK_SEL,
            _BANK_DSP,
            _HSIZE,
            max_x & 0xFF,
            _VSIZE,
            max_y & 0xFF,
            _XOFFL,
            offset_x & 0xFF,
            _YOFFL,
            offset_y & 0xFF,
            _VHYX,
            ((max_y >> 1) & 0x80)
            | ((offset_y >> 4) & 0x70)
            | ((max_x >> 5) & 0x08)
            | ((offset_y >> 8) & 0x07),
            _TEST,
            (max_x >> 2) & 0x80,
            _ZMOW,
            (width) & 0xFF,
            _ZMOH,
            (height) & 0xFF,
            _ZMHH,
            ((height >> 6) & 0x04) | ((width >> 8) & 0x03),
        ]

        pclk_auto = 0
        pclk_div = 8
        clk_2x = 0
        clk_div = 0

        if self._colorspace != OV2640_COLOR_JPEG:
            pclk_auto = 1
            clk_div = 7

        if mode == _OV2640_MODE_CIF:
            regs = _ov2640_settings_to_cif
            if self._colorspace != OV2640_COLOR_JPEG:
                clk_div = 3
        elif mode == _OV2640_MODE_SVGA:
            regs = _ov2640_settings_to_svga
        else:
            regs = _ov2640_settings_to_uxga
            pclk_div = 12

        clk = clk_div | (clk_2x << 7)
        pclk = pclk_div | (pclk_auto << 7)

        self._write_bank_register(_BANK_DSP, _R_BYPASS, _R_BYPASS_DSP_BYPAS)
        self._write_list(regs)
        self._write_list(win_regs)
        self._write_bank_register(_BANK_SENSOR, _CLKRC, clk)
        self._write_bank_register(_BANK_DSP, _R_DVP_SP, pclk)
        self._write_register(_R_BYPASS, _R_BYPASS_DSP_EN)
        time.sleep(0.01)

        # Reestablish colorspace
        self._set_colorspace()

        # Reestablish test pattern
        if self._test_pattern:
            self.test_pattern = self._test_pattern

    @property
    def exposure(self):
        """The exposure level of the sensor"""
        aec_9_2 = self._get_reg_bits(_BANK_SENSOR, _AEC, 0, 0xFF)
        aec_15_10 = self._get_reg_bits(_BANK_SENSOR, _REG45, 0, 0b111111)
        aec_1_0 = self._get_reg_bits(_BANK_SENSOR, _REG04, 0, 0b11)

        return aec_1_0 | (aec_9_2 << 2) | (aec_15_10 << 10)

    @exposure.setter
    def exposure(self, exposure):
        aec_1_0 = exposure & 0x11
        aec_9_2 = (exposure >> 2) & 0b11111111
        aec_15_10 = exposure >> 10

        self._set_reg_bits(_BANK_SENSOR, _AEC, 0, 0xFF, aec_9_2)
        self._set_reg_bits(_BANK_SENSOR, _REG45, 0, 0b111111, aec_15_10)
        self._set_reg_bits(_BANK_SENSOR, _REG04, 0, 0b11, aec_1_0)
