from serial import Serial, EIGHTBITS, STOPBITS_TWO


class DUOMAG:
    def __init__(
        self,
        port,
        baudrate=1000000,
        bytesize=EIGHTBITS,
        stopbits=STOPBITS_TWO,
        timeout=1,
    ):
        self.ser = Serial(
            port,
            baudrate=baudrate,
            bytesize=bytesize,
            stopbits=stopbits,
            timeout=timeout,
        )
        self.written = []

    def write(self, data):
        self.written.append(data)

    def set_intensity(self, intensity=0):
        if isinstance(intensity, int) == False:
            raise ValueError("Intensity must be an integer between 1 and 100.")
        elif intensity > 100 or intensity < 0:
            raise ValueError("Intensity must be between 1 and 100.")
        else:
            self.ser.write(bytes([intensity, intensity]))
            self.write(bytes([intensity, intensity]))

    def duopulse(self):
        self.ser.write(bytes([121, 121]))
        self.write(bytes([121, 121]))

    def close(self):
        self.ser.close()
