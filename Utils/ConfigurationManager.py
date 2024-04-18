import configparser

import Utils.Mode as Mode

class ConfigurationManager:
    def __init__(self):
        self.config = configparser.ConfigParser()

    def writeMode(self, mode: Mode):
        self.config['MODE'] = {'Mode': mode}
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
        
    def writeHAConfig(self, home_assistant_ip, home_assistant_port):
        self.config['HOME ASSISTANT'] = {'home_assistant_ip': home_assistant_ip, 'home_assistant_port': home_assistant_port}
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def writeYeelightConfig(self, yeelight_ip):
        self.config['YEELIGHT'] = {'yeelight_ip': yeelight_ip}
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def writeRefreshRateConfig(self, refresh_rate):
        self.config['ADVANCED'] = {'refresh_rate': refresh_rate}
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def default(self):
        self.writeMode(Mode.Mode.HomeAssistant.name)
        self.writeHAConfig('192.168.1.123', '8123') # Default home assistant values
        self.writeYeelightConfig('192.168.1.200') # Random made up IP
        self.writeRefreshRateConfig('150')
    
    def read(self):
        try:
            self.config.read('config.ini')
            return self.config
        except:
            print('Reading config failed, writing new config instead.')
            self.default()
