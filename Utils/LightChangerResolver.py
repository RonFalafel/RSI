import Utils.ConfigurationManager as ConfigurationManager, Utils.ILightChanger as ILightChanger, Utils.Mode as Mode
from Utils.HALightChanger import HALightChanger
from Utils.YeeLightChanger import YeeLightChanger

class LightChangerResolver():
    def __init__(self, configManager: ConfigurationManager):
        self.configManager = configManager

    def getLightChanger(self) -> ILightChanger.ILightChanger:
        config = self.configManager.read()
        mode = config['MODE']['mode']
        if str(mode) == str(Mode.Mode.HomeAssistant.name):
            home_assistant_ip = config['HOME ASSISTANT']['home_assistant_ip']
            home_assistant_port = config['HOME ASSISTANT']['home_assistant_port']
            return HALightChanger(home_assistant_ip, home_assistant_port)
        elif str(mode) == str(Mode.Mode.Yeelight.name):
            yeelight_ip = config['YEELIGHT']['yeelight_ip']
            return YeeLightChanger(yeelight_ip)