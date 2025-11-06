import argparse
from ipaddress import ip_address
import socket
import sys

class CPSC:
    def __init__(self, address, port, timeout=1):
        self.address = address
        self.port = int(port)
        self.timeout = timeout
        self._connect()

    def _connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(self.timeout)
        self.client.connect((self.address, self.port))

    def _write(self, message):
        message = message.encode('ascii') + b'\r\n'
        self.client.sendall(message)

    def _read(self):
        value = b''
        delimiter = b'\r\n'
        while delimiter not in value:
            data = self.client.recv(32)
            if not data:
                return None
            value += data

        return value

    def _close(self):
        self.client.close()
        
    def _decode(self, data) -> str:
        cr = b'\x0D'
        lf = b'\x0A'
        delimiter = cr + lf

        data = data.strip(delimiter).decode()

        return data

    def move_cadm2(self, dir, freq, step, temp):
        rss = 100
        stage = 'CLA2601'
        df = 1

        command = f'MOV 1 {dir} {freq} {rss} {step} {temp} {stage} {df}'
        self._write(command)
        move_res = self._read()
        move_res = self._decode(move_res)

        print("Start actuating the stage...: {}".format(move_res))

        self._close()

    def stop_cadm2(self):
        self._write('STP 1')
        stop_res = self._read()
        stop_res = self._decode(stop_res)

        print("Stopping the stage...: {}".format(stop_res))

        self._close()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cryo Positioning Systems Controller Command")
    parser.add_argument("--stop", action=argparse.BooleanOptionalAction, help="Immediately stop the liner actuator")
    parser.add_argument("-a", "--address", type=ip_address, required=True, help="IP Address of JPE CAB1-115 Unit")
    parser.add_argument("-d", "--direction", type=int, default=1, help="Direction (1 for positive movement and 0 for negative movement) [Default: 1]")
    parser.add_argument("-f", "--frequency", type=int, default=300, help="Frequency (1[Hz] to 600[Hz]) [Default: 300[Hz]]")
    parser.add_argument("-s", "--step", type=int, default=0, help="Number of actuation steps. Range 0 to 5000, where 0 is used for infinite move [Default: 0]")
    parser.add_argument("-t", "--temperature", type=int, default=300, help="Temperature of the environment in which the actuator is used in Kelvin[K]. Range 0[K] to 300[K]. [Default: 300[K]]")
    args = parser.parse_args()

    # CPSC Info
    address = args.address
    port = 2000
    # Connect CPSC
    try:
        cpsc = CPSC(str(address), port)
    except TimeoutError:
        print("Timeout error occured")
        sys.exit(1)

    # Stop Liner Actuator
    if args.stop:
        print("Stop command executed")
        cpsc.stop_cadm2()
        sys.exit(0)

    dir = args.direction
    if dir not in [0, 1]:
        print("Direction must be 0 (negative) or 1 (positive).")
        sys.exit(1)
    freq = args.frequency
    if freq not in range(1, 601):
        print("Frequency must be from 1[Hz] to 600[Hz].")
        sys.exit(1)
    step = args.step
    if step not in range(0, 5001):
        print("Number of steps must be from 0 (infinite) to 5000.")
        sys.exit(1)
    temp = args.temperature
    if temp not in range(0, 301):
        print("Temperature must be betwen 0[K] to 300[K]")
        sys.exit(1)

    # Move Liner Actuator
    print("Move command executed")
    print(f"Direction:\t{dir}\nFrequency:\t{freq}[Hz]\nStep:\t\t{step}\nTemperature:\t{temp}[K]")
    # cpsc.move_cadm2(dir, freq, step, temp)
    print(args.address)