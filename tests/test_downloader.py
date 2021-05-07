#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 22:34:05 2020

@author: mostafamousavi
"""

from EQTransformer.utils.downloader import downloadMseeds, makeStationList
from EQTransformer.utils.downloader import makeStationListExact, downloadMseedsExact
import pytest
import glob
import os



def test_downloader():
    
    makeStationList(json_path = "test_output/test_downloader/station_list.json",
                  client_list=["SCEDC"],  
                  min_lat=35.50,
                  max_lat=35.60,
                  min_lon=-117.80, 
                  max_lon=-117.40,                      
                  start_time="2019-09-01 00:00:00.00", 
                  end_time="2019-09-03 00:00:00.00",
                  channel_list=["HH[ZNE]", "HH[Z21]", "BH[ZNE]", "EH[ZNE]", "SH[ZNE]", "HN[ZNE]", "HN[Z21]", "DP[ZNE]"],
                  filter_network=["SY"],
                  filter_station=[])
    
    
    downloadMseeds(client_list=["SCEDC", "IRIS"], 
              stations_json='test_output/test_downloader/station_list.json', 
              output_dir="test_output/test_downloader/downloads_mseeds", 
              start_time="2019-09-01 00:00:00.00", 
              end_time="2019-09-02 00:00:00.00", 
              min_lat=35.50,
              max_lat=35.60,
              min_lon=-117.80, 
              max_lon=-117.40,
              chunck_size=1,
              channel_list=[],
              n_processor=2)
    
        
    dir_list = [ev for ev in os.listdir('test_output/test_downloader')]  
    if ('downloads_mseeds' in dir_list) and ('station_list.json' in dir_list):
        successful = True
    else:
        successful = False 
        
    assert successful == True
    
    
def test_mseeds():
    
    mseeds = glob.glob("downloads_mseeds/CA06/*.mseed")
    
    assert len(mseeds) > 0

def test_exact_station_downloader():
        
    makeStationListExact(json_path = "test_output/test_downloader/exact_station_list.json", 
                         client = "IRIS",
                         stations = "ADK,AFI",
                         start_time = "2021-04-01 00:00:00.00",
                         end_time = "2021-04-01 00:00:03.00")
    
    downloadMseedsExact(client_name = "IRIS", 
                        stations_json = "test_output/test_downloader/exact_station_list.json",
                        output_dir = "test_output/test_downloader/exact_download_mseeds",
                        start_time = "2021-04-01 00:00:00.00",
                        end_time = "2021-04-01 00:00:03.00")
    
    dir_list = [ev for ev in os.listdir('test_output/test_downloader')]  
    if ('exact_download_mseeds' in dir_list) and ('exact_station_list.json' in dir_list):
        successful = True
    else:
        successful = False 
        
    assert successful == True