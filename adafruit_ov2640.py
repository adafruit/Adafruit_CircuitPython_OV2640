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

.. todo:: Add links to any specific hardware product page(s), or category page(s).
  Use unordered list & hyperlink rST inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https:# github.com/adafruit/circuitpython/releases

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies
  based on the library's use of either.

# * Adafruit's Bus Device library: https:# github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https:# github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https:# github.com/adafruit/Adafruit_CircuitPython_OV2640.git"

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_OV7670.git"

import time

import digitalio
import imagecapture
import pwmio
from adafruit_bus_device.i2c_device import I2CDevice

from micropython import const

R_BYPASS = const(0x05)
QS = const(0x44)
CTRLI = const(0x50)
HSIZE = const(0x51)
VSIZE = const(0x52)
XOFFL = const(0x53)
YOFFL = const(0x54)
VHYX = const(0x55)
DPRP = const(0x56)
TEST = const(0x57)
ZMOW = const(0x5A)
ZMOH = const(0x5B)
ZMHH = const(0x5C)
BPADDR = const(0x7C)
BPDATA = const(0x7D)
CTRL2 = const(0x86)
CTRL3 = const(0x87)
SIZEL = const(0x8C)
HSIZE8 = const(0xC0)
VSIZE8 = const(0xC1)
CTRL0 = const(0xC2)
CTRL1 = const(0xC3)
R_DVP_SP = const(0xD3)
IMAGE_MODE = const(0xDA)
RESET = const(0xE0)
MS_SP = const(0xF0)
SS_ID = const(0xF7)
SS_CTRL = const(0xF7)
MC_BIST = const(0xF9)
MC_AL = const(0xFA)
MC_AH = const(0xFB)
MC_D = const(0xFC)
P_CMD = const(0xFD)
P_STATUS = const(0xFE)
BANK_SEL = const(0xFF)

CTRLI_LP_DP = const(0x80)
CTRLI_ROUND = const(0x40)

CTRL0_AEC_EN = const(0x80)
CTRL0_AEC_SEL = const(0x40)
CTRL0_STAT_SEL = const(0x20)
CTRL0_VFIRST = const(0x10)
CTRL0_YUV422 = const(0x08)
CTRL0_YUV_EN = const(0x04)
CTRL0_RGB_EN = const(0x02)
CTRL0_RAW_EN = const(0x01)

CTRL2_DCW_EN = const(0x20)
CTRL2_SDE_EN = const(0x10)
CTRL2_UV_ADJ_EN = const(0x08)
CTRL2_UV_AVG_EN = const(0x04)
CTRL2_CMX_EN = const(0x01)

CTRL3_BPC_EN = const(0x80)
CTRL3_WPC_EN = const(0x40)

R_DVP_SP_AUTO_MODE = const(0x80)

R_BYPASS_DSP_EN = const(0x00)
R_BYPASS_DSP_BYPAS = const(0x01)

OV2640_COLOR_RGB = 0
OV2640_COLOR_YUV = 1

IMAGE_MODE_Y8_DVP_EN = const(0x40)
IMAGE_MODE_JPEG_EN = const(0x10)
IMAGE_MODE_YUV422 = const(0x00)
IMAGE_MODE_RAW10 = const(0x04)
IMAGE_MODE_RGB565 = const(0x08)
IMAGE_MODE_HREF_VSYNC = const(0x02)
IMAGE_MODE_LBYTE_FIRST = const(0x01)

RESET_MICROC = const(0x40)
RESET_SCCB = const(0x20)
RESET_JPEG = const(0x10)
RESET_DVP = const(0x04)
RESET_IPU = const(0x02)
RESET_CIF = const(0x01)

MC_BIST_RESET = const(0x80)
MC_BIST_BOOT_ROM_SEL = const(0x40)
MC_BIST_12KB_SEL = const(0x20)
MC_BIST_12KB_MASK = const(0x30)
MC_BIST_512KB_SEL = const(0x08)
MC_BIST_512KB_MASK = const(0x0C)
MC_BIST_BUSY_BIT_R = const(0x02)
MC_BIST_MC_RES_ONE_SH_W = const(0x02)
MC_BIST_LAUNCH = const(0x01)


BANK_DSP = const(0)
BANK_SENSOR = const(1)

