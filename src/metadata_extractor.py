# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 12:43:07 2025

@author: Sharif Ahmed, Principal Scientist, DIAD, Diamond 
"""
# import necessary packages
import h5py
import argparse
import os
import tkinter as tk
from tkinter import filedialog
from datetime import datetime, timedelta
import re

# the extracts the metadata and formats were necessary e.g. date/time 
def extract_metadata(file_path):
    metadata = {}
    with h5py.File(file_path, 'r') as file:
        #========= Preprocessing metadata to make it human-readable=========
        scan_no = os.path.splitext(os.path.basename(file_path))[0] # get the scan number from the file path. this is not the best as if the .nxs file name is changed it will give the wrong scan no. this is needs fixing
        
        # Exp start time
        raw_start_time = file['entry/start_time'][()] # grab raw timestamp 
        time_str = raw_start_time.decode('utf-8')
        start_timeHR = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%f") 
        formatted_start_time = start_timeHR.strftime("%A, %B %d, %Y at %I:%M:%S %p") # formats in DAy, months, date, time....

        # Measurement duration
        duration_seconds = file['entry/duration'][()] / 1000
        duration_td = timedelta(seconds=duration_seconds)
        hours, remainder = divmod(duration_td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_duration = f"{duration_td.days * 24 + hours:02d}h {minutes:02d}m {seconds:02d}s"

        # Info on theta stage
        scan_request = file['entry/diamond_scan/scan_request'][()].decode('utf-8')
        theta_info = re.findall(r'start"\s*:\s*(-?\d+\.?\d*),\s*"stop"\s*:\s*(-?\d+\.?\d*),\s*"step"\s*:\s*(-?\d+\.?\d*)', scan_request) # Use regex to find all sequences of start, stop, and step values in the scan_request
        # get the name of the savu PL
        savu_path_match = re.search(r'savu"\s*:\s*"\s*(.*?)"', scan_request)
        savu_path = savu_path_match.group(1) if savu_path_match else None

        # === General Information ===
        metadata['Beamline'] = file['entry/instrument/beamline'][()].decode('utf-8')
        metadata['Experiment no.'] = file['entry/experiment_identifier'][()].decode('utf-8')
        metadata['Scan no.'] = scan_no
        metadata['Start Time'] = formatted_start_time

        # === Instrument Parameters ===
        metadata['X-ray beam type'] = file['entry/instrument/configuration_summary/Imaging/type'][()].decode('utf-8')
        metadata['Nominal Energy (keV)'] = file['entry/instrument/configuration_summary/Imaging/nominal_energy'][()]
        metadata['Propagation dist. (mm)'] = file['entry/instrument/pco/pco_z'][()]

        # === Scanning Parameters ===
        metadata['PCO Exposure Time (s)'] = file['entry/instrument/imaging/count_time'][()]
        metadata['Duration'] = formatted_duration
        metadata['No. of flats'] = (file['entry/instrument/imaging/image_key'][()] == 1).sum()
        metadata['No. of darks'] = (file['entry/instrument/imaging/image_key'][()] == 2).sum()
        metadata['No. of projection'] = (file['entry/instrument/imaging/image_key'][()] == 0).sum()
        metadata['Start angle'] = theta_info[0][0]
        metadata['Stop angle'] = theta_info[0][1]
        metadata['Angular step'] = theta_info[0][2]

        # === Reconstruction Info ===
        metadata['savu PL'] = savu_path
    return metadata

def save_metadata_to_txt(metadata, output_path):
    with open(output_path, 'w') as f:
        f.write("=== General Information ===\n")
        f.write(f"Beamline: {metadata['Beamline']}\n")
        f.write(f"Experiment no.: {metadata['Experiment no.']}\n")
        f.write(f"Scan no.: {metadata['Scan no.']}\n")
        f.write(f"Start Time: {metadata['Start Time']}\n\n")
        
        f.write("=== Instrument Parameters ===\n")
        f.write(f"X-ray beam type: {metadata['X-ray beam type']}\n")
        f.write(f"Nominal Energy (keV): {metadata['Nominal Energy (keV)']}\n")
        f.write(f"Propagation dist. (mm): {metadata['Propagation dist. (mm)']}\n\n")
        
        f.write("=== Scanning Parameters ===\n")
        f.write(f"PCO Exposure Time (s): {metadata['PCO Exposure Time (s)']}\n")
        f.write(f"Duration: {metadata['Duration']}\n")
        f.write(f"No. of flats: {metadata['No. of flats']}\n")
        f.write(f"No. of darks: {metadata['No. of darks']}\n")
        f.write(f"No. of projection: {metadata['No. of projection']}\n")
        f.write(f"Start angle: {metadata['Start angle']}\n")
        f.write(f"Stop angle: {metadata['Stop angle']}\n")
        f.write(f"Angular step: {metadata['Angular step']}\n\n")
        
        f.write("=== Reconstruction Info ===\n")
        f.write(f"savuPL: {metadata['savu PL']}\n")

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title='Select .nxs file',
        filetypes=[('NeXus files', '*.nxs')]
    )
    return file_path

def main():
    parser = argparse.ArgumentParser(description='Extract metadata from a .nxs file')
    parser.add_argument('--file_path', type=str, help='Path to the .nxs file')
    args = parser.parse_args()

    file_path = args.file_path or select_file()
    if not file_path:
        print("No file selected. Exiting.")
        return

    metadata = extract_metadata(file_path)
    output_path = os.path.splitext(file_path)[0] + '_metadata.txt'
    save_metadata_to_txt(metadata, output_path)
    print(f"Metadata has been saved to {output_path}")

if __name__ == '__main__':
    main()
