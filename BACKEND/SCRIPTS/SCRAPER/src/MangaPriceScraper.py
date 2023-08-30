import requests
from bs4 import BeautifulSoup as BS 
def get_prices(name:str|None, isbn:int|None ):
    """
    Return a list of prices as floats.

    :param name: Name of volume. Not needed if isbn included.
    :type name: Str or None
    :param isbn: ISBN value of volume. Not needed if name included.
    :type isbn: Int or None 
    :raise MangaPriceScraper.PricesNotFoundError: If no prices could be found.
    :return: List of prices. Index 0 is RightStufAnime price, Index 1 is Barnes and Nobles price, and Index 3 is Books a Million price
    :rtype: list[float]

    """

    return [1.0,1.0,1.0]

class PricesNotFoundError(Exception):
    """Raised if the parameters provided do not represent valid manga volume or the 
        volume could not be found on any website."""
    
    pass

def _getBNPrice(name, isbn) -> float:
    """
    Gets price of volume at Barnes and Noble.

    :param name: Name of volume. Not needed if isbn included.
    :type name: Str or None
    :param isbn: ISBN value of volume. Not needed if name included.
    :type isbn: Int or None
    :raise MangaPriceScraper.PricesNotFoundError: If no price could be found.
    :return: Price of volume.
    :rtype: float
    """

    