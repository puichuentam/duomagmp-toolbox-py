from datetime import datetime
from duomag import DUOMAG
from net_sender import NetSender
from pathlib import Path
from serial.tools import list_ports
from unittest.mock import patch
import csv
import os
import random
import serial
import sys
import time


def main():
    os.system("cls" if os.name == "nt" else "clear")
    test_mode = False
    test_mode_q = input(
        "For computer without 2 connected serial ports,\nEnter 'y' to enter Test Mode OR other key for actual stimulation: "
    )
    if test_mode_q.lower() == "y":
        test_mode = True
    if test_mode:

        class FakeSerial:
            def __init__(self, port, *args, **kwargs):
                self.port = port
                print(f"FakeSerial initialized for coil: {port}")

            def write(self, data):
                print(f"{self.port} write: {list(data)} to stimulator")

            def close(self):
                print(f"{self.port} closed")

        with patch("duomag.Serial", new=FakeSerial):
            input_data = user_input(test_mode=True)
            save_input(input_data)
            full_data = start_stim(input_data)
            save_stim_output(full_data)
    else:
        input_data = user_input()
        save_input(input_data)
        full_data = start_stim(input_data)
        save_stim_output(full_data)


def user_input(test_mode=False):
    Start_input = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    if test_mode:
        print("\nPlease Enter Parameters for TEST MODE")
    else:
        print("\nPlease Enter Parameters for Paired-pulse TMS Using DuoMAG Stimulators")

    participant_ID = input("\nEnter ID: ").strip().replace(" ", "")
    session_ID = input("\nEnter Session Number (e.g., S1): ")

    while True:
        intensity = input("\nEnter Paired-Pulse Stimulation Intensity (1 - 100): ")
        try:
            intensity = int(intensity)
            if 1 <= intensity <= 100:
                break
            else:
                print("\nValid number is an integer between 1 - 100.")
        except ValueError:
            print("\nNot a valid number. Please enter an integer.")

    while True:
        total_pulses = input(
            "\nEnter the total no. of pulses (e.g., 360 for 180 pairs): "
        )
        try:
            total_pulses = int(total_pulses)
            if total_pulses > 0 and total_pulses % 6 == 0:
                break
            else:
                print("\nPlease enter a multiple of 6.")
        except ValueError:
            print("\nNot a valid number. Please enter a multiple of 6 integer.")

    while True:
        print("\nSelect Stimulation Mode: ")
        print("1 = Synchronized (A & B simultaneous)")
        print("2 = Desynchronized (A then B)")
        print("3 = Desynchronized (B then A)")

        stim_mode = input("\nEnter Mode Number (1 - 3): ")
        try:
            stim_mode = int(stim_mode)
            if stim_mode in (1, 2, 3):
                break
            else:
                print("\nValid mode is 1 / 2 / 3")
        except ValueError:
            print("\nNot a valid number. Please choose from 1 - 3.")

    match stim_mode:
        case 1:
            stim_mode_str = "sync"
            delay_ms = 0
        case 2 | 3:
            if stim_mode == 2:
                stim_mode_str = "A_then_B"
            else:
                stim_mode_str = "B_then_A"
            while True:
                delay_ms = input("\nEnter Inter-stimulus/inter-pulse interval in ms: ")
                try:
                    delay_ms = int(delay_ms)
                    if delay_ms > 0:
                        break
                    else:
                        print("\nDelay has to be greater than 0.")
                except ValueError:
                    print("\nNot a valid number. Delay has to be a non-zero integer.")

    while True:
        print("\nSelect Frequency Mode: ")
        print("1 = Fixed Frequency (in seconds)")
        print("2 = Variable Frequency (3 types; in seconds)")

        freq_mode = input("\nEnter Frequency Mode (1 / 2): ")
        try:
            freq_mode = int(freq_mode)
            if freq_mode in (1, 2):
                break
            else:
                print("\nValid mode is 1 / 2")
        except ValueError:
            print("\nNot a valid number. Please choose 1 or 2.")

    match freq_mode:
        case 1:
            freq_mode_str = "fixed"
            while True:
                interval = input("\nEnter the fixed frequency in seconds: ")
                interval_input = interval_x = interval_y = interval_z = "N/A"
                try:
                    interval = int(interval)
                    if interval > 0:
                        break
                    else:
                        print("\nPlease set a longer interval.")
                except ValueError:
                    print(
                        "\nNot a valid number. Please enter an integer that is larger than zero."
                    )
        case 2:
            freq_mode_str = "variable"
            while True:
                interval_input = (
                    input("\nEnter 3 integers as seconds, separated by comma: ")
                    .strip()
                    .replace(" ", "")
                )
                try:
                    interval_x, interval_y, interval_z = map(
                        int, interval_input.split(",")
                    )
                    if interval_x > 0 and interval_y > 0 and interval_z > 0:
                        break
                    else:
                        print("\nTime has to be a positive integer.")
                except ValueError:
                    print(
                        "\nNot a valid number(s). Please enter 3 integers that are larger than zero."
                    )

            interval = (
                [interval_x] * int((total_pulses / 6))
                + [interval_y] * int((total_pulses / 6))
                + [interval_z] * int((total_pulses / 6))
            )
            random.shuffle(interval)

    if test_mode:
        ports = "FakePorts"
        first = "None"
        portA = "FakeCoilA"
        second = "None"
        portB = "FakeCoilB"
    else:
        ports = list(list_ports.comports())
        if len(ports) < 2:
            sys.exit(
                "Less than 2 serial ports connected. Please check connection. Exiting..."
            )
        print("\nAvailable Serial Ports: ")
        for i, port in enumerate(ports, start=1):
            print(f"{i}: {port.device} - {port.description}")

        while True:
            try:
                first = int(input(f"\nSelect a port for coil A [1-{len(ports)}]: "))
                if 1 <= first <= len(ports):
                    portA = ports[first - 1].device
                    break
                else:
                    print("\nInvalid choice.")
            except ValueError:
                print("\nPlease enter a number.")

        while True:
            try:
                second = int(
                    input(f"\nSelect another port for coil B [1-{len(ports)}]: ")
                )
                if 1 <= second <= len(ports) and second != first:
                    portB = ports[second - 1].device
                    break
                else:
                    print("\nInvalid or duplicate choice.")
            except ValueError:
                print("\nPlease enter a number.")

    End_input = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    return {
        "Start_input": Start_input,
        "participant_ID": participant_ID,
        "session_ID": session_ID,
        "intensity": intensity,
        "total_pulses": total_pulses,
        "stim_mode": stim_mode,
        "stim_mode_str": stim_mode_str,
        "delay_ms": delay_ms,
        "freq_mode": freq_mode,
        "freq_mode_str": freq_mode_str,
        "interval": interval,
        "interval_input": interval_input,
        "interval_x": interval_x,
        "interval_y": interval_y,
        "interval_z": interval_z,
        "first": first,
        "portA": portA,
        "second": second,
        "portB": portB,
        "End_input": End_input,
    }


