# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""
The Kaluga development kit comes in two versions (v1.2 and v1.3); this demo is
tested on v1.3.

The audio board must be mounted between the Kaluga and the LCD, it provides the
I2C pull-ups(!)

The v1.3 development kit's LCD can have one of two chips, the ili9341 or
st7789.  Furthermore, there are at least 2 ILI9341 variants, which differ
by rotation.  This example is written for one if the ILI9341 variants,
the one which usually uses rotation=90 to get a landscape display.

This example also requires an SD card breakout wired as follows:
 * IO18: SD Clock Input
 * IO17: SD Serial Output (MISO)
 * IO14: SD Serial Input (MOSI)
 * IO12: SD Chip Select

Insert a CircuitPython-compatible SD card before powering on the Kaluga.
Press the "Record" button on the audio daughterboard to take a photo.
"""

import os
import struct

import analogio
import board
import busdisplay
import busio
import displayio
import fourwire
import sdcardio
import storage

import adafruit_ov2640

V_MODE = 1.98
V_RECORD = 2.41

a = analogio.AnalogIn(board.IO6)

# Release any resources currently in use for the displays
displayio.release_displays()

spi = busio.SPI(MOSI=board.LCD_MOSI, clock=board.LCD_CLK)
display_bus = fourwire.FourWire(
    spi,
    command=board.LCD_D_C,
    chip_select=board.LCD_CS,
    reset=board.LCD_RST,
    baudrate=80_000_000,
)
_INIT_SEQUENCE = (
    b"\x01\x80\x80"  # Software reset then delay 0x80 (128ms)
    b"\xef\x03\x03\x80\x02"
    b"\xcf\x03\x00\xc1\x30"
    b"\xed\x04\x64\x03\x12\x81"
    b"\xe8\x03\x85\x00\x78"
    b"\xcb\x05\x39\x2c\x00\x34\x02"
    b"\xf7\x01\x20"
    b"\xea\x02\x00\x00"
    b"\xc0\x01\x23"  # Power control VRH[5:0]
    b"\xc1\x01\x10"  # Power control SAP[2:0];BT[3:0]
    b"\xc5\x02\x3e\x28"  # VCM control
    b"\xc7\x01\x86"  # VCM control2
    b"\x36\x01\x40"  # Memory Access Control
    b"\x37\x01\x00"  # Vertical scroll zero
    b"\x3a\x01\x55"  # COLMOD: Pixel Format Set
    b"\xb1\x02\x00\x18"  # Frame Rate Control (In Normal Mode/Full Colors)
    b"\xb6\x03\x08\x82\x27"  # Display Function Control
    b"\xf2\x01\x00"  # 3Gamma Function Disable
    b"\x26\x01\x01"  # Gamma curve selected
    b"\xe0\x0f\x0f\x31\x2b\x0c\x0e\x08\x4e\xf1\x37\x07\x10\x03\x0e\x09\x00"  # Set Gamma
    b"\xe1\x0f\x00\x0e\x14\x03\x11\x07\x31\xc1\x48\x08\x0f\x0c\x31\x36\x0f"  # Set Gamma
    b"\x11\x80\x78"  # Exit Sleep then delay 0x78 (120ms)
    b"\x29\x80\x78"  # Display on then delay 0x78 (120ms)
)

display = busdisplay.BusDisplay(display_bus, _INIT_SEQUENCE, width=320, height=240)

bus = busio.I2C(scl=board.CAMERA_SIOC, sda=board.CAMERA_SIOD)
cam = adafruit_ov2640.OV2640(
    bus,
    data_pins=board.CAMERA_DATA,
    clock=board.CAMERA_PCLK,
    vsync=board.CAMERA_VSYNC,
    href=board.CAMERA_HREF,
    mclk=board.CAMERA_XCLK,
    mclk_frequency=20_000_000,
    size=adafruit_ov2640.OV2640_SIZE_QVGA,
)

cam.flip_x = False
cam.flip_y = True
pid = cam.product_id
ver = cam.product_version
print(f"Detected pid={pid:x} ver={ver:x}")
# cam.test_pattern = True

bitmap = displayio.Bitmap(320, 240, 65536)

display.auto_refresh = False

sd_spi = busio.SPI(clock=board.IO18, MOSI=board.IO14, MISO=board.IO17)
sd_cs = board.IO12
sdcard = sdcardio.SDCard(sd_spi, sd_cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")


def exists(filename):
    try:
        os.stat(filename)
        return True
    except OSError:
        return False


_image_counter = 0


def open_next_image():
    global _image_counter  # noqa: PLW0603
    while True:
        filename = f"/sd/img{_image_counter:04d}.jpg"
        _image_counter += 1
        if exists(filename):
            continue
        print("#", filename)
        return open(filename, "wb")


def capture_image():
    old_size = cam.size
    old_colorspace = cam.colorspace
    exposure = cam.exposure
    try:
        cam.size = adafruit_ov2640.OV2640_SIZE_UXGA
        cam.colorspace = adafruit_ov2640.OV2640_COLOR_JPEG
        cam.exposure = exposure
        b = bytearray(cam.capture_buffer_size)
        jpeg = cam.capture(b)

        print(f"Captured {len(jpeg)} bytes of jpeg data")
        with open_next_image() as f:
            f.write(jpeg)
    finally:
        cam.size = old_size
        cam.colorspace = old_colorspace
        cam.exposure = exposure


def main():
    display.auto_refresh = False
    display_bus.send(42, struct.pack(">hh", 0, 319))
    display_bus.send(43, struct.pack(">hh", 0, 239))
    while True:
        a_voltage = a.value * a.reference_voltage / 65535
        record_pressed = abs(a_voltage - V_RECORD) < 0.05
        if record_pressed:
            capture_image()
        cam.capture(bitmap)
        display_bus.send(44, bitmap)


main()
