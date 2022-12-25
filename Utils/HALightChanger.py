import requests

import Utils.ILightChanger as ILightChanger

class HALightChanger(ILightChanger.ILightChanger):
    def __init__(self, home_assistant_ip, home_assistant_port):
        self.home_assistant_ip = home_assistant_ip
        self.home_assistant_port = home_assistant_port

    def changeColor(self, h, s, v):
        requests.post(f"http://{self.home_assistant_ip}:{self.home_assistant_port}/api/webhook/hsv-webhook?H={h}&S={s}&V={v}")

    def defaultColor(self):
        requests.post(f"http://{self.home_assistant_ip}:{self.home_assistant_port}/api/webhook/white-light")