def save_input(input_data):
    fieldnames = list(input_data)

    input_file_path = Path.cwd() / "logs" / "user_input.csv"
    input_file_path.parent.mkdir(parents=True, exist_ok=True)
    input_file_exists = input_file_path.exists()

    with open(input_file_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not input_file_exists:
            writer.writeheader()
        writer.writerow(input_data)


def start_stim(input_data, coil_A=None, coil_B=None):
    Start_stim = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    if coil_A is None:
        coil_A = DUOMAG(input_data["portA"])
    if coil_B is None:
        coil_B = DUOMAG(input_data["portB"])
    
    net = NetSender(host="192.168.0.152", port=5005, use_tcp=False)

    coil_A.set_intensity(input_data["intensity"])
    coil_B.set_intensity(input_data["intensity"])

    interval_index = 0
    pulse_count = 0

    print()

    i = 3
    while i != 0:
        print(f"Countdown {i}")
        time.sleep(1)
        i -= 1

    print("\nBeginning Stimulation...\n")

    while pulse_count < input_data["total_pulses"]:
        try:
            match input_data["stim_mode"]:
                case 1:
                    coil_A.duopulse()
                    pulse_count += 1
                    print(
                        f"Mode: Synchronized ({pulse_count}/{input_data["total_pulses"]} Pulses Delivered)"
                    )
                    coil_B.duopulse()
                    net.send("B")
                    pulse_count += 1
                    print(
                        f"Mode: Synchronized ({pulse_count}/{input_data["total_pulses"]} Pulses Delivered)"
                    )

                case 2:
                    coil_A.duopulse()
                    pulse_count += 1
                    print(
                        f"Mode: A then B ({pulse_count}/{input_data["total_pulses"]} Pulses Delivered)"
                    )
                    time.sleep(input_data["delay_ms"] / 1000)
                    coil_B.duopulse()
                    net.send("B")
                    pulse_count += 1
                    print(
                        f"Mode: A then B ({pulse_count}/{input_data["total_pulses"]} Pulses Delivered)"
                    )

                case 3:
                    coil_B.duopulse()
                    net.send("B")
                    pulse_count += 1
                    print(
                        f"Mode: B then A ({pulse_count}/{input_data["total_pulses"]} Pulses Delivered)"
                    )
                    time.sleep(input_data["delay_ms"] / 1000)
                    coil_A.duopulse()
                    pulse_count += 1
                    print(
                        f"Mode: B then A ({pulse_count}/{input_data["total_pulses"]} Pulses Delivered)"
                    )

            if input_data["freq_mode"] == 1:
                time.sleep(input_data["interval"])
            else:
                time.sleep(input_data["interval"][interval_index])
                interval_index += 1

        except (
            serial.serialutil.PortNotOpenError,
            serial.SerialException,
            OSError,
            EOFError,
            KeyboardInterrupt,
        ) as errors:
            End_stim = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            print("\nEncountered an error. Saving data...")
            coil_A.close()
            coil_B.close()
            net.close()

            output = {
                "Start_input": input_data["Start_input"],
                "participant_ID": input_data["participant_ID"],
                "session_ID": input_data["session_ID"],
                "intensity": input_data["intensity"],
                "total_pulses": input_data["total_pulses"],
                "stim_mode": input_data["stim_mode"],
                "stim_mode_str": input_data["stim_mode_str"],
                "delay_ms": input_data["delay_ms"],
                "freq_mode": input_data["freq_mode"],
                "freq_mode_str": input_data["freq_mode_str"],
                "interval": input_data["interval"],
                "interval_input": input_data["interval_input"],
                "interval_x": input_data["interval_x"],
                "interval_y": input_data["interval_y"],
                "interval_z": input_data["interval_z"],
                "first": input_data["first"],
                "portA": input_data["portA"],
                "second": input_data["second"],
                "portB": input_data["portB"],
                "End_input": input_data["End_input"],
                "Start_stim": Start_stim,
                "coil_A": coil_A,
                "coil_B": coil_B,
                "interval_index": interval_index,
                "pulse_count": pulse_count,
                "errors": f"{type(errors).__name__}: {errors}",
                "End_stim": End_stim,
            }
            save_stim_output(output)

    print("\nStimulation Ended")
    errors = "None"
    End_stim = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    coil_A.set_intensity()
    coil_B.set_intensity()

    coil_A.close()
    coil_B.close()

    net.close()

    return {
        "Start_input": input_data["Start_input"],
        "participant_ID": input_data["participant_ID"],
        "session_ID": input_data["session_ID"],
        "intensity": input_data["intensity"],
        "total_pulses": input_data["total_pulses"],
        "stim_mode": input_data["stim_mode"],
        "stim_mode_str": input_data["stim_mode_str"],
        "delay_ms": input_data["delay_ms"],
        "freq_mode": input_data["freq_mode"],
        "freq_mode_str": input_data["freq_mode_str"],
        "interval": input_data["interval"],
        "interval_input": input_data["interval_input"],
        "interval_x": input_data["interval_x"],
        "interval_y": input_data["interval_y"],
        "interval_z": input_data["interval_z"],
        "first": input_data["first"],
        "portA": input_data["portA"],
        "second": input_data["second"],
        "portB": input_data["portB"],
        "End_input": input_data["End_input"],
        "Start_stim": Start_stim,
        "coil_A": coil_A,
        "coil_B": coil_B,
        "interval_index": interval_index,
        "pulse_count": pulse_count,
        "errors": errors,
        "End_stim": End_stim,
    }


def save_stim_output(stim_data):
    fieldnames = list(stim_data)
    full_file_path = Path.cwd() / "logs" / "stim_data.csv"
    full_file_path.parent.mkdir(parents=True, exist_ok=True)
    full_file_exists = full_file_path.exists()

    with open(full_file_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not full_file_exists:
            writer.writeheader()
        writer.writerow(stim_data)
        sys.exit("\nData saved.")


if __name__ == "__main__":
    main()
