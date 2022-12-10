import requests

import Utils.ILightChanger as ILightChanger

class HALightChanger(ILightChanger.ILightChanger):
    def __init__(self, home_assistant_ip, home_assistant_port):
        self.home_assistant_ip = home_assistant_ip
        self.home_assistant_port = home_assistant_port

    def changeColor(self, r, g, b, br):
        requests.post(f"http://{self.home_assistant_ip}:{self.home_assistant_port}/api/webhook/light-color-&-brightness-webhook?R={r}&G={g}&B={b}&BR={br}")

    def defaultColor(self):
        requests.post(f"http://{self.home_assistant_ip}:{self.home_assistant_port}/api/webhook/white-light")