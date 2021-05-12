#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri May 7 18:04:30 2021

@author: cbell
"""

import os
import json
from flask import Flask, request
from EQTransformer.core.predictor import load_tf_model, predict_on_model
from EQTransformer.utils.hdf5_maker import preprocessor
from EQTransformer.utils.downloader import makeStationListExact, downloadMseedsExact


model = load_tf_model("../ModelsAndSampleData/EqT_model.h5")
app = Flask(__name__)
json_path = "json/station_list.json"


@app.route('/apitest')
def apitest():
    return "API working"

# Main API code

@app.route('/new_list', methods=['POST'])
def create_json():
    if request.method == 'POST':
        client = request.json['client']
        stations = request.json['stations']
        start_time = request.json['start_time']
        end_time = request.json['end_time']
        
        makeStationListExact(json_path = json_path,
                             client = client,
                             stations = stations,
                             start_time = start_time,
                             end_time = end_time)
        

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        client = request.json['client']
        start_time = request.json['start_time']
        end_time = request.json['end_time']
        mseed_dir = "download_mseeds"
        preproc_dir = "preproc"
        hdf5_dir = "download_mseed_processed_hdfs"
    
        downloadMseedsExact(client_name = client,
                            stations_json = json_path,
                            output_dir = mseed_dir,
                            start_time = start_time,
                            end_time = end_time)
    
        preprocessor(preproc_dir, mseed_dir, json_path)
        
        predict_on_model(input_dir = hdf5_dir,
                         input_model = model,
                         output_dir = "detections1")
        
        return "Prediction created"
        ## Call Converter and Post to USNDS once we have that info.
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5005)