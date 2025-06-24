# DuoMAG ToolBox MP (Python Port; Driver not included)

This project is a Python-based port of DuoMAG ToolBox MATLAB script designed to control paired-pulse Transcranial Magnetic Stimulation (TMS) using DuoMAG MP stimulators via serial communication. It reproduces key functionality such as user-driven mode selection, serial port interfacing, pulse delivery, and session logging. DuoMAG Driver not included.

---

## Features

- Serial communication with DuoMAG MP via PySerial
- Supports 3 stimulation modes: synchronized, A→B, and B→A
- Inter-pulse and inter-pair (fixed/variable) interval configuration
- Pulse Count tracking
- Session metadata logging
- Crash logging
- Data logging (in .csv)

---

## Requirements

- Python 3.8+
- [PySerial](https://pypi.org/project/pyserial/)
- DuoMAG Driver for Windows (please check with vendor)

## Instructions
Install pyserial and pytest(optional) to a venv virtual environment. 
Then run the project.py script.
```bash
pip install pyserial pytest
```
