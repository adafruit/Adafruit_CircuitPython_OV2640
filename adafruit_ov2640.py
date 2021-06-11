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
  https://github.com/adafruit/circuitpython/releases

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies
  based on the library's use of either.

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_OV2640.git"

R_BYPASS = 0x05
QS = 0x44
CTRLI = 0x50
HSIZE = 0x51
VSIZE = 0x52
XOFFL = 0x53
YOFFL = 0x54
VHYX = 0x55
DPRP = 0x56
TEST = 0x57
ZMOW = 0x5A
ZMOH = 0x5B
ZMHH = 0x5C
BPADDR = 0x7C
BPDATA = 0x7D
CTRL2 = 0x86
CTRL3 = 0x87
SIZEL = 0x8C
HSIZE8 = 0xC0
VSIZE8 = 0xC1
CTRL0 = 0xC2
CTRL1 = 0xC3
R_DVP_SP = 0xD3
IMAGE_MODE = 0xDA
RESET = 0xE0
MS_SP = 0xF0
SS_ID = 0xF7
SS_CTRL = 0xF7
MC_BIST = 0xF9
MC_AL = 0xFA
MC_AH = 0xFB
MC_D = 0xFC
P_CMD = 0xFD
P_STATUS = 0xFE
BANK_SEL = 0xFF

CTRLI_LP_DP = 0x80
CTRLI_ROUND = 0x40

CTRL0_AEC_EN = 0x80
CTRL0_AEC_SEL = 0x40
CTRL0_STAT_SEL = 0x20
CTRL0_VFIRST = 0x10
CTRL0_YUV422 = 0x08
CTRL0_YUV_EN = 0x04
CTRL0_RGB_EN = 0x02
CTRL0_RAW_EN = 0x01

CTRL2_DCW_EN = 0x20
CTRL2_SDE_EN = 0x10
CTRL2_UV_ADJ_EN = 0x08
CTRL2_UV_AVG_EN = 0x04
CTRL2_CMX_EN = 0x01

CTRL3_BPC_EN = 0x80
CTRL3_WPC_EN = 0x40

R_DVP_SP_AUTO_MODE = 0x80

R_BYPASS_DSP_EN = 0x00
R_BYPASS_DSP_BYPAS = 0x01

IMAGE_MODE_Y8_DVP_EN = 0x40
IMAGE_MODE_JPEG_EN = 0x10
IMAGE_MODE_YUV422 = 0x00
IMAGE_MODE_RAW10 = 0x04
IMAGE_MODE_RGB565 = 0x08
IMAGE_MODE_HREF_VSYNC = 0x02
IMAGE_MODE_LBYTE_FIRST = 0x01

RESET_MICROC = 0x40
RESET_SCCB = 0x20
RESET_JPEG = 0x10
RESET_DVP = 0x04
RESET_IPU = 0x02
RESET_CIF = 0x01

MC_BIST_RESET = 0x80
MC_BIST_BOOT_ROM_SEL = 0x40
MC_BIST_12KB_SEL = 0x20
MC_BIST_12KB_MASK = 0x30
MC_BIST_512KB_SEL = 0x08
MC_BIST_512KB_MASK = 0x0C
MC_BIST_BUSY_BIT_R = 0x02
MC_BIST_MC_RES_ONE_SH_W = 0x02
MC_BIST_LAUNCH = 0x01


typedef enum {
    BANK_DSP, BANK_SENSOR, BANK_MAX
} ov2640_bank_t;

