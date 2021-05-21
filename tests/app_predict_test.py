#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Friday May 7 18:45:00

@author: cbell

"""

import requests

predict_json = {"client": "IRIS",
                "start_time": "2021-04-01 00:20:00.00",
                "end_time": "2021-04-01 00:24:00.00"}

head = {"Content-Type": "application/json"}


predict_response = requests.post('http://127.0.0.1:5005/predict',
                                 json=predict_json,
                                 headers=head)

print(predict_response)


