# Metadata Extractor for .nxs Files

## Overview

This Python script extracts essential metadata from DIAD tomography scan `.nxs` (NeXus) files and outputs the information into a structured, human-readable `.txt` file. The output is organized into clearly defined sections for easier interpretation.

## Features

- Dynamic file selection through command-line or GUI file dialog.
- Human-readable date and time formatting.
- Duration displayed in `hh mm ss` format.
- Organized metadata output with clear section headers:
  - **General Information**
  - **Instrument Parameters**
  - **Scanning Parameters**
  - **Reconstruction Info**

## Requirements

- Python 3.7 or higher
- Required Python packages:
  - `h5py`
  - `tkinter`
  - `argparse`
  - `datetime`
  - `re`

Install dependencies with:

```bash
pip install h5py
```

## Usage

### Command-Line Execution

Run the script from the command line by specifying the file path:

```bash
python metadata_extractor.py --file_path "C:\path\to\file.nxs"
```

### GUI File Selection

Simply run the script without arguments to open a file dialog:

```bash
python metadata_extractor.py
```

## Output

The script generates a `.txt` file in the same directory as the input `.nxs` file. The output will be structured as follows:

```
=== General Information ===
Beamline: I13-2
Experiment no.: 45357
Scan no.: k11-45357
Start Time: Wednesday, July 31, 2024 at 11:52:39 PM

=== Instrument Parameters ===
X-ray beam type: Imaging
Nominal Energy (keV): 25
Propagation dist. (mm): 150.0

=== Scanning Parameters ===
PCO Exposure Time (s): 0.05
Duration: 002h 15m 42s
No. of flats: 10
No. of darks: 10
No. of projection: 500
Start angle: 0.0
Stop angle: 180.0
Angular step: 0.1

=== Reconstruction Info ===
savuPL: /path/to/savu/config.json
```

## Notes

- Ensure `.nxs` files are accessible and not in use by another application.
- Compatible with Windows and cross-platform systems.

## License

This project is licensed under the MIT License.

