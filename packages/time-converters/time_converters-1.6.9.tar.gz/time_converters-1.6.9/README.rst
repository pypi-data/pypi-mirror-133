Installing
~~~~~~~~~~

**Should work on any version, Python 2.7+ is recommended**


.. code:: sh

    # Linux/macOS
    pip3 install -U time_converters

    # Windows
    pip install -U time_converters

Code Example
~~~~~~~~~~~~~~~~~~~~

.. code:: py

    from time_converters import time_to_sec

    time = '24h'

    print(time_to_sec(time))
    //results: 86400 (int)

Convert proof:
~~~~~~~~~~~~~~~~~~~~
.. image:: https://cdn.discordapp.com/attachments/925827864950108180/929453894470361188/unknown.png
   :target: https://cdn.discordapp.com/attachments/925827864950108180/929453894470361188/unknown.png