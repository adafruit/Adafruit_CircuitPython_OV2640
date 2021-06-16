# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
import busio
import digitalio
import displayio
from adafruit_seesaw.tftshield18 import TFTShield18
from adafruit_st7735r import ST7735R
from adafruit_ov2640 import (  # pylint: disable=unused-import
    OV2640,
    OV2640_SIZE_DIV4,
    OV2640_SIZE_DIV8,
)

# Pylint is unable to see that the "size" property of OV2640_GrandCentral exists
# pylint: disable=attribute-defined-outside-init

# Release any resources currently in use for the displays
displayio.release_displays()

ss = TFTShield18()

spi = board.SPI()
tft_cs = board.D10
tft_dc = board.D8

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)

ss.tft_reset()
display = ST7735R(
    display_bus, width=160, height=128, rotation=90, bgr=True, auto_refresh=False
)

ss.set_backlight(True)


class OV2640_GrandCentral(OV2640):
    def __init__(self):
        with digitalio.DigitalInOut(board.D39) as shutdown:
            shutdown.switch_to_output(True)
            time.sleep(0.001)
            bus = busio.I2C(board.D24, board.D25)
        self._bus = bus
        OV2640.__init__(
            self,
            bus,
            mclk=board.PCC_XCLK,
            data_pins=[
                board.PCC_D0,
                board.PCC_D1,
                board.PCC_D2,
                board.PCC_D3,
                board.PCC_D4,
                board.PCC_D5,
                board.PCC_D6,
                board.PCC_D7,
            ],
            clock=board.PCC_CLK,
            vsync=board.PCC_DEN1,
            href=board.PCC_DEN2,
            shutdown=board.D39,
            reset=board.D38,
        )

    def deinit(self):
        self._bus.deinit()
        OV2640.deinit(self)


cam = OV2640_GrandCentral()

cam.size = OV2640_SIZE_DIV4
cam.flip_x = False
cam.flip_y = True
pid = cam.product_id
ver = cam.product_version
print(f"Detected pid={pid:x} ver={ver:x}")
# cam.test_pattern = True

g = displayio.Group(scale=1)
bitmap = displayio.Bitmap(160, 120, 65536)
tg = displayio.TileGrid(
    bitmap,
    pixel_shader=displayio.ColorConverter(
        input_colorspace=displayio.Colorspace.RGB565_SWAPPED
    ),
)
g.append(tg)
display.show(g)

display.auto_refresh = False
while True:
    cam.capture(bitmap)
    bitmap.dirty()
    display.refresh(minimum_frames_per_second=0)

cam.deinit()