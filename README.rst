Introduction
============


.. image:: https://readthedocs.org/projects/adafruit-circuitpython-ov2640/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/ov2640/en/latest/
    :alt: Documentation Status


.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/adafruit/Adafruit_CircuitPython_OV2640/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_OV2640/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

CircuitPython driver for OV2640 Camera.


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




Usage Example
=============

On an Adafruit Metro M4 Grand Central, capture a 160x120 image into a buffer:

.. code-block:: python3

    import board
    from adafruit_ov2640 import OV2640, OV2640_SIZE_QQVGA

    cam = OV2640(
        bus,
        data_pins=[board.PCC_D0, board.PCC_D1, board.PCC_D2, board.PCC_D3, board.PCC_D4, board.PCC_D5, board.PCC_D6, board.PCC_D7],
        clock=board.PCC_CLK,
        vsync=board.PCC_DEN1,
        href=board.PCC_DEN2,
        mclk=board.D29,
        shutdown=board.D39,
        reset=board.D38,
    )
    cam.size = OV2640_SIZE_QQVGA

    buf = bytearray(2 * cam.width * cam.height)

    cam.capture(buf)


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_OV2640/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
