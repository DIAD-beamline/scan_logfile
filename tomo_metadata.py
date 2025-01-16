#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 18:59:22 2024

@author: fsd59835
"""

import h5py
from datetime import datetime
import re

# Load the provided file
file_path = '/Users/fsd59835/globus/k11-45357.nxs'

# Read and print the value of 'experiment_identifier'
with h5py.File(file_path, 'r') as file:
    start_time = file['entry/start_time'][()]
    beamline = file['entry/instrument/beamline'][()]
    experiment_no = file['entry/experiment_identifier'][()]
    nominal_energy = file['entry/instrument/configuration_summary/Imaging/nominal_energy'][()]
    config_summary_type = file['entry/instrument/configuration_summary/Imaging/type'][()]
    pco_z = file['entry/instrument/pco/pco_z'][()]
    flats = (file['entry/instrument/imaging/image_key'][()] == 1).sum()
    no_proj = (file['entry/instrument/imaging/image_key'][()] == 0).sum()
    darks = (file['entry/instrument/imaging/image_key'][()] == 2).sum()
    pco_exp = file['entry/instrument/imaging/count_time'][()]
    
    duration = (file['entry/duration'][()])/1000
    dur_hr = int(duration // 3600)
    dur_min = int((duration % 3600) // 60)
    dur_sec = duration % 60
    
    #savu PL
    scan_request = file['entry/diamond_scan/scan_request'][()].decode('utf-8')


# Use regex to find the file path that follows the word "savu"
savu_path_match = re.search(r'savu"\s*:\s*"\s*(.*?)"', scan_request)
savu_path = savu_path_match.group(1) if savu_path_match else None

# Use regex to find all sequences of start, stop, and step values in the scan_request
sequence_matches = re.findall(r'start"\s*:\s*(-?\d+\.?\d*),\s*"stop"\s*:\s*(-?\d+\.?\d*),\s*"step"\s*:\s*(-?\d+\.?\d*)', scan_request)

# Convert matched sequences to a list of dictionaries for easier readability
sequences = [{'start ()': float(match[0]), 'stop': float(match[1]), 'step': float(match[2])} for match in sequence_matches]

    
# Convert the start time to a human-readable format
time_str = start_time.decode('utf-8')
start_timeHR= datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%f")

##
print("Start time : "+start_timeHR.strftime("%A, %B %d, %Y at %I:%M:%S %p"))
print("Beamline : " + beamline.decode('utf-8'))  # Decoding from bytes to string
print("Experiment no. : "+experiment_no.decode('utf-8')) # Decoding from bytes to string
print("X-ray beam type : "+config_summary_type.decode('utf-8'))
print(f"Nominal energy (keV) : {nominal_energy}")
print (f"Propogation dist. (mm) : {pco_z}")
print(f"Exposure time (s) : {pco_exp}")
print(f"No. of flats : {flats}")
print(f"No. of darks : {darks}")
print(f"No. of projection : {no_proj}")
print(f"Duration : {dur_hr}:{dur_min}:{dur_sec:.1f}")

print("savu PL : "+savu_path)
