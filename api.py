#!/usr/bin/python3

from flask import Flask
from flask_restful import Api
import resource

app = Flask(__name__)
api = Api(app)

#Finviz
api.add_resource(resource.Finviz, "/finance/finviz/<string:service>/<string:ticker_symbol>")

#StockTwits
api.add_resource(resource.Stocktwits, "/finance/stocktwits/<string:service>/<string:ticker_symbol>")

#Zacks
api.add_resource(resource.Zacks, "/finance/zacks/<string:service>/<string:ticker_symbol>")

if __name__ == '__main__':
    app.run(debug=True)