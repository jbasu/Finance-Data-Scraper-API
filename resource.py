from flask import make_response, jsonify
from flask_restful import reqparse, Resource
import finviz
import stocktwits
import zacks


class API_Resource(Resource):
    """
    This is the base class for all resources in the API which extends Resource class from flask_restful module.
    It contains a few static utility methods, class variables as well as common instance variables.
    """
    errors = {500: {"Error 500": "Could not get data"},
              404: {"Error 404": "Could not find data"}
              }

    def __init__(self):
        super().__init__()

        self.parser = reqparse.RequestParser()

    @staticmethod
    def error(status_code=500):
        """
        Utility method to return various error responses based on HTTP status code
        :param status_code: HTTP status code. Default is 500
        :return: a HTTP response of the error with a corresponding JSON message payload
        """
        return make_response(jsonify(API_Resource.errors[status_code]), status_code)

    @staticmethod
    def json(response):
        """
        Utility method to create JSON payloads of dictionaries and return them as a HTTP response
        :param response:
        :return:
        """
        if type(response) is dict:
            return make_response(jsonify(response), 200)
        else:
            return API_Resource.error()


class Finviz(API_Resource):
    """
    API Resource for the finviz website. This uses the finviz scrapper python script.
    """
    def __init__(self):
        super().__init__()

        self.parser.add_argument("fields")

    def get(self, service, ticker_symbol):
        """
        Handles all GET request for the RESTful API
        :param service: the name of the interested service
        :param ticker_symbol: The ticker symbol of the interested stock (e.g., "AAPL", "GOOG", "MSFT")
        :return: returns a 200 HTTP response along with JSON payload, otherwise returns a 404 response
        """
        args = self.parser.parse_args()

        response = API_Resource.error(404)
        if service == "statistics":
            response = self.get_statistics(ticker_symbol, args)

        return response

    def get_statistics(self, ticker_symbol, args):
        """
        Helper function for the statistics service
        :param ticker_symbol: The ticker symbol of the interested stock (e.g., "AAPL", "GOOG", "MSFT")
        :param args: Optional arguments in the REST call
        :return: a 200 HTTP response with JSON statistics payload of statistics, other a 404 HTTP response
        """
        if args["fields"]:
            response = {}
            for arg in args["fields"].split(","):
                stat = finviz.get_statistic(ticker_symbol, arg)
                if stat:
                    response.update({arg: stat})

            return API_Resource.json(response) if response else API_Resource.error(404)
        else:
            response = finviz.get_all_statistics(ticker_symbol)

            return API_Resource.json(response) if response else API_Resource.error(404)


class Stocktwits(API_Resource):
    """
    API resource for the StockTwits website. This uses the stocktwits scrapper python script
    """
    def __init__(self):
        super().__init__()

    def get(self, service, ticker_symbol):
        """
        Handles all GET request for the RESTful API
        :param service: the name of the interested service
        :param ticker_symbol: The ticker symbol of the interested stock (e.g., "AAPL", "GOOG", "MSFT")
        :return: returns a 200 HTTP response along with JSON payload, otherwise returns a 404 response
        """
        response = API_Resource.error(404)
        if service == "sentiment":
            response = self.get_sentiment(ticker_symbol)

        return response

    def get_sentiment(self, ticker_symbol):
        """
        Helper function for the sentiment service
        :param ticker_symbol: The ticker symbol of the interested stock (e.g., "AAPL", "GOOG", "MSFT")
        :return: returns a 200 HTTP response along with JSON sentiment payload, otherwise returns a 404 response
        """
        response = {}
        response["bullish"] = stocktwits.get_bullish_sentiment(ticker_symbol)
        response["bearish"] = stocktwits.get_bearish_sentiment(ticker_symbol)

        return API_Resource.json(response) if response["bullish"] and response["bearish"] else API_Resource.error(404)

class Zacks(API_Resource):
    """
    API resource for the zacks website. This uses the zacks scrapper python script
    """
    def __init__(self):
        super().__init__()

    def get(self, service, ticker_symbol):
        """
        Handles all GET request for the RESTful API
        :param service: the name of the interested service
        :param ticker_symbol: The ticker symbol of the interested stock (e.g., "AAPL", "GOOG", "MSFT")
        :return: returns a 200 HTTP response along with JSON payload, otherwise returns a 404 response
        """
        response = API_Resource.error(404)
        if service == "rating":
            response = self.get_rating(ticker_symbol)
        elif service == "peers":
            response = self.get_peers(ticker_symbol)

        return response

    def get_rating(self, ticker_symbol):
        """
        Helper function for the rating service
        :param ticker_symbol: The ticker symbol of the interested stock (e.g., "AAPL", "GOOG", "MSFT")
        :return: returns a 200 HTTP response along with JSON rating payload, otherwise returns a 404 response
        """
        response = {}
        response["rating"]  = zacks.get_rating(ticker_symbol)

        return API_Resource.json(response) if response["rating"] else API_Resource.error(404)

    def get_peers(self, ticker_symbol):
        """
        Helper function for the rating service
        :param ticker_symbol: The ticker symbol of the interested stock (e.g., "AAPL", "GOOG", "MSFT")
        :return: returns a 200 HTTP response along with JSON peers payload, otherwise returns a 404 response
        """
        response = {}
        response["peers"]  = zacks.get_peers(ticker_symbol)

        return API_Resource.json(response) if response["peers"] else API_Resource.error(404)