from datetime import datetime
from duomag import DUOMAG
from serial.tools import list_ports
import csv
import random
import sys
import time


def main():
    input_dict = user_input()
    start_stim(input_dict)
    #save_output()


def user_input():
    participant_ID = input("Enter ID: ").strip().replace(" ", "")
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
        total_pulses = input("\nEnter the total no. of pulses (e.g., 360 for 180 pairs): ")
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
            delay_ms = 0
        case 2 | 3:
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
            while True:
                interval = input("\nEnter the fixed frequency in seconds: ")
                try:
                    interval = int(interval)
                    if interval > 0:
                        break
                    else:
                        print("\nPlease set a longer interval.")
                except ValueError:
                    print("\nNot a valid number. Please enter an integer that is larger than zero.")
        case 2:
            while True:
                interval_input = input("\nEnter 3 integers as seconds, separated by comma: ").strip().replace(" ", "")
                try:
                    interval_x, interval_y, interval_z = map(int, interval_input.split(","))
                    if interval_x > 0 and interval_y > 0 and interval_z > 0:
                        break
                    else:
                        print("\nTime has to be a positive integer.")
                except ValueError:
                    print("\nNot a valid number(s). Please enter 3 integers that are larger than zero.")

            interval = [interval_x]*int((total_pulses/3)) + [interval_y]*int((total_pulses/3)) + [interval_z]*int((total_pulses/3))
            random.shuffle(interval)

    ports = list(list_ports.comports())
    if len(ports) < 2:
        sys.exit("\nAt least two serial ports are required.")
    
    print("\nAvailalbe Serial Ports: ")
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
            second = int(input(f"\nSelect another port for coil B [1-{len(ports)}]: "))
            if 1 <= second <= len(ports) and second != first:
                portB = ports[second - 1].device
                break
            else:
                print("\nInvalid or duplicate choice.")
        except ValueError:
            print("\nPlease enter a number.")

    input_filename = f"{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.csv"
    writer_input = csv.DictWriter()
    return locals()
    

    





if __name__ == "__main__":
    main()