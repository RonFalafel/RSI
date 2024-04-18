import requests

import Utils.ILightChanger as ILightChanger
import Utils.RGBToHSVConverter as RGBToHSVConverter

class HALightChanger(ILightChanger.ILightChanger):
    def __init__(self, home_assistant_ip, home_assistant_port):
        self.home_assistant_ip = home_assistant_ip
        self.home_assistant_port = home_assistant_port
        self.rgbToHSVConverter = RGBToHSVConverter()

    def changeColor(self, r, g, b, br = 100):
        hsv = self.rgbToHSVConverter.rgb2hsv(r, g, b)
        requests.post(f"http://{self.home_assistant_ip}:{self.home_assistant_port}/api/webhook/hsv-webhook?H={hsv[0]}&S={hsv[1]}&V={hsv[2]}")

    def defaultColor(self):
        requests.post(f"http://{self.home_assistant_ip}:{self.home_assistant_port}/api/webhook/white-light")