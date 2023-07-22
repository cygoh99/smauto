#!/usr/bin/env python

import time
import random

from commlib.transports.mqtt import ConnectionParameters
from rich import print
from commlib.msg import PubSubMessage
from commlib.utils import Rate
from commlib.node import Node

class Weather_stationMsg(PubSubMessage):
        temperature: float = 0.0
        humidity: float = 0.0
        airQuality: float = 0.0


class Weather_stationNode(Node):
    def __init__(self, *args, **kwargs):
        self.pub_freq = 1
        self.topic = 'porch.weather_station'
        conn_params = ConnectionParameters(
            host='localhost',
            port=1883,
            username='',
            password='',
        )
        super().__init__(
            node_name='entities.weather_station',
            connection_params=conn_params,
            *args, **kwargs
        )
        self.pub = self.create_publisher(
            msg_type=Weather_stationMsg,
            topic=self.topic
        )

    def start(self):
        self.run()
        rate = Rate(self.pub_freq)
        while True:
            msg = self.gen_data()
            print(f'[Entity - weather_station] Sending data: {msg}')
            self.pub.publish(msg)
            rate.sleep()

    def gen_data(self):
        msg = Weather_stationMsg()
        msg.temperature = random.uniform(20, 40)
        msg.humidity = random.uniform(10, 60)
        msg.airQuality = random.uniform(0, 1)
        return msg


if __name__ == '__main__':
    node = Weather_stationNode()
    node.start()