# Sensor register bank FF=0x01
GAIN = const(0x00)
COM1 = const(0x03)
REG04 = const(0x04)
REG08 = const(0x08)
COM2 = const(0x09)
REG_PID = const(0x0A)
REG_VER = const(0x0B)
COM3 = const(0x0C)
COM4 = const(0x0D)
AEC = const(0x10)
CLKRC = const(0x11)
COM7 = const(0x12)
COM8 = const(0x13)
COM9 = const(0x14) # AGC gain ceiling
COM10 = const(0x15)
HSTART = const(0x17)
HSTOP = const(0x18)
VSTART = const(0x19)
VSTOP = const(0x1A)
MIDH = const(0x1C)
MIDL = const(0x1D)
AEW = const(0x24)
AEB = const(0x25)
VV = const(0x26)
REG2A = const(0x2A)
FRARL = const(0x2B)
ADDVSL = const(0x2D)
ADDVSH = const(0x2E)
YAVG = const(0x2F)
HSDY = const(0x30)
HEDY = const(0x31)
REG32 = const(0x32)
ARCOM2 = const(0x34)
REG45 = const(0x45)
FLL = const(0x46)
FLH = const(0x47)
COM19 = const(0x48)
ZOOMS = const(0x49)
COM22 = const(0x4B)
COM25 = const(0x4E)
BD50 = const(0x4F)
BD60 = const(0x50)
REG5D = const(0x5D)
REG5E = const(0x5E)
REG5F = const(0x5F)
REG60 = const(0x60)
HISTO_LOW = const(0x61)
HISTO_HIGH = const(0x62)

REG04_DEFAULT = const(0x28)
REG04_HFLIP_IMG = const(0x80)
REG04_VFLIP_IMG = const(0x40)
REG04_VREF_EN = const(0x10)
REG04_HREF_EN = const(0x08)
REG04_SET = lambda x: (REG04_DEFAULT|x)

COM2_STDBY = const(0x10)
COM2_OUT_DRIVE_1x = const(0x00)
COM2_OUT_DRIVE_2x = const(0x01)
COM2_OUT_DRIVE_3x = const(0x02)
COM2_OUT_DRIVE_4x = const(0x03)

COM3_DEFAULT = const(0x38)
COM3_BAND_50Hz = const(0x04)
COM3_BAND_60Hz = const(0x00)
COM3_BAND_AUTO = const(0x02)
COM3_BAND_SET = lambda x:    (COM3_DEFAULT|x)

COM7_SRST = const(0x80)
COM7_RES_UXGA = const(0x00) # UXGA
COM7_RES_SVGA = const(0x40) # SVGA
COM7_RES_CIF = const(0x20) # CIF 
COM7_ZOOM_EN = const(0x04) # Enable Zoom
COM7_COLOR_BAR = const(0x02) # Enable Color Bar Test

COM8_DEFAULT = const(0xC0)
COM8_BNDF_EN = const(0x20) # Enable Banding filter
COM8_AGC_EN = const(0x04) # AGC Auto/Manual control selection
COM8_AEC_EN = const(0x01) # Auto/Manual Exposure control
COM8_SET = lambda x:         (COM8_DEFAULT|x)

COM9_DEFAULT = const(0x08)
COM9_AGC_GAIN_2x = const(0x00) # AGC:    2x
COM9_AGC_GAIN_4x = const(0x01) # AGC:    4x
COM9_AGC_GAIN_8x = const(0x02) # AGC:    8x
COM9_AGC_GAIN_16x = const(0x03) # AGC:   16x
COM9_AGC_GAIN_32x = const(0x04) # AGC:   32x
COM9_AGC_GAIN_64x = const(0x05) # AGC:   64x
COM9_AGC_GAIN_128x = const(0x06) # AGC:  128x
COM9_AGC_SET = lambda x:     (COM9_DEFAULT|(x<<5))

COM10_HREF_EN = const(0x80) # HSYNC changes to HREF
COM10_HSYNC_EN = const(0x40) # HREF changes to HSYNC
COM10_PCLK_FREE = const(0x20) # PCLK output option: free running PCLK
COM10_PCLK_EDGE = const(0x10) # Data is updated at the rising edge of PCLK
COM10_HREF_NEG = const(0x08) # HREF negative
COM10_VSYNC_NEG = const(0x02) # VSYNC negative
COM10_HSYNC_NEG = const(0x01) # HSYNC negative

CTRL1_AWB = const(0x08) # Enable AWB

VV_AGC_TH_SET = lambda h,l:  ((h<<4)|(l&0x0F))

