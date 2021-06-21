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
        self.inputMessageRequest = "_WaitForInput_"
        self.portlist = self.serial_ports()



    def portSelector(self):
        print("[-]: Aviable serial ports:")

        if len(self.portlist) == 0:
            print("[!]: No ports found!")

            print("[!]: Exiting...")

            sleep(2)

            exit()

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

    def serial_ports(self): ### Jediná část kodu kterou sem převzal z internetu ###
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
        self.device = serial.Serial(self.port, 115200, timeout=1)



    def read(self):
        while 1:
            try:
                self.message = self.device.readline()
                if self.inputMessageRequest in str(self.message):
                    self.write()

                if self.message == b'':
                    pass
                
                else:
                    print("[>]:", self.message)
                
            except KeyboardInterrupt:
                print("[!]: Exiting...")
                sleep(2)
                exit()

            except:
                print("[!]: Disconected!")
                try:
                    self.setdevice()
                except:
                    sleep(2)

    def write(self):
        print("[</>]: -----------------------------")
        print("[</>]: Device want an input message!")
        self.inputMessageString = input("[</>]: Enter string: ")
        print("[</>]: -----------------------------")

        try:
            self.inputMessageString = ascii(self.inputMessageString)
            self.inputMessageBytes = bytes((self.inputMessageString + "#"), "ascii")
            self.device.write(self.inputMessageBytes)

        except:
            print(("[!]: Convert to ASCII Failed!"))






if __name__ == "__main__":
    serialHandler()
