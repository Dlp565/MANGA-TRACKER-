Usage
=====

.. _installation:

Installation
------------

To use Manga Price Scraper, first install it using pip:

.. code-block:: console

    (.venv) $ pip install MangaPriceScraper

Getting Prices
--------------

To retrieve the price of the manga from the 
three websites, you can use the ``MangaPriceScraper.get_prices()``
function:

.. autofunction:: MangaPriceScraper.get_prices(name=None,isbn=None)

    

    If neither parameter returns a valid price for any of the websites,
    :py:func:`MangaPriceScraper.get_prices` will raise 
    an exception

    .. autoexception:: MangaPriceScraper.PricesNotFoundError

         

