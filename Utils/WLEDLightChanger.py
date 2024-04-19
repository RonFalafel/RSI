import Utils.ILightChanger as ILightChanger
import socket

class WLEDLightChanger(ILightChanger.ILightChanger):
    def __init__(self, wledIP):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.protocol = 1
        self.timeout = 1
        self.UDP_IP_ADDRESS = wledIP
        self.UDP_PORT_NO = 21324
    
    def changeColor(self, r, g, b, br = 100):
        color = (r, g, b)
        # print(f"Changing color to {color} at brightness {br}")

        # Max amount of LEDs
        num_leds = 256

        colors = [color for i in range(num_leds)]

        # Convert to WARLS Protocol
        data = bytearray([self.protocol, self.timeout])
        for i in range(num_leds):
            data += bytearray([i, int(colors[i][0]), int(colors[i][1]), int(colors[i][2])])

        self.sock.sendto(data, (self.UDP_IP_ADDRESS, self.UDP_PORT_NO))
        # print(data, (self.UDP_IP_ADDRESS, self.UDP_PORT_NO))
                   
    def defaultColor(self):
        # From https://github.com/RolandDaum/WLED-UDP-Realtime-Controll-Python-JavaScript/blob/master/WLEDUDP.py (works)
        color = (255, 255, 255)

        # Max amount of LEDs
        num_leds = 256

        colors = [color for i in range(num_leds)]

        # Convert to WARLS Protocol
        data = bytearray([self.protocol, self.timeout])
        for i in range(num_leds):
            data += bytearray([i, int(colors[i][0]), int(colors[i][1]), int(colors[i][2])])

        self.sock.sendto(data, (self.UDP_IP_ADDRESS, self.UDP_PORT_NO))
