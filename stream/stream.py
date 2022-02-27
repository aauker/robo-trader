from concurrent.futures import ThreadPoolExecutor
import websocket  
import os
import json
import boto3
from datetime import datetime
import configparser

from concurrent.futures import ThreadPoolExecutor

import logging
logging.basicConfig(format="[%(asctime)s] [%(name)s] %(levelname)s: %(message)s")
logger = logging.getLogger('alpaca2firehose')
logger.setLevel(logging.INFO)
logger.info ("Hello from alpaca2firehose!")

config = configparser.ConfigParser()
config.read('/.aws/alpaca2firehose')

delivery_stream_name = config['firehose']['STREAM_NAME']

firehose = boto3.Session().client('firehose')

executor = ThreadPoolExecutor(4)

logger.info(f"Started firehose @ {delivery_stream_name}")
logger.info(f"Started executor with 4 threads")

def on_open(ws):
    logger.info("Opened Connection")
    auth_data = {"action": "auth", "key": config['alpaca']['ALPACA_KEY_ID'], "secret": config['alpaca']['ALPACA_SECRET_KEY']}

    ws.send(json.dumps(auth_data))
    
    #subscribe to minute bars for all stocks
    listen_message = {"action": "subscribe", "bars": ["*"]}

    ws.send(json.dumps(listen_message))
    
def on_message(ws, message):
    data = json.loads(message)

    if data[0]['T'] not in ['error', 'success', 'subscription']:
        for i in data: executor.submit (alpaca_to_firehose, firehose, i)

def on_close(*args, **kwargs):
    logger.warning(f"Closed Connection with args: {args}, {kwargs}")

def on_error(ws, error):
    logger.error(f"Recieved some error: {error}")

def alpaca_to_firehose(firehose, i):
    item={
        "ticker":      i["S"],
        "open_price":  i["o"],
        "high_price":  i["h"],
        "low_price":   i["l"],
        "close_price": i["c"], 
        "volume":      i["v"],
        "bar_time":    datetime.strptime(i["t"], '%Y-%m-%dT%H:%M:%SZ').timestamp(),
        "real_time":   datetime.now().timestamp()
    }
    logger.info(f"Pushing record: {json.dumps(item)}")
    response = firehose.put_record (
        DeliveryStreamName=delivery_stream_name,
        Record={'Data': json.dumps(item)}
    )
    logger.info ( "Response ID: {0}, status code: {1}".format( response['ResponseMetadata']['RequestId'], ", status code:", response['ResponseMetadata']['HTTPStatusCode'] ) )


if __name__ == '__main__':
    socket = 'wss://stream.data.alpaca.markets/v2/iex'
    logger.info ("Ready to stream stock data from wss://stream.data.alpaca.markets/v2/iex")
    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()
