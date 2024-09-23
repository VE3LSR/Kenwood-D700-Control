import serial
import logging



class d700:
    toneCodes = [67.00, 0, 71.90, 74.40, 77.00, 79.70, 82.50, 85.40, 88.50, 91.50, 94.80, 97.40, 100.00, 103.50, 107.20, 110.90, 114.80, 118.80, 123.00, 127.30, 131.80, 136.50, 141.30, 146.20, 151.40, 156.70, 162.20, 167.90, 173.80, 179.90, 186.20, 192.80, 203.50, 210.70, 218.10, 225.70, 233.60, 241.80, 2503.0]

    def __init__(self, port, speed = 9600):
        self.port = port
        self.serial = serial.Serial(port)
        self.serial.baudrate = speed
        if self.serial.isOpen() == False:
            self.serial.open()

    def _send(self, command):
        logging.info(command)
        self.serial.write(command.encode())
        self.serial.write(b"\r\n")

    def setRxFreq(self, freq):
        if freq < 1000:
            freq = int(freq * 1000000)
        CMD = f"FQ {freq:011},0"
        self._send(CMD)

    def setOffset(self, offset):
        if offset[0] in ['-', '+']:
            direction = offset[0]
            freq = int(offset[1:])
        else:
            direction = None
            freq = int(offset)

        freq = int(freq * 1000)
        CMD = f"OS {freq:09}"
        self._send(CMD)

        match direction:
            case "-":
                CMD = "SFT 2"
            case "+":
                CMD = "SFT 1"
            case _:
                CMD = "SFT 0"
        self._send(CMD)

    def setTone(self, tone):
        # Use CTCSS
        CMD = "TO 1"
        self._send(CMD)
        tone = self.toneCodes.index(tone) + 1
        CMD = f"TN {tone}"
        self._send(CMD)
