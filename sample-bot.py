#!/usr/bin/python3

# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x bot.py
# 3) Run in loop: while true; do ./bot.py; sleep 1; done

#f  rom __future__ import print_function

import sys
import socket
import json
from random import randrange
from collections import defaultdict

# ~~~~~============== CONFIGURATION  ==============~~~~~
# replace REPLACEME with your team name!
team_name="FLYINGCIRCUS"
# This variable dictates whether or not the bot is connecting to the prod
# or test exchange. Be careful with this switch!
test_mode = "-test" in sys.argv

# This setting changes which test exchange is connected to.
# 0 is prod-like
# 1 is slower
# 2 is empty
# this is my provate comment111 
test_exchange_index=0
prod_exchange_hostname="production"

port=25000 + (test_exchange_index if test_mode else 0)
exchange_hostname = "test-exch-" + team_name if test_mode else prod_exchange_hostname
outd = defaultdict(lambda : False)

__ID = 1
def next():
    global __ID
    __ID += 1
    return randrange(2**31)

# ~~~~~============== NETWORKING CODE ==============~~~~~
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((exchange_hostname, port))
    return s.makefile('rw', 1)

def write_to_exchange(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read_from_exchange(exchange):
    return json.loads(exchange.readline())

def sell(symbol, price, size):
    ID = next()
    price = int(price)
    request = {"type": "add", "order_id": ID, "symbol": symbol, "dir": "SELL", "price": price, "size": size}
    write_to_exchange(exchange,request)
    return ID
    

def buy(symbol, price, size):
    ID = next()
    price = int(price)
    request = {"type": "add", "order_id": ID, "symbol": symbol, "dir": "BUY", "price": price, "size": size}
    write_to_exchange(exchange,request)
    return ID

def getoutid(request):
    if request["type"] in ["out", "reject"]:
        return request["order_id"]
    else:
        False


def bond_trade(sell_id, buy_id):
    global outd
    if outd[sell_id]:
        sell_id = sell("BOND",1001,1)
        #print("sell", sell_id)
    if outd[buy_id]:
        buy_id = buy("BOND",999,1)
        #print("buy", buy_id)
    return sell_id, buy_id

def vale_trade(sell_id, buy_id):
    global outd
    if outd[sell_id]:
        price = histories.securities["VALE"].predict_sell()
        sell_id = sell("VALE",price,5)
        print("VALE sell", sell_id)
    if outd[buy_id]:
        price = histories.securities["VALE"].predict_buy()
        buy_id = buy("VALE",price,5)
        print("VALE buy", buy_id)
    return sell_id, buy_id

def is_trade(msg):
    return msg["type"] == "trade"

def print_trade(msg):
    if msg["symbol"] in ["VALE", "VALBZ","BOND"]:
        print(msg["symbol"], msg["price"], msg["size"])

class trading_bot:
    def __init__(self, symbol):
        self.symbol = symbol
        self.sell_ids = []
        self.buy_ids = []
        self.limit = 5


    def trade():
        symbol = self.symbol
        if count_alive(self.sell_ids) > self.limit:
            price = histories.securities[symbol].predict_sell()
            sell_id = sell(symbol,price,5)
            #print("sell", sell_id)
        if count_alive(self.buy_ids) > self.limit
            price = histories.securities[symbol].predict_buy()
            buy_id = buy(symbol,price,5)
            #print("buy", buy_id)
        self.sell_ids += [sell_id]
        self.buy_ids += [buy_id]


def count_alive(ids):
    return sum(map(lambda x : outd[x] == False))

class trades_histories:
    def __init__(self):
        self.securities = {}
        self.names = ["BOND", "GS", "MS", "WFC", "VALBZ", "VALE", "XLF"]
        for name in self.names:
            self.securities[name] = trade_history()
    def add(self, msg):
        self.securities[msg["symbol"]].add(msg)

    def wavg(self):
        ret = {}
        for name in self.names:
            ret[name] = self.securities[name].get_wavg()
        return ret

    def max(self):
        ret = {}
        for name in self.names:
            ret[name] = self.securities[name].get_max()
        return ret

    def min(self):
        ret = {}
        for name in self.names:
            ret[name] = self.securities[name].get_min()
        return ret

    def delta(self):
        ret = {}
        for name in self.names:
            ret[name] = self.securities[name].get_delta()
        return ret

    def predict_sell(self):
        ret = {}
        for name in self.names:
            if name == "XLF":
                ret[name] = 3 * ret["BOND"] + 2 * ret["GS"] + 3 * ret["MS"] + 2 * ret["WFC"] / 10
            else:
                ret[name] = self.securities[name].predict_sell()
        return ret


    def predict_buy(self):
        ret = {}
        for name in self.names:
            if name == "XLF":
                ret[name] = 3 * ret["BOND"] + 2 * ret["GS"] + 3 * ret["MS"] + 2 * ret["WFC"] / 10
            else:
                ret[name] = self.securities[name].predict_buy()
        return ret

    def print_all(self):
        print("wavg", self.wavg())
        print("#######################################")
        print("min", self.min())
        print("#######################################")
        print("max", self.max())
        print("#######################################")
        print("delta", self.delta())
        print("#######################################")
        print("sell", self.predict_sell())
        print("#######################################")
        print("buy", self.predict_buy())
        print("#######################################")


            

def fst(xs):
    return [x[0] for x in xs]

class trade_history:
    def __init__(self):
        self.trade = []

    def add(self, msg):
        self.trade += [(msg["price"], msg["size"]) ]

    def get_wavg(self):
        return wavg(self.trade)

    def get_min(self):
        return min(self.trade)

    def get_max(self):
        return max(self.trade)

    def get_delta(self):
        return max(fst(self.trade)) - min(fst(self.trade))

    def predict_sell(self):
        return self.get_wavg() + 0.1 * self.get_delta()

    def predict_buy(self):
        return self.get_wavg() - 0.1 * self.get_delta()


def wavg(xs):
    weight = sum(map(lambda x : x[1], xs))
    suma = sum(map(lambda x : x[0] * x[1], xs))
    return 1.0 * suma / weight
# ~~~~~============== MAIN LOOP ==============~~~~~


BUY = "BUY"
SELL = "SELL"

histories = trades_histories()
bot = trading_bot("XLF")

def main():
    
    write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
    hello_from_exchange = read_from_exchange(exchange)
    # A common mistake people make is to call write_to_exchange() > 1
    # time for every read_from_exchange() response.
    # Since many write messages generate marketdata, this will cause an
    # exponential explosion in pending messages. Please, don't do that!
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)
    bond_sell_id = sell("BOND",1001,1)
    bond_buy_id = buy("BOND",999,1)
    vale_sell_id, vale_buy_id = next(), next()
    outd[vale_sell_id] = True 
    outd[vale_buy_id] = True
    counter = 0

    while True:
        bond_sell_id, bond_buy_id = bond_trade(bond_sell_id, bond_buy_id)
        if len(histories.securities["VALBZ"].trade) > 20:
            vale_sell_id, vale_buy_id = vale_trade(vale_sell_id, vale_buy_id)
        if len(histories.securities["XLF"].trade) > 20:
            bot.trade()


        for i in range(10):
            msg = read_from_exchange(exchange)

            if is_trade(msg):
                histories.add(msg)

            # clearing IDs
            if getoutid(msg):
                outd[getoutid(msg)] = True




if __name__ == "__main__":
    exchange = connect()
    # try:
    main()
    # except:
        # histories.print_all()
    histories.print_all()
