from datetime import datetime
from pathlib import Path
import csv
import project


def simulate_user_input(monkeypatch, inputs_list):
    class FAKEPORT:
        def __init__(self, device, description):
            self.device = device
            self.description = description

    monkeypatch.setattr("project.list_ports.comports", 
                        lambda: [FAKEPORT("COMTest1","Fake port for coil A"), 
                                 FAKEPORT("COMTest2", "Fake port for coil B")])
    inputs = iter(inputs_list)
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    return project.user_input()


def test_user_input(monkeypatch, capsys):
    result = simulate_user_input(monkeypatch, [
            "testID",# participant_ID 
            "S1", # session_ID
            "150", "0", "a", "50", # 150 = failed; 0 = failed; a = failed; 50 = okay (intensity)          
            "5", "a", "6",    # 5 = failed; a = failed; 6 = okay (total_pulses)        
            "4", "a", "1",    # 4 = failed; a = failed; 1 = okay (stim_mode)        
            "3", "a", "2",    # 3 = failed; a = failed; 2 = okay (freq_mode)         
            "0,1,2", "a,b,c", "3,4,5",    # "0,1,2" = failed; "a,b,c" = failed; "3,4,5" = okay (variable interval)            
            "3", "1",    # 3 = failed; 1 = okay (coil A)               
            "1", "2",    # 1 = failed (duplicate); 2 = okay (coil B)               
        ])
    
    out = capsys.readouterr().out

    assert "Valid number is an integer between 1 - 100." in out
    assert "Not a valid number. Please enter an integer." in out
    assert "Please enter a multiple of 6." in out
    assert "Not a valid number. Please enter a multiple of 6 integer." in out
    assert "Valid mode is 1 / 2 / 3" in out
    assert "Not a valid number. Please choose from 1 - 3." in out
    assert "Valid mode is 1 / 2" in out
    assert "Not a valid number. Please choose 1 or 2." in out
    assert "Time has to be a positive integer." in out
    assert "Not a valid number(s). Please enter 3 integers that are larger than zero." in out
    assert "Invalid choice." in out
    assert "Invalid or duplicate choice." in out

    assert result["Start_input"] == datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    assert result["participant_ID"] == "testID"
    assert result["session_ID"] == "S1"
    assert result["intensity"] == 50
    assert result["total_pulses"] == 6
    assert result["stim_mode"] == 1
    assert result["freq_mode"] == 2
    assert result["interval_x"] == 3
    assert result["interval_y"] == 4
    assert result["interval_z"] == 5
    assert result["portA"] == "COMTest1"
    assert result["portB"] == "COMTest2"
    assert result["End_input"] == datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

def test_save_input(monkeypatch):
    result = simulate_user_input(monkeypatch, [
            "testID",# participant_ID 
            "S1", # session_ID
            "150", "0", "a", "50", # 150 = failed; 0 = failed; a = failed; 50 = okay (intensity)          
            "5", "a", "6",    # 5 = failed; a = failed; 6 = okay (total_pulses)        
            "4", "a", "1",    # 4 = failed; a = failed; 1 = okay (stim_mode)        
            "3", "a", "2",    # 3 = failed; a = failed; 2 = okay (freq_mode)         
            "0,1,2", "a,b,c", "3,4,5",    # "0,1,2" = failed; "a,b,c" = failed; "3,4,5" = okay (variable interval)            
            "3", "1",    # 3 = failed; 1 = okay (coil A)               
            "1", "2",    # 1 = failed (duplicate); 2 = okay (coil B)               
        ])
    project.save_input(result)

    with open(Path.cwd() / "logs" / "user_input.csv") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

        assert rows[-1]["participant_ID"] == "testID"
        assert rows[-1]["session_ID"] == "S1"
        assert rows[-1]["intensity"] == "50"
        assert rows[-1]["total_pulses"] == "6"
        assert rows[-1]["stim_mode"] == "1"
        assert rows[-1]["freq_mode"] == "2"
        assert rows[-1]["interval_x"] == "3"
        assert rows[-1]["interval_y"] == "4"
        assert rows[-1]["interval_z"] == "5"
        assert rows[-1]["portA"] == "COMTest1"
        assert rows[-1]["portB"] == "COMTest2"
    

