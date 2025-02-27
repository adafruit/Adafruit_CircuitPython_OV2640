Simple test
------------

Ensure your device works with this simple test.

.. literalinclude:: ../examples/ov2640_simpletest.py
    :caption: ov2640_simpletest.py
    :linenos:


LCD tests
---------

Kaluga 1.3 with ili9341
~~~~~~~~~~~~~~~~~~~~~~~

Display an image from the camera on the Kaluga 1.3 board, if it is fitted with an ili9341 display.

.. literalinclude:: ../examples/ov2640_displayio_kaluga1_3_ili9341.py
    :caption: ov2640_displayio_kaluga1_3_ili9341.py
    :linenos:

Kaluga 1.3 with st7789
~~~~~~~~~~~~~~~~~~~~~~

Display an image from the camera on the Kaluga 1.3 board, if it is fitted with an st7789 display.

.. literalinclude:: ../examples/ov2640_displayio_kaluga1_3_st7789.py
    :caption: ov2640_displayio_kaluga1_3_st7789.py
    :linenos:

Raspberry Pi Pico with st7789
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Display an image from the camera connected to a Raspberry Pi Pico with an st7789 2" display

.. literalinclude:: ../examples/ov2640_displayio_pico_st7789_2in.py
    :caption: ov2640_displayio_pico_st7789_2in.py
    :linenos:

Kaluga 1.3 with ili9341, direct display
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Preview images on LCD, bypassing displayio for slightly higher framerate

.. literalinclude:: ../examples/ov2640_directio_kaluga1_3_ili9341.py
    :caption: ../examples/ov2640_directio_kaluga1_3_ili9341.py
    :linenos:


Image-saving tests
------------------

Kaluga 1.3 with ili9341, internal flash, JPEG
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Preview images on LCD t hen save JPEG images to internal flash on Kaluga 1.3.  Requires the second snippet of
code to be saved as ``boot.py``.

.. literalinclude:: ../examples/ov2640_jpeg_kaluga1_3.py
    :caption: ov2640_jpeg_kaluga1_3.py
    :linenos:

``boot.py`` for the above program

.. literalinclude:: ../examples/ov2640_jpeg_kaluga1_3_boot.py
    :caption: ov2640_jpeg_kaluga1_3_boot.py
    :linenos:

Kaluga 1.3 with ili9341, external SD card, JPEG
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Preview images on LCD then save JPEG images to SD on Kaluga 1.3 fitted with an ili9341 display.

.. literalinclude:: ../examples/ov2640_jpeg_sd_kaluga1_3.py
    :caption: ov2640_jpeg_sd_kaluga1_3.py
    :linenos:

Kaluga 1.3 with ili9341, external SD card, BMP
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Preview images on LCD then save BMP images to SD on Kaluga 1.3 fitted with an ili9341 display.

.. literalinclude:: ../examples/ov2640_bmp_sd_kaluga1_3.py
    :caption: ov2640_bmp_sd_kaluga1_3.py
    :linenos:


Kaluga 1.3 with Adafruit IO
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Upload JPEG images to Adafruit IO. Requires that WIFI and Adafruit IO be configured in ``settings.toml``.

.. literalinclude:: ../examples/ov2640_aio_kaluga1_3.py
    :caption: ov2640_aio_kaluga1_3.py
    :linenos:
