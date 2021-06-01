#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri May 7 18:04:30 2021

@author: cbell
"""

from flask import Flask, request
from EQTransformer.core.predictor import load_tf_model, predict_on_model
from EQTransformer.utils.hdf5_maker import preprocessor
from EQTransformer.utils.downloader import makeStationListExact, downloadMseedsExact
from json_poster import json_poster


model = load_tf_model("../ModelsAndSampleData/EqT_model.h5")
app = Flask(__name__)
json_path = "json/station_list.json"


@app.route('/apitest')
def apitest():
    """
    A test function for the application.

    Returns
    -------
    str
        DESCRIPTION.

    """
    return "API working"

# Main API code

@app.route('/new_list', methods=['POST'])
def create_json():
    """
    Calls the EQTransformer makeStationListExact method with the given
    posted parameters.  Creates the required json on the server machine and
    overwrites any previous JSON.

    Returns
    -------
    None.

    """
    if request.method == 'POST':
        client = request.json['client']
        stations = request.json['stations']
        start_time = request.json['start_time']
        end_time = request.json['end_time']
        
        makeStationListExact(json_path = json_path,
                             client = client,
                             stations = stations,
                             start_time = start_time,
                             end_time = end_time,
                             channel_list="BH*")
    return "JSON Created"

@app.route('/predict', methods=['POST'])
def predict():
    """
    Calls the EQTransformer downloadMseedsExact, preprocessor, and 
    predict_on_model methods in that order.  This requires that the 
    create_json function has been run and that a json exists on the server 
    machine.  This function stores intermidiate mseeds and hdf5s.  The result
    folder is detections1.  All these folder are overwritten

    Returns
    -------
    None.

    """
    if request.method == 'POST':
        client = request.json['client']
        start_time = request.json['start_time']
        end_time = request.json['end_time']
        mseed_dir = "download_mseeds"
        preproc_dir = "preproc"
        hdf5_dir = "download_mseeds_processed_hdfs"
    
        downloadMseedsExact(client = client,
                            stations_json = json_path,
                            output_dir = mseed_dir,
                            start_time = start_time,
                            end_time = end_time,
                            channel_list = "BH*")
    
        preprocessor(preproc_dir, mseed_dir, json_path)
        
        predict_on_model(input_dir = hdf5_dir,
                         input_model = model,
                         output_probabilities=True,
                         output_dir = "detections1")
        
        ## Uncomment when OSNDS Server can be connected to.
        ## json_poster("detections1", "https://config.osnds.net/json_in")
        
        return "Predictions Made"
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5005, threaded=False)