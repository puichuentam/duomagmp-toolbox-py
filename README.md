# Python Port of DuoMAG Toolbox for paired-pulse Transcranial Magnetic Stimulation (TMS)
#### Description:
This project is a Python-based port of DuoMAG ToolBox MATLAB script designed to control paired-pulse Transcranial Magnetic Stimulation (TMS) using DuoMAG MP stimulators via serial communication. Because not anyone can afford MATLAB, I tried to port it to Python. It reproduces key functionality such as user-driven mode selection, serial port interfacing, pulse delivery, and session logging. Although DuoMAG driver needed for the actual stimulation is not included, anyone can try out this script even if you don't have the driver or the TMS device.

---

## Features

- Serial communication with DuoMAG MP via PySerial
- Mock serial connection and TMS coils
- Supports 6 modes: 3 stimulation mode: synchronized, A→B, and B→A, x 2 frequency mode: fixed/variable frequency (at least 3: e.g., 4,5,6)
- Inter-pulse interval configuration (delay between coils)
- Pulse Count tracking
- User input logging
- Crash logging (in .csv)
- Data logging (also in .csv)

---

## Requirements

- Python 3.8+
- [PySerial](https://pypi.org/project/pyserial/)
- DuoMAG Driver for Windows (please check with vendor)

## Instructions
In a venv virtual environment, install pyserial and pytest(optional;for running test_project.py).
Then run the project.py script.
```bash
pip install pyserial pytest
```