REG32_UXGA = const(0x36)
REG32_SVGA = const(0x09)
REG32_CIF = const(0x89)

CLKRC_2X = const(0x80)
CLKRC_2X_UXGA = const(0x01 | CLKRC_2X)
CLKRC_2X_SVGA = CLKRC_2X
CLKRC_2X_CIF = CLKRC_2X

OV2640_MODE_CIF = const(0)
OV2640_MODE_SVGA = const(1)
OV2640_MODE_UXGA = const(2)

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

ASPECT_RATIO_4X3 = const(0)
ASPECT_RATIO_3X2 = const(1)
ASPECT_RATIO_16X10 = const(2)
ASPECT_RATIO_5X3 = const(3)
ASPECT_RATIO_16X9 = const(4)
ASPECT_RATIO_21X9 = const(5)
ASPECT_RATIO_5X4 = const(6)
ASPECT_RATIO_1X1 = const(7)
ASPECT_RATIO_9X16 = const(8)

_resolution_info = [
    [   96,   96, ASPECT_RATIO_1X1   ], # 96x96
    [  160,  120, ASPECT_RATIO_4X3   ], # QQVGA
    [  176,  144, ASPECT_RATIO_5X4   ], # QCIF 
    [  240,  176, ASPECT_RATIO_4X3   ], # HQVGA
    [  240,  240, ASPECT_RATIO_1X1   ], # 240x240
    [  320,  240, ASPECT_RATIO_4X3   ], # QVGA 
    [  400,  296, ASPECT_RATIO_4X3   ], # CIF  
    [  480,  320, ASPECT_RATIO_3X2   ], # HVGA 
    [  640,  480, ASPECT_RATIO_4X3   ], # VGA  
    [  800,  600, ASPECT_RATIO_4X3   ], # SVGA 
    [ 1024,  768, ASPECT_RATIO_4X3   ], # XGA  
    [ 1280,  720, ASPECT_RATIO_16X9  ], # HD   
    [ 1280, 1024, ASPECT_RATIO_5X4   ], # SXGA 
    [ 1600, 1200, ASPECT_RATIO_4X3   ], # UXGA 
]

_ratio_table = [
    # ox,  oy,   mx,   my
    [   0,   0, 1600, 1200 ], # 4x3
    [   8,  72, 1584, 1056 ], # 3x2
    [   0, 100, 1600, 1000 ], # 16x10
    [   0, 120, 1600,  960 ], # 5x3
    [   0, 150, 1600,  900 ], # 16x9
    [   2, 258, 1596,  684 ], # 21x9
    [  50,   0, 1500, 1200 ], # 5x4
    [ 200,   0, 1200, 1200 ], # 1x1
    [ 462,   0,  676, 1200 ]  # 9x16
]

