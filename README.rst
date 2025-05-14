Introduction
============


.. image:: https://readthedocs.org/projects/adafruit-circuitpython-ov2640/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/ov2640/en/latest/
    :alt: Documentation Status


.. image:: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Bundle/main/badges/adafruit_discord.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/adafruit/Adafruit_CircuitPython_OV2640/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_OV2640/actions
    :alt: Build Status


.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Code Style: Ruff

CircuitPython driver for OV2640 Camera.

This driver is designed to work directly with the OV2640 camera module through an 18-pin header.
It does not work with products such as ArduCam which process the camera data themselves.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.


* `ESP32-S2 Kaluga Dev Kit featuring ESP32-S2 WROVER <https://www.adafruit.com/product/4729>`_



Usage Example
=============

Using the ESP32-S2 Kaluga Dev Kit and its included camera, capture a 160x120 image into a buffer:

.. code-block:: python3

    import board
    from adafruit_ov2640 import OV2640, OV2640_SIZE_QQVGA

    bus = busio.I2C(scl=board.CAMERA_SIOC, sda=board.CAMERA_SIOD)
    cam = OV2640(
        bus,
        data_pins=board.CAMERA_DATA,
        clock=board.CAMERA_PCLK,
        vsync=board.CAMERA_VSYNC,
        href=board.CAMERA_HREF,
        mclk=board.CAMERA_XCLK,
        size=OV2640_SIZE_QQVGA,
    )
    buf = bytearray(2 * cam.width * cam.height)

    cam.capture(buf)


Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/ov2640/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_OV2640/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
