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
        return make_response(jsonify(API_Resource.errors[status_code]), status_code)

    @staticmethod
    def json(response):
        if type(response) is dict:
            return make_response(jsonify(response), 200)
        else:
            return API_Resource.error()


class Finviz(API_Resource):
    def __init__(self):
        super().__init__()

        self.parser.add_argument("fields")

    def get(self, service, ticker_symbol):
        args = self.parser.parse_args()

        response = None
        if service == "statistics":
            response = self.get_statistics(ticker_symbol, args)

        return response if response else API_Resource.error(404)

    def get_statistics(self, ticker_symbol, args):
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
    def __init__(self):
        super().__init__()

    def get(self, service, ticker_symbol):
        response = None
        if service == "sentiment":
            response = self.get_sentiment(ticker_symbol)

        return response if response else API_Resource.error(404)

    def get_sentiment(self, ticker_symbol):
        response = {}
        response["bullish"] = stocktwits.get_bullish_sentiment(ticker_symbol)
        response["bearish"] = stocktwits.get_bearish_sentiment(ticker_symbol)

        return API_Resource.json(response) if response["bullish"] and response["bearish"] else API_Resource.error(404)

class Zacks(API_Resource):
    def __init__(self):
        super().__init__()

    def get(self, service, ticker_symbol):
        response = None
        if service == "rating":
            response = self.get_rating(ticker_symbol)
        elif service == "peers":
            response = self.get_peers(ticker_symbol)

        return response if response else API_Resource.error(404)

    def get_rating(self, ticker_symbol):
        response = {}
        response["rating"]  = zacks.get_rating(ticker_symbol)

        return API_Resource.json(response) if response["rating"] else API_Resource.error(404)

    def get_peers(self, ticker_symbol):
        response = {}
        response["peers"]  = zacks.get_peers(ticker_symbol)

        return API_Resource.json(response) if response["peers"] else API_Resource.error(404)