# 30fps@24MHz
_ov2640_settings_cif = bytes([
    BANK_SEL, BANK_DSP,
    0x2c, 0xff,
    0x2e, 0xdf,
    BANK_SEL, BANK_SENSOR,
    0x3c, 0x32,
    CLKRC, 0x01,
    COM2, COM2_OUT_DRIVE_3x,
    REG04, REG04_DEFAULT,
    COM8, COM8_DEFAULT | COM8_BNDF_EN | COM8_AGC_EN | COM8_AEC_EN,
    COM9, COM9_AGC_SET(COM9_AGC_GAIN_8x),
    0x2c, 0x0c,
    0x33, 0x78,
    0x3a, 0x33,
    0x3b, 0xfB,
    0x3e, 0x00,
    0x43, 0x11,
    0x16, 0x10,
    0x39, 0x92,
    0x35, 0xda,
    0x22, 0x1a,
    0x37, 0xc3,
    0x23, 0x00,
    ARCOM2, 0xc0,
    0x06, 0x88,
    0x07, 0xc0,
    COM4, 0x87,
    0x0e, 0x41,
    0x4c, 0x00,
    0x4a, 0x81,
    0x21, 0x99,
    AEW, 0x40,
    AEB, 0x38,
    VV, VV_AGC_TH_SET(8,2),
    0x5c, 0x00,
    0x63, 0x00,
    HISTO_LOW, 0x70,
    HISTO_HIGH, 0x80,
    0x7c, 0x05,
    0x20, 0x80,
    0x28, 0x30,
    0x6c, 0x00,
    0x6d, 0x80,
    0x6e, 0x00,
    0x70, 0x02,
    0x71, 0x94,
    0x73, 0xc1,
    0x3d, 0x34,
    0x5a, 0x57,
    BD50, 0xbb,
    BD60, 0x9c,
    COM7, COM7_RES_CIF,
    HSTART, 0x11,
    HSTOP, 0x43,
    VSTART, 0x00,
    VSTOP, 0x25,
    REG32, 0x89,
    0x37, 0xc0,
    BD50, 0xca,
    BD60, 0xa8,
    0x6d, 0x00,
    0x3d, 0x38,
    BANK_SEL, BANK_DSP,
    0xe5, 0x7f,
    MC_BIST, MC_BIST_RESET | MC_BIST_BOOT_ROM_SEL,
    0x41, 0x24,
    RESET, RESET_JPEG | RESET_DVP,
    0x76, 0xff,
    0x33, 0xa0,
    0x42, 0x20,
    0x43, 0x18,
    0x4c, 0x00,
    CTRL3, CTRL3_WPC_EN | 0x10 ,
    0x88, 0x3f,
    0xd7, 0x03,
    0xd9, 0x10,
    R_DVP_SP, R_DVP_SP_AUTO_MODE | 0x02,
    0xc8, 0x08,
    0xc9, 0x80,
    BPADDR, 0x00,
    BPDATA, 0x00,
    BPADDR, 0x03,
    BPDATA, 0x48,
    BPDATA, 0x48,
    BPADDR, 0x08,
    BPDATA, 0x20,
    BPDATA, 0x10,
    BPDATA, 0x0e,
    0x90, 0x00,
    0x91, 0x0e,
    0x91, 0x1a,
    0x91, 0x31,
    0x91, 0x5a,
    0x91, 0x69,
    0x91, 0x75,
    0x91, 0x7e,
    0x91, 0x88,
    0x91, 0x8f,
    0x91, 0x96,
    0x91, 0xa3,
    0x91, 0xaf,
    0x91, 0xc4,
    0x91, 0xd7,
    0x91, 0xe8,
    0x91, 0x20,
    0x92, 0x00,
    0x93, 0x06,
    0x93, 0xe3,
    0x93, 0x05,
    0x93, 0x05,
    0x93, 0x00,
    0x93, 0x04,
    0x93, 0x00,
    0x93, 0x00,
    0x93, 0x00,
    0x93, 0x00,
    0x93, 0x00,
    0x93, 0x00,
    0x93, 0x00,
    0x96, 0x00,
    0x97, 0x08,
    0x97, 0x19,
    0x97, 0x02,
    0x97, 0x0c,
    0x97, 0x24,
    0x97, 0x30,
    0x97, 0x28,
    0x97, 0x26,
    0x97, 0x02,
    0x97, 0x98,
    0x97, 0x80,
    0x97, 0x00,
    0x97, 0x00,
    0xa4, 0x00,
    0xa8, 0x00,
    0xc5, 0x11,
    0xc6, 0x51,
    0xbf, 0x80,
    0xc7, 0x10,
    0xb6, 0x66,
    0xb8, 0xA5,
    0xb7, 0x64,
    0xb9, 0x7C,
    0xb3, 0xaf,
    0xb4, 0x97,
    0xb5, 0xFF,
    0xb0, 0xC5,
    0xb1, 0x94,
    0xb2, 0x0f,
    0xc4, 0x5c,
    CTRL1, 0xfd,
    0x7f, 0x00,
    0xe5, 0x1f,
    0xe1, 0x67,
    0xdd, 0x7f,
    IMAGE_MODE, 0x00,
    RESET, 0x00,
    R_BYPASS, R_BYPASS_DSP_EN,
])

