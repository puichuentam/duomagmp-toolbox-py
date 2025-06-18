from duomag import DUOMAG
from serial.tools import list_ports
import random
import sys
import time


def main():
    vars_dict = user_input()
    print(vars_dict)
    #start_stim()
    #save_output()


def user_input():
    participant_ID = input("Enter ID: ").strip().replace(" ", "")
    session_ID = input("Enter Session Number (e.g., S1): ")

    while True:
        intensity = input("Enter Paired-Pulse Stimulation Intensity (1 - 100): ")
        try:
            intensity = int(intensity)
            if 1 <= intensity <= 100:
                break
            else:
                print("\nValid range is between 1 - 100, an integer.\n")
        except ValueError:
            print("\nNot a valid number. Please enter an integer.\n")

    while True:
        total_pulses = input("Enter the total no. of pulses (e.g., 360 for 180 pairs): ")
        try:
            total_pulses = int(total_pulses)
            if total_pulses > 6:
                break
            else:
                print("\nPlease enter a multiple of 6.\n")
        except ValueError:
            print("\nNot a valid number. Please enter a multiple of 6 integer.\n")


    while True:
        print("Select Stimulation Mode: ")
        print("1 = Synchronized (A & B simultaneous)")
        print("2 = Desynchronized (A then B)")
        print("3 = Desynchronized (B then A)")

        stim_mode = input("Enter Mode Number (1 - 3): ")
        try:
            stim_mode = int(stim_mode)
            if stim_mode in (1, 2, 3):
                break
            else:
                print("\nValid mode is 1 / 2 / 3\n")
        except ValueError:
            print("\nNot a valid number. Please choose from 1 - 3.\n")
    
    match stim_mode:
        case 1:
            delay_ms = 0
        case 2 | 3:
            while True:
                delay_ms = input("Enter Inter-stimulus/inter-pulse interval in ms: ")
                try:
                    delay_ms = int(delay_ms)
                    if delay_ms > 0:
                        break
                    else:
                        print("\nDelay has to be greater than 0.\n")
                except ValueError:
                    print("\nNot a valid number. Delay has to be a non-zero integer.\n")

    while True:
        print("Select Frequency Mode: ")
        print("1 = Fixed Frequency (in seconds)")
        print("2 = Variable Frequency (3 types; in seconds)")

        freq_mode = input("Enter Frequency Mode (1 / 2): ")
        try:
            freq_mode = int(freq_mode)
            if freq_mode in (1, 2):
                break
            else:
                print("\nValid mode is 1 / 2\n")
        except ValueError:
            print("\nNot a valid number. Please choose 1 or 2.\n")
    
    match freq_mode:
        case 1:
            while True:
                interval = input("Enter the fixed frequency in seconds: ")
                try:
                    interval = int(interval)
                    if interval > 0:
                        break
                    else:
                        print("\nPlease set a longer interval.\n")
                except ValueError:
                    print("\nNot a valid number. Please enter a number that is larger than zero.\n")
        case 2:
            while True:
                interval_input = input("Enter 3 numbers in seconds, separated by comma: ").strip()
                try:
                    interval_x, interval_y, interval_z = map(int, interval_input.split(","))
                    if interval_x > 0 and interval_y > 0 and interval_z > 0:
                        break
                    else:
                        print("\nTime has to be greater than 0, integer.\n")
                except ValueError:
                    print("\nNot a valid number. Please enter a number that is larger than zero.\n")

            interval = [interval_x]*(total_pulses/3) + [interval_y]*(total_pulses/3) + [interval_z]* (total_pulses/3)
            interval = random.shuffle(interval)

    #ports = list(list_ports.comports())
    #if len(ports) < 2:
        #sys.exit("\nAt least two serial ports are required.\n")
    
    #print("Availalbe Serial Ports: ")
    #for i, port in enumerate(ports, start=1):
        #print(f"{i}: {port.device} - {port.description}")

    #while True:
        #try:
            #first = int(input("Select a port for coil A [1-{len(ports)}]: "))
            #if 1 <= first <= len(ports):
                #portA = ports[first - 1].device
                #break
            #else:
                #print("\nInvalid choice.\n")
        #except ValueError:
            #print("\nPlease enter a number.\n")

    #while True:
        #try:
            #second = int(input("Select another port for coil B [1-{len(ports)}]: "))
            #if 1 <= second <= len(ports) and second != first:
                #portB = ports[second - 1].device
                #break
            #else:
                #print("\nInvalid or duplicate choice.\n")
        #except ValueError:
            #print("\nPlease enter a number.\n")

    return locals()
    

    

    








    

if __name__ == "__main__":
    main()