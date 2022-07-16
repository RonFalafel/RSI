import requests

import Utils.ConfigurationManager as ConfigurationManager

class LightChanger:
    def __init__(self, configManager: ConfigurationManager):
        self.configManager = configManager

    def changeColor(self, R, G, B, BR):
        config = self.configManager.read()
        home_assistant_ip = config['HOME ASSISTANT']['home_assistant_ip']
        home_assistant_port = config['HOME ASSISTANT']['home_assistant_port']
        requests.post(f"http://{home_assistant_ip}:{home_assistant_port}/api/webhook/light-color-&-brightness-webhook?R={R}&G={G}&B={B}&BR={BR}")

    def defaultColor(self):
        config = self.configManager.read()
        home_assistant_ip = config['HOME ASSISTANT']['home_assistant_ip']
        home_assistant_port = config['HOME ASSISTANT']['home_assistant_port']
        requests.post(f"http://{home_assistant_ip}:{home_assistant_port}/api/webhook/white-light")