_ov2640_settings_to_cif = bytes([
    BANK_SEL, BANK_SENSOR,
    COM7, COM7_RES_CIF,

    # Set the sensor output window
    COM1, 0x0A,
    REG32, REG32_CIF,
    HSTART, 0x11,
    HSTOP, 0x43,
    VSTART, 0x00,
    VSTOP, 0x25,

    # CLKRC, 0x00,
    BD50, 0xca,
    BD60, 0xa8,
    0x5a, 0x23,
    0x6d, 0x00,
    0x3d, 0x38,
    0x39, 0x92,
    0x35, 0xda,
    0x22, 0x1a,
    0x37, 0xc3,
    0x23, 0x00,
    ARCOM2, 0xc0,
    0x06, 0x88,
    0x07, 0xc0,
    COM4, 0x87,
    0x0e, 0x41,
    0x4c, 0x00,
    BANK_SEL, BANK_DSP,
    RESET, RESET_DVP,

    # Set the sensor resolution (UXGA, SVGA, CIF)
    HSIZE8, 0x32,
    VSIZE8, 0x25,
    SIZEL, 0x00,

    # Set the image window size >= output size
    HSIZE, 0x64,
    VSIZE, 0x4a,
    XOFFL, 0x00,
    YOFFL, 0x00,
    VHYX, 0x00,
    TEST, 0x00,

    CTRL2, CTRL2_DCW_EN | 0x1D,
    CTRLI, CTRLI_LP_DP | 0x00,
    # R_DVP_SP, 0x08,
])

_ov2640_settings_to_svga = bytes([
    BANK_SEL, BANK_SENSOR,
    COM7, COM7_RES_SVGA,

    # Set the sensor output window
    COM1, 0x0A,
    REG32, REG32_SVGA,
    HSTART, 0x11,
    HSTOP, 0x43,
    VSTART, 0x00,
    VSTOP, 0x4b,

    # CLKRC, 0x00,
    0x37, 0xc0,
    BD50, 0xca,
    BD60, 0xa8,
    0x5a, 0x23,
    0x6d, 0x00,
    0x3d, 0x38,
    0x39, 0x92,
    0x35, 0xda,
    0x22, 0x1a,
    0x37, 0xc3,
    0x23, 0x00,
    ARCOM2, 0xc0,
    0x06, 0x88,
    0x07, 0xc0,
    COM4, 0x87,
    0x0e, 0x41,
    0x42, 0x03,
    0x4c, 0x00,
    BANK_SEL, BANK_DSP,
    RESET, RESET_DVP,

    # Set the sensor resolution (UXGA, SVGA, CIF)
    HSIZE8, 0x64,
    VSIZE8, 0x4B,
    SIZEL, 0x00,

    # Set the image window size >= output size
    HSIZE, 0xC8,
    VSIZE, 0x96,
    XOFFL, 0x00,
    YOFFL, 0x00,
    VHYX, 0x00,
    TEST, 0x00,

    CTRL2, CTRL2_DCW_EN | 0x1D,
    CTRLI, CTRLI_LP_DP | 0x00,
    # R_DVP_SP, 0x08,
])

_ov2640_settings_to_uxga = bytes([
    BANK_SEL, BANK_SENSOR,
    COM7, COM7_RES_UXGA,

    # Set the sensor output window
    COM1, 0x0F,
    REG32, REG32_UXGA,
    HSTART, 0x11,
    HSTOP, 0x75,
    VSTART, 0x01,
    VSTOP, 0x97,

    # CLKRC, 0x00,
    0x3d, 0x34,
    BD50, 0xbb,
    BD60, 0x9c,
    0x5a, 0x57,
    0x6d, 0x80,
    0x39, 0x82,
    0x23, 0x00,
    0x07, 0xc0,
    0x4c, 0x00,
    0x35, 0x88,
    0x22, 0x0a,
    0x37, 0x40,
    ARCOM2, 0xa0,
    0x06, 0x02,
    COM4, 0xb7,
    0x0e, 0x01,
    0x42, 0x83,
    BANK_SEL, BANK_DSP,
    RESET, RESET_DVP,

    # Set the sensor resolution (UXGA, SVGA, CIF)
    HSIZE8, 0xc8,
    VSIZE8, 0x96,
    SIZEL, 0x00,

    # Set the image window size >= output size
    HSIZE, 0x90,
    VSIZE, 0x2c,
    XOFFL, 0x00,
    YOFFL, 0x00,
    VHYX, 0x88,
    TEST, 0x00,

    CTRL2, CTRL2_DCW_EN | 0x1d,
    CTRLI, 0x00,
    # R_DVP_SP, 0x06,
])

# _ov2640_settings_jpeg3 = bytes([
#     BANK_SEL, BANK_DSP,
#     RESET, RESET_JPEG | RESET_DVP,
#     IMAGE_MODE, IMAGE_MODE_JPEG_EN | IMAGE_MODE_HREF_VSYNC,
#     0xD7, 0x03,
#     0xE1, 0x77,
#     0xE5, 0x1F,
#     0xD9, 0x10,
#     0xDF, 0x80,
#     0x33, 0x80,
#     0x3C, 0x10,
#     0xEB, 0x30,
#     0xDD, 0x7F,
#     RESET, 0x00,
# ])

