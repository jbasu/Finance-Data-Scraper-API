#!/usr/bin/python3

from scrape import scrape_page

BASE_URL = "http://www.zacks.com/stock/quote/"
RATING_XPATH = '//*[@id="premium_research"]/div/table/tbody/tr[1]/td/strong/text()'
PEERS_XPATH = '//*[@id="stock_industry_analysis"]/table/tbody/tr/td[2]/a/span/text()'

def get_rating(ticker_symbol, page=None):
    """
    Gets the Zack's Rank Rating of the target ticker symbol
    :param ticker_symbol: The ticker symbol of the interested stock (e.g., "AAPL", "GOOG", "MSFT")
    :param page: html tree structure based on the html markup of the scraped website
    :return: String of Zack's Rank Rating as listed on a stock's Zacks page
    """
    if page is None:
        page = scrape_page(BASE_URL + ticker_symbol)

    rating = page.xpath(RATING_XPATH)

    if not rating:
        return None
    else:
        return rating[0]

def get_peers(ticker_symbol, page=None):
    """
    Gets the list of Top Peers for a stock as listed on the "Premium Research: Industry Analysis" section
    :param ticker_symbol: The ticker symbol of the interested stock (e.g., "AAPL", "GOOG", "MSFT")
    :param page: html tree structure based on the html markup of the scraped website
    :return: a list of the Top Peers as listed on a stock's "Premium Research: Industry Analysis" section
    on it's respective zacks page
    """
    if page is None:
        page = scrape_page(BASE_URL+ ticker_symbol)

    peers = page.xpath(PEERS_XPATH)

    if peers:
        try:
            peers.remove(ticker_symbol.upper())
        except:
            pass

        if peers:
            return peers
        else:
            return None
    else:
        return None

if __name__ == "__main__":
    # Test cases
    print (get_rating("AAPL"))
    print (get_peers("GOOG"))
