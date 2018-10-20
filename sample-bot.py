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
print(sys.argv)

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
    return randrange(2**16)

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
    request = {"type": "add", "order_id": ID, "symbol": symbol, "dir": "SELL", "price": price, "size": size}
    write_to_exchange(exchange,request)
    return ID
    

def buy(symbol, price, size):
    ID = next()
    request = {"type": "add", "order_id": ID, "symbol": symbol, "dir": "BUY", "price": price, "size": size}
    write_to_exchange(exchange,request)
    return ID

def getoutid(request):
    if request["type"] == "out":
        return request["order_id"]
    else:
        False


def bond_trade(sell_id, buy_id):
    global outd
    if outd[sell_id]:
        sell_id = sell("BOND",1001,20)
        print("sell", sell_id)
    if outd[buy_id]:
        buy_id = buy("BOND",999,20)
        print("buy", buy_id)
    return sell_id, buy_id


def is_trade(msg):
    return msg["type"] == "trade"

def print_trade(msg):
    if mgs["symbol"] in ["VALE", "VALBZ"]:
        print(msg["symbol"], msg["dir"], msg["price"], msg["size"])
    #if mgs["symbol"] ==


class trade_history

# ~~~~~============== MAIN LOOP ==============~~~~~


BUY = "BUY"
SELL = "SELL"

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

    while True:
        bond_sell_id, bond_buy_id = bond_trade(bond_sell_id, bond_buy_id)
        message = read_from_exchange(exchange)

        if is_trade(msg):
            print_trade(msg)

        # clearing IDs
        if getoutid(message):
            outd[getoutid(message)] = True




if __name__ == "__main__":
    exchange = connect()
    main()