_ov2640_settings_yuv422 = bytes([
    BANK_SEL, BANK_DSP,
    RESET, RESET_DVP,
    IMAGE_MODE, IMAGE_MODE_YUV422,
    0xD7, 0x01,
    0xE1, 0x67,
    RESET, 0x00,
])

_ov2640_settings_rgb565 = bytes([
    BANK_SEL, BANK_DSP,
    RESET, RESET_DVP,
    IMAGE_MODE, IMAGE_MODE_RGB565,
    0xD7, 0x03,
    0xE1, 0x77,
    RESET, 0x00,
])

class RegBits:
    def __init__(self, bank, reg, shift, mask):
        self.bank = bank
        self.reg = reg
        self.shift = shift
        self.mask = mask

    def __get__(self, obj):
        reg_value = obj._read_bank_register(self.bank, self.reg)
        return (obj >> shift) & mask

    def __set__(self, obj, value):
        if value & ~self.mask:
            raise ValueError(
                f"Value 0x{value:02x} does not fit in mask 0x{self._mask:02x}"
            )
        reg_value = obj._read_bank_register(self.bank, self.reg)
        reg_value &= ~(self.mask << self.shift)
        reg_value |= (value << self.shift)
        obj._write_register(self.reg, reg_value)
 
class RegBool(RegBits):
    def __init__(self, bank, reg, shift):
        super().__init__(bank, reg, shift, 1)

    def __get__(self, obj):
        return bool(super().__get__(obj))

    def __set__(self, obj, value):
        super().__set__(obj, bool(value))

