# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""
The Kaluga development kit comes in two versions (v1.2 and v1.3); this demo is
tested on v1.3.

The audio board must be mounted between the Kaluga and the LCD, it provides the
I2C pull-ups(!)

This example requires that your WIFI and Adafruit IO credentials be configured
in CIRCUITPY/settings.toml, and that you have created a feed called "image" with
history disabled.

The maximum image size is 100kB after base64 encoding, or about 65kB before
base64 encoding.  In practice, "SVGA" (800x600) images are typically around
40kB even though the "capture_buffer_size" (theoretical maximum size) is
(width*height/5) bytes or 96kB.
"""

import binascii
import time
from os import getenv

import adafruit_connection_manager
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import board
import busio
import wifi
from adafruit_io.adafruit_io import IO_MQTT

import adafruit_ov2640

feed_name = "image"

# Get WiFi details and Adafruit IO keys, ensure these are setup in settings.toml
# (visit io.adafruit.com if you need to create an account, or if you need your Adafruit IO key.)
ssid = getenv("CIRCUITPY_WIFI_SSID")
password = getenv("CIRCUITPY_WIFI_PASSWORD")
aio_username = getenv("ADAFRUIT_AIO_USERNAME")
aio_key = getenv("ADAFRUIT_AIO_KEY")

print("Connecting to WIFI")
wifi.radio.connect(ssid, password)
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)

print("Connecting to Adafruit IO")
mqtt_client = MQTT.MQTT(
    broker="io.adafruit.com",
    username=aio_username,
    password=aio_key,
    socket_pool=pool,
    ssl_context=ssl_context,
)
mqtt_client.connect()
io = IO_MQTT(mqtt_client)

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
cam.flip_y = False
cam.test_pattern = False

cam.size = adafruit_ov2640.OV2640_SIZE_SVGA
cam.colorspace = adafruit_ov2640.OV2640_COLOR_JPEG
jpeg_buffer = bytearray(cam.capture_buffer_size)
while True:
    jpeg = cam.capture(jpeg_buffer)
    print(f"Captured {len(jpeg)} bytes of jpeg data")

    # b2a_base64() appends a trailing newline, which IO does not like
    encoded_data = binascii.b2a_base64(jpeg).strip()
    print(f"Expanded to {len(encoded_data)} for IO upload")

    io.publish("image", encoded_data)

    print("Waiting 3s")
    time.sleep(3)
