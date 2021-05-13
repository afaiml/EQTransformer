# -*- coding: utf-8 -*-

import requests
import pandas as pd
import os

def json_poster(detection_dir, post_url):
    station_list =  [os.path.join(detection_dir, site,
                    "X_prediction_results.csv") for site in 
                     os.listdir(detection_dir) if site.split("/")[-1] 
                     != ".DS_Store"]
    
    dfs = []
    for st in station_list:
        dfs.append(pd.read_csv(st))
    df = pd.concat(dfs)
    json = df.to_json()
    head = {"Content-Type": "application/json"}
    list_response = requests.post(post_url,
                            json=json,
                            headers=head)
    return list_response