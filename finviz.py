#!/usr/bin/python3

from scrape import scrape_page

BASE_URL = "http://finviz.com/quote.ashx?t="
VALUE_NAMES_XPATH = '//*[@class="snapshot-td2-cp"]/text()'
VALUES_XPATH = '//*[@class="snapshot-td2"]/b/text() | //*[@class="snapshot-td2"]/b/*/text()'

def get_statistics_table(page):
    value_names = page.xpath(VALUE_NAMES_XPATH)

    values = page.xpath(VALUES_XPATH)
    values = [value if value != "-" else None for value in values]

    table = dict(zip(value_names, values))

    return table

def get_statistic(ticker_symbol, stat_name, page=None):
    """
    This function will get the associated financial statistic given the statistic's name and the ticker symbol
    from the corresponding finviz page
    :param ticker_symbol: The ticker symbol of the interested stock (e.g., "AAPL", "GOOG", "MSFT")
    :param stat_name: The name of the interested financial statistic (e.g., "P/E", "Price", "Volume").
    An exhaustive list of available financial statistics can be found on a stock's finviz page
    :param page: HTML tree structure based on the html markup of the scraped web page
    :return:
    """
    if page is None:
        page = scrape_page(BASE_URL + ticker_symbol)

    table = get_statistics_table(page)

    if stat_name in table.keys() and table[stat_name]:
        return table[stat_name]
    else:
        return None

def get_all_statistics(ticker_symbol, page=None):
    if page is None:
        page = scrape_page(BASE_URL + ticker_symbol)

    table = get_statistics_table(page)

    if table:
        return table
    else:
        return None

if __name__ == "__main__":
    # Test Cases
    print(get_statistic("AAPL", "P/E"))
    print(get_statistic("AAPL", "Inst Own"))
    print(get_statistic("AAPL", "Change"))
    print(get_statistic("AAPL", "This should return None"))
    print(get_all_statistics("AAPL"))