class OV2640:  # pylint: disable=too-many-instance-attributes
    """Library for the OV2640 digital camera"""

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
        mclk_frequency=24_000_000,
        i2c_address=0x30,
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
            time.sleep(0.001)
            self._shutdown.switch_to_output(False)
            time.sleep(0.3)
        else:
            self._shutdown = None

        if reset:
            self._reset = digitalio.DigitalInOut(reset)
            self._reset.switch_to_output(False)
            time.sleep(0.001)
            self._reset.switch_to_output(True)
            time.sleep(0.001)

        self._i2c_device = I2CDevice(i2c_bus, i2c_address)

        self._bank = None
        self._write_bank_register(BANK_SENSOR, COM7, COM7_SRST)
        time.sleep(0.001)

        self._write_list(_ov2640_settings_cif)

        self._colorspace = OV2640_COLOR_RGB
        self._w = None
        self._h = None
        self._size = None
        self._test_pattern = False
        self.size = OV2640_SIZE_QQVGA
        self.size = OV2640_SIZE_QQVGA

        self._flip_x = False
        self._flip_y = False

        self.gain_ceiling = COM9_AGC_GAIN_2x
        self.bpc = False
        self.wpc = True
        self.lenc = True

        #self._sensor_init()

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
        print('setting colorspace')
        self._write_list(_ov2640_settings_rgb565 if colorspace == OV2640_COLOR_RGB else _ov2640_settings_yuv422)
        print('setting colorspace again')
        # written twice?
        self._write_list(_ov2640_settings_rgb565 if colorspace == OV2640_COLOR_RGB else _ov2640_settings_yuv422)
        time.sleep(.01)

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

    @size.setter
    def size(self, size):
        width, height, ratio = _resolution_info[size]
        offset_x, offset_y, max_x, max_y = _ratio_table[ratio]
        print(f"set size={size} {width}x{height} ratio={ratio}")
        print(f"pre", offset_x, offset_y, max_x, max_y)
        mode = OV2640_MODE_UXGA
        if size <= OV2640_SIZE_CIF:
            mode = OV2640_MODE_CIF
            max_x //= 4            
            max_y //= 4            
            offset_x //= 4            
            offset_y //= 4            
            if max_y > 296:
                max_y = 296

        elif size <= OV2640_SIZE_SVGA:
            mode = OV2640_MODE_SVGA
            max_x //= 2
            max_y //= 2
            offset_x //= 2
            offset_y //= 2

        print(f"post", offset_x, offset_y, max_x, max_y)
        self._set_window(mode, offset_x, offset_y, max_x, max_y, width, height)
        self._size = size

    test_pattern = RegBool(BANK_SENSOR, COM7, 1)

    def _set_flip(self):
        bits = 0
        if self._flip_x:
            bits |= REG04_HFLIP_IMG
        if self._flip_y:
            bits |= REG04_VFLIP_IMG | REG04_VREF_EN
        self._write_bank_register(BANK_SENSOR, REG04, REG04_SET(bits))

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
        return self._read_bank_register(BANK_SENSOR, REG_PID)

    @property
    def product_version(self):
        """Get the version (VER) register.  The expected value is 0x4x."""
        return self._read_bank_register(BANK_SENSOR, REG_VER)

    def _write_list(self, reg_list):
        for i in range(0, len(reg_list), 2):
            self._write_register(reg_list[i], reg_list[i + 1])
            time.sleep(0.001)

    def _write_bank_register(self, bank, reg, value):
        if self._bank != bank:
            self._write_register(BANK_SEL, bank)
        self._write_register(reg, value)

    def _read_bank_register(self, bank, reg):
        if self._bank != bank:
            self._write_register(BANK_SEL, bank)
        result = self._read_register(reg)
        print(f"read_bank_register({bank}, 0x{reg:02x}) -> 0x{result:02x}")
        return result

    def _write_register(self, reg, value):
        #print(f"write_register(0x{reg:02x}, 0x{value:02x})")
        if reg == BANK_SEL:
            if self._bank == value: return
            self._bank = value
        print(f"write to 0x30 ack data: 0x{reg:02X} 0x{value:02X}")
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

    def _set_window(
        self, mode, offset_x, offset_y, max_x, max_y, w, h
    ):  # pylint: disable=too-many-arguments
        self._w = w
        self._h = h

        max_x //= 4
        max_y //= 4
        w //= 4
        h //= 4

        win_regs = [
            BANK_SEL, BANK_DSP,
            HSIZE, max_x & 0xFF,
            VSIZE, max_y & 0xFF,
            XOFFL, offset_x & 0xFF,
            YOFFL, offset_y & 0xFF,
            VHYX, ((max_y >> 1) & 0X80) | ((offset_y >> 4) & 0X70) | ((max_x >> 5) & 0X08) | ((offset_y >> 8) & 0X07),
            TEST, (max_x >> 2) & 0X80,
            ZMOW, (w)&0xFF,
            ZMOH, (h)&0xFF,
            ZMHH, ((h>>6)&0x04)|((w>>8)&0x03),
        ]

        print("_set_window", offset_x, offset_y, max_x, max_y, w, h)
        print("win_regs", win_regs)
        pclk_auto = 1
        pclk_div = 7
        clk_2x = 0
        clk_div = 0

        if mode == OV2640_MODE_CIF:
            print("using cif settings")
            regs = _ov2640_settings_to_cif
            #if pixformat is not jpeg:
            clk_div = 3
        elif mode == OV2640_MODE_SVGA:
            print("using svga settings")
            regs = _ov2640_settings_to_svga
        else:
            print("using uxga settings")
            regs = _ov2640_settings_to_uxga
            pclk_div = 12

        clk = clk_div | (clk_2x << 7)
        pclk = pclk_div | (pclk_auto << 7)

        self._write_bank_register(BANK_DSP, R_BYPASS, R_BYPASS_DSP_BYPAS)
        self._write_list(regs)
        self._write_list(win_regs)
        self._write_bank_register(BANK_SENSOR, CLKRC, clk)
        self._write_bank_register(BANK_DSP, R_DVP_SP, pclk)
        self._write_register(R_BYPASS, R_BYPASS_DSP_EN)
        time.sleep(.01)

        # Reestablish colorspace
        self.colorspace = self._colorspace

        # Reestablish test pattern
        if self._test_pattern:
            self.test_pattern = self._test_pattern


    def _get_reg_bits(self, bank, reg, shift, mask):
        return (self._read_bank_register(bank, reg) >> shift) & mask
    
    def _set_reg_bits(self, bank, reg, shift, mask, value):
        reg_value = self._read_bank_register(bank, reg)
        reg_value &= ~ (mask << shift)
        reg_value |= (value << shift)
        self._write_register(reg, reg_value)

    gain_ceiling = RegBits(BANK_SENSOR, COM9, 5, 7)

    bpc = RegBool(BANK_DSP, CTRL3, 7)
    wpc = RegBool(BANK_DSP, CTRL3, 6)
    lenc = RegBool(BANK_DSP, CTRL1, 1)