def test_start_stim(monkeypatch):
        
    config = {
        "Start_input": datetime.now().strftime("%Y_%m_%d_%H_%M_%S"), 
        "participant_ID": "testID", 
        "session_ID": "S1", 
        "intensity": 50, 
        "total_pulses": 6, 
        "stim_mode": 2, 
        "stim_mode_str": "A_then_B", 
        "delay_ms": 100, 
        "freq_mode": 2, 
        "freq_mode_str": "variable", 
        "interval": [1,2,3], 
        "interval_input": "1,2,3", 
        "interval_x": 1, 
        "interval_y": 2, 
        "interval_z": 3, 
        "first": 1, 
        "portA": "COMTest1", 
        "second": 2, 
        "portB": "COMTest2",
        "End_input": datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        }
    class FAKEDUOMAG:
        def __init__(self, port): 
            self.port = port
            self.written = []

        def write(self, data):
            self.written.append(data)

        def set_intensity(self, intensity=None):
            self.write(bytes([intensity or 0, intensity or 0])) 

        def duopulse(self):
            self.write(bytes([121, 121]))

        def close(self):
            pass

    fakeA = FAKEDUOMAG(config["portA"])
    fakeB = FAKEDUOMAG(config["portB"])

    monkeypatch.setattr("time.sleep", lambda x: None)

    project.start_stim(config, coil_A=fakeA, coil_B=fakeB)

    assert fakeA.written[0] == bytes([50, 50])
    assert fakeB.written[0] == bytes([50, 50])
    assert fakeA.written[1:4] == [b"yy", b"yy", b"yy"]
    assert fakeB.written[1:4] == [b"yy", b"yy", b"yy"]
    assert fakeA.written[-1] == bytes([0, 0])
    assert fakeB.written[-1] == bytes([0, 0])


def test_save_stim_output():

        config = {
        "Start_input": datetime.now().strftime("%Y_%m_%d_%H_%M_%S"),
        "participant_ID": "testID",
        "session_ID": "S1", 
        "intensity": 50, 
        "total_pulses": 6, 
        "stim_mode": 2, 
        "stim_mode_str": "A_then_B", 
        "delay_ms": 100, 
        "freq_mode": 2, 
        "freq_mode_str": "variable", 
        "interval": [3, 1, 2], 
        "interval_input": "1,2,3", 
        "interval_x": 1, 
        "interval_y": 2, 
        "interval_z": 3, 
        "first": 1, 
        "portA": "COMTest1", 
        "second": 2, 
        "portB": "COMTest2",
        "End_input": datetime.now().strftime("%Y_%m_%d_%H_%M_%S"),
        "Start_stim": datetime.now().strftime("%Y_%m_%d_%H_%M_%S"),
        "coil_A": "fakeA",
        "coil_B": "fakeB",
        "interval_index": 3,
        "pulse_count": 6,
        "errors": "None",
        "End_stim": datetime.now().strftime("%Y_%m_%d_%H_%M_%S") 
        }

        project.save_stim_output(config)

        with open(Path.cwd() / "logs" / "stim_data.csv") as file:
            rows = list(csv.DictReader(file))

            assert rows[-1]["Start_input"] == datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            assert rows[-1]["freq_mode"] == "2"
            assert rows[-1]["interval"] == "[3, 1, 2]"
            assert rows[-1]["portA"] == "COMTest1"
            assert rows[-1]["portB"] == "COMTest2"
            assert rows[-1]["End_input"] == datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            assert rows[-1]["Start_stim"] == datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            assert rows[-1]["coil_A"] == "fakeA"
            assert rows[-1]["coil_B"] == "fakeB"
            assert rows[-1]["pulse_count"] == "6"
            assert rows[-1]["errors"] == "None"
            assert rows[-1]["End_stim"] == datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            




        