/* Sensor register bank FF=0x01*/
GAIN = 0x00
COM1 = 0x03
REG04 = 0x04
REG08 = 0x08
COM2 = 0x09
REG_PID = 0x0A
REG_VER = 0x0B
COM3 = 0x0C
COM4 = 0x0D
AEC = 0x10
CLKRC = 0x11
COM7 = 0x12
COM8 = 0x13
COM9 = 0x14 # AGC gain ceiling
COM10 = 0x15
HSTART = 0x17
HSTOP = 0x18
VSTART = 0x19
VSTOP = 0x1A
MIDH = 0x1C
MIDL = 0x1D
AEW = 0x24
AEB = 0x25
VV = 0x26
REG2A = 0x2A
FRARL = 0x2B
ADDVSL = 0x2D
ADDVSH = 0x2E
YAVG = 0x2F
HSDY = 0x30
HEDY = 0x31
REG32 = 0x32
ARCOM2 = 0x34
REG45 = 0x45
FLL = 0x46
FLH = 0x47
COM19 = 0x48
ZOOMS = 0x49
COM22 = 0x4B
COM25 = 0x4E
BD50 = 0x4F
BD60 = 0x50
REG5D = 0x5D
REG5E = 0x5E
REG5F = 0x5F
REG60 = 0x60
HISTO_LOW = 0x61
HISTO_HIGH = 0x62

REG04_DEFAULT = 0x28
REG04_HFLIP_IMG = 0x80
REG04_VFLIP_IMG = 0x40
REG04_VREF_EN = 0x10
REG04_HREF_EN = 0x08
REG04_SET = lambda x: (REG04_DEFAULT|x)

COM2_STDBY = 0x10
COM2_OUT_DRIVE_1x = 0x00
COM2_OUT_DRIVE_2x = 0x01
COM2_OUT_DRIVE_3x = 0x02
COM2_OUT_DRIVE_4x = 0x03

COM3_DEFAULT = 0x38
COM3_BAND_50Hz = 0x04
COM3_BAND_60Hz = 0x00
COM3_BAND_AUTO = 0x02
COM3_BAND_SET = lambda x:    (COM3_DEFAULT|x)

COM7_SRST = 0x80
COM7_RES_UXGA = 0x00 # UXGA
COM7_RES_SVGA = 0x40 # SVGA
COM7_RES_CIF = 0x20 # CIF 
COM7_ZOOM_EN = 0x04 # Enable Zoom
COM7_COLOR_BAR = 0x02 # Enable Color Bar Test

COM8_DEFAULT = 0xC0
COM8_BNDF_EN = 0x20 # Enable Banding filter
COM8_AGC_EN = 0x04 # AGC Auto/Manual control selection
COM8_AEC_EN = 0x01 # Auto/Manual Exposure control
COM8_SET = lambda x:         (COM8_DEFAULT|x)

COM9_DEFAULT = 0x08
COM9_AGC_GAIN_2x = 0x00 # AGC:    2x
COM9_AGC_GAIN_4x = 0x01 # AGC:    4x
COM9_AGC_GAIN_8x = 0x02 # AGC:    8x
COM9_AGC_GAIN_16x = 0x03 # AGC:   16x
COM9_AGC_GAIN_32x = 0x04 # AGC:   32x
COM9_AGC_GAIN_64x = 0x05 # AGC:   64x
COM9_AGC_GAIN_128x = 0x06 # AGC:  128x
COM9_AGC_SET = lambda x:     (COM9_DEFAULT|(x<<5))

COM10_HREF_EN = 0x80 # HSYNC changes to HREF
COM10_HSYNC_EN = 0x40 # HREF changes to HSYNC
COM10_PCLK_FREE = 0x20 # PCLK output option: free running PCLK
COM10_PCLK_EDGE = 0x10 # Data is updated at the rising edge of PCLK
COM10_HREF_NEG = 0x08 # HREF negative
COM10_VSYNC_NEG = 0x02 # VSYNC negative
COM10_HSYNC_NEG = 0x01 # HSYNC negative

CTRL1_AWB = 0x08 # Enable AWB

C_TH_SET = lambda h,l:  ((h<<4)|(l&0x0F))

REG32_UXGA = 0x36
REG32_SVGA = 0x09
REG32_CIF = 0x89

CLKRC_2X = 0x80
CLKRC_2X_UXGA = (0x01 | CLKRC_2X)
CLKRC_2X_SVGA = CLKRC_2X
CLKRC_2X_CIF = CLKRC_2X


