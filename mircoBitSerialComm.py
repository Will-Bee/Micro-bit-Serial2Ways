### $ pip uninstall serial
### $ pip install pyserial


### Na micro:bitu musíte pomocí tlačítka odeslat string "WaitForInput", někdy je potřeba zmáčknout vícekrát
### Poté přidat spouštěč funkcí " sériové na přijatá data (#v) " (weird čeština)
### Jako první akci v tomto spouštěči nastavte jakoukoliv proměnnou na ( sériový číst dokud (#v) )
### Poté se s touto proměnnou dá operovat jakkoliv, přepíše se po každém poslání dat

from time import sleep
import serial
import glob
import sys








class serialHandler:

    def __init__(self):
        print("\033c", end="")
        self.variables()

        self.portSelector()
        self.setdevice()
        self.read()

    def variables(self):
        self.inputMessageRequest = "WaitForInput"
        self.portlist = self.serial_ports()



    def portSelector(self):
        print("[-]: Aviable serial ports:")

        if len(self.portlist) == 0:
            print("[!]: No ports found!")
            sleep(2)
            print("\033c", end="")
            self.portSelector()

        else:
            print("[-]:", self.portlist)
            self.selected_int = input("[>]: Select port: ")

        try:
            self.selected_int = int(self.selected_int)
            self.port_id = self.selected_int - 1
            self.port = self.portlist[self.port_id]
            print("[-]: Port", self.port, "selected \n")

        except:
            print("\033c", end="")
            print("[!]: Wrong option!")
            self.portSelector()

    def serial_ports(self): ### Jediná část kodu kterou sem převzal z internetu
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]

        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
            
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')

        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)

            except (OSError, serial.SerialException):
                pass

        return result

    def setdevice(self):
        self.device = serial.Serial(self.port, 115200, timeout=.1)



    def read(self):
        while 1:
            print("[>]:", self.device.readline())
            if self.inputMessageRequest in str(self.device.readline()):
                print("[</>]: -----------------------------")
                print("[</>]: Device want an input message!")
                self.write()

    def write(self):
        self.inputMessageString = input("[</>]: Enter string: ")
        print("[</>]: -----------------------------")

        self.inputMessageBytes = bytes((self.inputMessageString + "#"), "ascii")
        self.device.write(self.inputMessageBytes)





if __name__ == "__main__":
    serialHandler()