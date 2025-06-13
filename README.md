# DuoMAG ToolBox MP (Python Port)

This project is a Python-based port of DuoMAG ToolBox MATLAB script designed to control paired-pulse Transcranial Magnetic Stimulation (TMS) using DuoMAG MP stimulators via serial communication. It reproduces key functionality such as user-driven mode selection, serial port interfacing, pulse delivery, and session logging. DuoMAG Driver not included.

---

## Features

- Supports 3 stimulation modes: synchronized, A→B, and B→A
- Inter-pulse and inter-pair interval configuration
- Real-time pulse count tracking
- Session metadata logging
- Emergency crash logging
- Serial communication with DuoMAG MP via PySerial

---

## Requirements

- Python 3.8+
- [PySerial](https://pypi.org/project/pyserial/)
- DuoMAG Driver for Windows (please check with vendor)
- (Optional) [`scipy`](https://pypi.org/project/scipy/) if you want to save logs in `.mat` format

Install dependencies:

```bash
pip install pyserial scipy
